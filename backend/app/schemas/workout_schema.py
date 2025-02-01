from typing import List
from pydantic import BaseModel

class ExercisePlan(BaseModel):
    name: str
    sets: int
    reps: int
    rest_between_sets: int  # in seconds

class WorkoutPlan(BaseModel):
    exercises: List[ExercisePlan]
    rest_time_hours: float