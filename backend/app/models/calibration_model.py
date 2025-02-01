from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from .base_model import Base

class Calibration(Base):
    __tablename__ = "calibrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    height = Column(Float)
    weight = Column(Float)
    sex = Column(String)
    body_fat_percentage = Column(Float)
    calibration_score = Column(Float)
    created_at = Column(DateTime, server_default=func.now())