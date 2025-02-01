from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.app.schemas import calibration_schema
from backend.app.models import calibration_model, exercise_result_model, exercise_model
from backend.app.models import profile_model 
from backend.app.models.associations import exercise_muscle
from backend.app.utils.database import get_db
from backend.app.routers.auth_route import get_current_user

router = APIRouter(
    prefix="/calibration",
    tags=["calibration"],
)

@router.post("/", response_model=calibration_schema.CalibrationResponse)
def calibrate(
    calibration_request: calibration_schema.CalibrationRequest,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Ensure that the user's profile has been set up
    profile = db.query(profile_model.Profile).filter(profile_model.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="User profile incomplete. Please set up your profile first.")
    
    if not calibration_request.exercises:
        raise HTTPException(status_code=400, detail="No exercise results provided.")

    # Validate that each exercise exists in the DB and calculate an effective score that incorporates muscle impacts
    effective_scores = []
    valid_exercise_names = {e.name: e for e in db.query(exercise_model.Exercise).all()}
    for name, score in calibration_request.exercises.items():
        exercise_obj = valid_exercise_names.get(name)
        if not exercise_obj:
            raise HTTPException(status_code=400, detail=f"Invalid exercise: {name}")
        # Query the association table for impacts of this exercise
        stmt = select(exercise_muscle.c.impact).where(exercise_muscle.c.exercise_id == exercise_obj.id)
        results = db.execute(stmt).scalars().all()
        if results:
            total_impact = sum(results)
        else:
            total_impact = 1.0  # Fallback if no muscles are associated
        effective_scores.append(score * total_impact)
    
    # Use the average effective score and adjust based on the profile.
    avg_effective_score = sum(effective_scores) / len(effective_scores)
    ratio = profile.weight / profile.height
    gender_adjustment = 1.1 if profile.sex.lower() == "male" else 0.9
    calibration_score = avg_effective_score + (ratio * gender_adjustment) - (profile.body_fat_percentage * 0.1)
    
    # Save calibration record with profile data
    calibration_obj = calibration_model.Calibration(
        user_id=current_user.id,
        height=profile.height,
        weight=profile.weight,
        sex=profile.sex,
        body_fat_percentage=profile.body_fat_percentage,
        calibration_score=calibration_score
    )
    db.add(calibration_obj)
    db.commit()
    db.refresh(calibration_obj)
    
    # Save individual exercise results
    for exercise_name, score in calibration_request.exercises.items():
        exercise_result = exercise_result_model.ExerciseResult(
            calibration_id=calibration_obj.id,
            exercise=exercise_name,
            score=score
        )
        db.add(exercise_result)
    db.commit()
    
    return calibration_schema.CalibrationResponse(calibration_score=calibration_score)