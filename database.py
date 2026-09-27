from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    workout_type = Column(String)  # Велосипед, Бег, Плавание, Силовая, Кардио
    duration = Column(Integer)  # в минутах
    intensity = Column(String)  # низкая, средняя, высокая
    distance = Column(Float, nullable=True)  # дистанция
    distance_unit = Column(String, nullable=True)  # км/м
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    goal_type = Column(String)  # выносливость, скорость, дистанция, сила, вес
    target = Column(String)  # описание цели
    deadline = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Инициализация базы данных - создание всех таблиц"""
    Base.metadata.create_all(bind=engine)
    print("✅ Таблицы базы данных созданы")


def get_db():
    """Генератор сессии БД для зависимостей"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Утилиты для работы с БД
def get_or_create_user(telegram_id: int, username: str = None, first_name: str = None):
    """Получить пользователя или создать нового"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()