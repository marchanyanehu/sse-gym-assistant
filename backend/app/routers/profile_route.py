from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.schemas import profile_schema
from backend.app.models import profile_model
from backend.app.routers.auth_route import get_current_user
from backend.app.utils.database import get_db

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
)

@router.post("/", response_model=profile_schema.Profile)
def create_or_update_profile(
    profile_data: profile_schema.ProfileCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_profile = db.query(profile_model.Profile).filter(profile_model.Profile.user_id == current_user.id).first()
    if existing_profile:
        existing_profile.height = profile_data.height
        existing_profile.weight = profile_data.weight
        existing_profile.sex = profile_data.sex
        existing_profile.body_fat_percentage = profile_data.body_fat_percentage
        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    else:
        new_profile = profile_model.Profile(
            user_id=current_user.id,
            height=profile_data.height,
            weight=profile_data.weight,
            sex=profile_data.sex,
            body_fat_percentage=profile_data.body_fat_percentage,
        )
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile