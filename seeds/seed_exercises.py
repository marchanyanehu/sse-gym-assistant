
from sqlalchemy.orm import Session
from backend.app.models.base_model import Base
from backend.app.models.exercise_model import Exercise
from backend.app.utils.database import engine, SessionLocal

def seed_exercises(db: Session):
    exercises = [
        {"name": "pushups"},
        {"name": "squats"},
        {"name": "pullups"},
        {"name": "lunges"},
        {"name": "planks"},
        {"name": "burpees"},
        {"name": "dips"},
        {"name": "mountain climbers"},
        {"name": "jumping jacks"}
    ]
    
    for ex in exercises:
        exists = db.query(Exercise).filter(Exercise.name == ex["name"]).first()
        if not exists:
            exercise = Exercise(name=ex["name"])
            db.add(exercise)
    db.commit()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_exercises(db)
        print("Exercise seed complete!")