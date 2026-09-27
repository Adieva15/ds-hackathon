import sys
import os

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_db, SessionLocal, User, Workout, Goal
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_sample_data():
    """Создание тестовых данных"""
    db = SessionLocal()

    try:
        # Проверяем, есть ли уже тестовый пользователь
        existing_user = db.query(User).filter(User.telegram_id == 123456789).first()
        if existing_user:
            print("✅ Тестовые данные уже существуют")
            return

        print("🔄 Создаем тестового пользователя...")
        # Создаем тестового пользователя
        test_user = User(
            telegram_id=123456789,
            username="test_user",
            first_name="Test User"
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        print("🔄 Создаем тестовые тренировки...")
        # Создаем несколько тестовых тренировок
        workouts = [
            Workout(
                user_id=test_user.telegram_id,
                workout_type="Велосипед",
                duration=45,
                intensity="средняя",
                distance=15.5,
                distance_unit="километров",
                notes="Утренняя поездка по парку"
            ),
            Workout(
                user_id=test_user.telegram_id,
                workout_type="Бег",
                duration=30,
                intensity="высокая",
                distance=5.2,
                distance_unit="километров",
                notes="Интервальный бег"
            ),
            Workout(
                user_id=test_user.telegram_id,
                workout_type="Плавание",
                duration=40,
                intensity="средняя",
                distance=800,
                distance_unit="метров",
                notes="Базовые упражнения в бассейне"
            )
        ]

        for workout in workouts:
            db.add(workout)

        print("🔄 Создаем тестовые цели...")
        # Создаем цели
        goals = [
            Goal(
                user_id=test_user.telegram_id,
                goal_type="выносливость",
                target="Пробежать 10 км без остановки",
                is_completed=False
            ),
            Goal(
                user_id=test_user.telegram_id,
                goal_type="дистанция",
                target="Проехать 50 км на велосипеде за одну поездку",
                is_completed=False
            )
        ]

        for goal in goals:
            db.add(goal)

        print("✅ Тестовые данные созданы успешно")

        # Показываем что создали
        user_count = db.query(User).count()
        workout_count = db.query(Workout).count()
        goal_count = db.query(Goal).count()

        print(f"📊 Создано:")
        print(f"   👤 Пользователей: {user_count}")
        print(f"   🏋️ Тренировок: {workout_count}")
        print(f"   🎯 Целей: {goal_count}")

    except Exception as e:
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Начало инициализации базы данных...")
    try:
        # Инициализируем базу данных
        init_db()

        # Создаем тестовые данные
        create_sample_data()

        print("🎉 База данных успешно инициализирована и готова к использованию!")
        print("📍 Файл базы данных: fitness_bot.db")

    except Exception as e:
        print(f"💥 Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()