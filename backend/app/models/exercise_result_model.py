from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from .base_model import Base

class ExerciseResult(Base):
    __tablename__ = "exercise_results"
    id = Column(Integer, primary_key=True, index=True)
    calibration_id = Column(Integer, ForeignKey("calibrations.id"))
    exercise = Column(String)
    score = Column(Float)
    created_at = Column(DateTime, server_default=func.now())