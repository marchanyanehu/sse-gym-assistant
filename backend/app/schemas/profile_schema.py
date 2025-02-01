from pydantic import BaseModel

class ProfileCreate(BaseModel):
    height: float
    weight: float
    sex: str  # "male" or "female"
    body_fat_percentage: float

class Profile(BaseModel):
    id: int
    user_id: int
    height: float
    weight: float
    sex: str
    body_fat_percentage: float

    class Config:
        from_attributes = True