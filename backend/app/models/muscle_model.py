from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base_model import Base
from .associations import exercise_muscle

class Muscle(Base):
    __tablename__ = "muscles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    exercises = relationship("Exercise", secondary=exercise_muscle, back_populates="muscle_groups")