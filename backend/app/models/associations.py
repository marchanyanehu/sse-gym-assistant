from sqlalchemy import Table, Column, Integer, Float, ForeignKey
from .base_model import Base

exercise_muscle = Table(
    "exercise_muscle",
    Base.metadata,
    Column("exercise_id", Integer, ForeignKey("exercises.id"), primary_key=True),
    Column("muscle_id", Integer, ForeignKey("muscles.id"), primary_key=True),
    Column("impact", Float, nullable=False)
)