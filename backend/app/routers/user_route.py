from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.schemas import user_schema as user_schema
from backend.app.services import user_service as user_service
from backend.app.utils.database import get_db
from .auth_route import get_current_user 

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=user_schema.User)
def read_current_user(current_user: user_schema.User = Depends(get_current_user)):
    return current_user

@router.post("/", response_model=user_schema.User)
def create_user_endpoint(
    username: str, 
    email: str, 
    password: str, 
    db: Session = Depends(get_db)
):
    user_data = user_schema.UserCreate(username=username, email=email, password=password)
    try:
        db_user = user_service.create_user(db, user_data)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    return db_user

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_service.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

