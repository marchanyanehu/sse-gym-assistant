# language: python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.schemas.workout_schema import WorkoutPlan
from backend.app.services.workout_service import generate_workout_plan
from backend.app.models import profile_model
from backend.app.routers.auth_route import get_current_user
from backend.app.utils.database import get_db
from typing import Literal

router = APIRouter(
    prefix="/workout",
    tags=["workout"],
)

@router.get("/plan", response_model=WorkoutPlan)
def get_workout_plan(
    current_user = Depends(get_current_user), 
    db: Session = Depends(get_db),
    goal: Literal[
        "weightloss (with muscle preservence)", 
        "weightloss (without muscle preservence)", 
        "build muscles", 
        "build strength", 
        "build endurance"
    ] = "build muscles"
):
    profile = db.query(profile_model.Profile).filter(profile_model.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="User profile not found. Please set up your profile first.")
    
    workout_plan = generate_workout_plan(profile, calibration_score=None, goal=goal)
    return workout_plan