# language: python
from sqlalchemy.orm import Session
from backend.app.models.muscle_model import Muscle
from backend.app.models.exercise_model import Exercise
from backend.app.models.associations import exercise_muscle
from backend.app.utils.database import engine, SessionLocal
from backend.app.models.base_model import Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def seed_muscles(db: Session):
    # Define muscle groups to seed.
    muscle_names = ["chest", "back", "legs", "arms", "shoulders", "core"]
    muscles = {}
    for name in muscle_names:
        muscle = db.query(Muscle).filter(Muscle.name == name).first()
        if not muscle:
            muscle = Muscle(name=name)
            db.add(muscle)
            db.commit()
            db.refresh(muscle)
        muscles[name] = muscle
    return muscles

def seed_muscle_associations(db: Session, muscles: dict):
    # Define a mapping of exercise names to their associated muscles with impact
    # You may adjust the mapping and impact values as needed.
    associations = {
        "pushups": [("chest", 1.0), ("arms", 0.8), ("shoulders", 0.7)],
        "squats": [("legs", 1.0), ("core", 0.5)],
        "pullups": [("back", 1.0), ("arms", 0.9)],
        "lunges": [("legs", 1.0), ("core", 0.6)],
        "planks": [("core", 1.0)],
        "burpees": [("legs", 0.8), ("arms", 0.7), ("core", 0.7)],
        "dips": [("arms", 1.0), ("chest", 0.8)],
        "mountain climbers": [("core", 0.9), ("legs", 0.7)],
        "jumping jacks": [("legs", 0.6), ("shoulders", 0.6)]
    }
    
    for ex_name, muscle_data in associations.items():
        # Find the exercise using its unique name
        exercise = db.query(Exercise).filter(Exercise.name == ex_name).first()
        if not exercise:
            continue  # Skip if exercise is not seeded
        for muscle_name, impact in muscle_data:
            muscle = muscles.get(muscle_name)
            if not muscle:
                continue
            # Manually insert into the association table with an impact value.
            # This assumes the exercise_muscle table is used directly.
            db.execute(
                exercise_muscle.insert().values(
                    exercise_id=exercise.id,
                    muscle_id=muscle.id,
                    impact=impact
                )
            )
    db.commit()

if __name__ == "__main__":
    with SessionLocal() as db:
        muscles = seed_muscles(db)
        seed_muscle_associations(db, muscles)
        print("Muscle seed and associations complete!")