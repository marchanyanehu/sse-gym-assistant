from typing import List
from pydantic import BaseModel

class WorkoutPlan(BaseModel):
    exercises: List[str]
    duration: int 