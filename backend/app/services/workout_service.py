from backend.app.schemas.workout_schema import WorkoutPlan
from backend.app.models.profile_model import Profile

def generate_workout_plan(profile: Profile, calibration_score: float = None) -> WorkoutPlan:
    """
    Generates a basic workout plan based on user's profile.
    Optionally adjusts based on calibration score if provided.
    """
    # For demonstration: choose workouts based simply on weight and height ratio.
    ratio = profile.weight / profile.height
    if calibration_score and calibration_score > 50:
        # Advanced plan if calibration score is high
        exercises = ["HIIT", "Weighted Squats", "Bench Press", "Pull-Ups"]
        duration = 60
    elif ratio > 1:
        exercises = ["Jogging", "Push-Ups", "Plank", "Light Dumbbell Circuit"]
        duration = 45
    else:
        exercises = ["Walking", "Bodyweight Squats", "Stretching"]
        duration = 30

    return WorkoutPlan(exercises=exercises, duration=duration)