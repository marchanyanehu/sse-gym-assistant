from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base_model import Base
from .associations import exercise_muscle

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    muscle_groups = relationship("Muscle", secondary=exercise_muscle, back_populates="exercises")