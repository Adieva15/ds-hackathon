from database import SessionLocal, Workout, Goal, get_or_create_user


def get_user_data(user_id, username=None, first_name=None):
    db = SessionLocal()
    try:
        user = get_or_create_user(user_id, username, first_name)

        workouts_count = db.query(Workout).filter(Workout.user_id == user_id).count()

        goals = db.query(Goal).filter(Goal.user_id == user_id, Goal.is_completed == False).all()
        goal_texts = [goal.target for goal in goals] if goals else ['стать сильнее']

        return {"workouts": workouts_count, "goals": goal_texts}
    except:
        return {"workouts": 0, "goals": ["стать сильнее"]}
    finally:
        db.close()


def update_user_workouts(user_id, workout_type="бег", duration=0):
    db = SessionLocal()
    try:
        workout = Workout(user_id=user_id, workout_type=workout_type, duration=duration)
        db.add(workout)
        db.commit()
        return db.query(Workout).filter(Workout.user_id == user_id).count()
    except:
        return db.query(Workout).filter(Workout.user_id == user_id).count()
    finally:
        db.close()


def get_user_workouts(user_id):
    db = SessionLocal()
    try:
        return db.query(Workout).filter(Workout.user_id == user_id).count()
    except:
        return 0
    finally:
        db.close()


def add_user_goal(user_id, goal_text):
    db = SessionLocal()
    try:
        goal = Goal(user_id=user_id, target=goal_text)
        db.add(goal)
        db.commit()
        return goal
    except:
        return None
    finally:
        db.close()