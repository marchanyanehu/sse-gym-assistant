# language: python
import os
import json
import openai

from backend.app.schemas.workout_schema import WorkoutPlan, ExercisePlan
from backend.app.models.profile_model import Profile

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_workout_plan(
    profile: Profile, 
    calibration_score: float = None, 
    goal: str = "build endurance"
) -> WorkoutPlan:
    """
    Generates a detailed workout plan including sets, reps, rest between sets, 
    and overall rest time (in hours) between training sessions.
    Goal options: "weightloss (with muscle preservence)", "weightloss (without muscle preservence)",
    "build muscles", "build strength", "build endurance"
    """
    ratio = profile.weight / profile.height
    if calibration_score and calibration_score > 50:
        fallback_exercises = [
            ExercisePlan(name="HIIT", sets=4, reps=12, rest_between_sets=90),
            ExercisePlan(name="Weighted Squats", sets=3, reps=10, rest_between_sets=120),
            ExercisePlan(name="Bench Press", sets=3, reps=8, rest_between_sets=120),
            ExercisePlan(name="Pull-Ups", sets=3, reps=8, rest_between_sets=120)
        ]
        fallback_rest = 24.0
    elif ratio > 1:
        fallback_exercises = [
            ExercisePlan(name="Jogging", sets=1, reps=1, rest_between_sets=0),
            ExercisePlan(name="Push-Ups", sets=4, reps=15, rest_between_sets=60),
            ExercisePlan(name="Plank", sets=3, reps=1, rest_between_sets=60),
            ExercisePlan(name="Light Dumbbell Circuit", sets=3, reps=12, rest_between_sets=90)
        ]
        fallback_rest = 18.0
    else:
        fallback_exercises = [
            ExercisePlan(name="Walking", sets=1, reps=1, rest_between_sets=0),
            ExercisePlan(name="Bodyweight Squats", sets=3, reps=15, rest_between_sets=60),
            ExercisePlan(name="Stretching", sets=1, reps=1, rest_between_sets=0)
        ]
        fallback_rest = 12.0

    prompt = (
        f"Generate a detailed workout plan for a {profile.sex} with a height of {profile.height} "
        f"and weight of {profile.weight}. The calibration score is {calibration_score}. "
        f"The fitness goal is '{goal}'. Return a JSON object with two keys: "
        f"'exercises' as a list of objects (each containing 'name', 'sets', 'reps', and 'rest_between_sets' in seconds) "
        f"and 'rest_time_hours' as a float indicating the rest time in hours between training sessions."
    )

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            temperature=0.7,
            n=1
        )
        result = response.choices[0].text.strip()
        api_plan = json.loads(result)
        # Map API exercises to ExercisePlan, fall back if key missing
        exercises = [
            ExercisePlan(
                name=ex.get("name", fb.name),
                sets=ex.get("sets", fb.sets),
                reps=ex.get("reps", fb.reps),
                rest_between_sets=ex.get("rest_between_sets", fb.rest_between_sets)
            )
            for ex, fb in zip(api_plan.get("exercises", []), fallback_exercises)
        ] if api_plan.get("exercises") else fallback_exercises
        rest_time_hours = api_plan.get("rest_time_hours", fallback_rest)
    except Exception:
        exercises = fallback_exercises
        rest_time_hours = fallback_rest

    return WorkoutPlan(exercises=exercises, rest_time_hours=rest_time_hours)