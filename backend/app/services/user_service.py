from sqlalchemy.orm import Session
from backend.app.models import user_model as user_model
from backend.app.schemas import user_schema as user_schema
from backend.app.services import auth_service

def create_user(db: Session, user_data: user_schema.UserCreate) -> user_model.User:
    # Check if the email is already registered
    db_user = db.query(user_model.User).filter(user_model.User.email == user_data.email).first()
    if db_user:
        raise ValueError("Email already registered")
    # Hash the password and create the user
    hashed_password = auth_service.get_password_hash(user_data.password)
    db_user = user_model.User(
        username=user_data.username, 
        email=user_data.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> user_model.User:
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()