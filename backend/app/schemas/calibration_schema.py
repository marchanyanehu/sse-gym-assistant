from typing import Dict
from pydantic import BaseModel

class CalibrationRequest(BaseModel):
    exercises: Dict[str, float]

class CalibrationResponse(BaseModel):
    calibration_score: float