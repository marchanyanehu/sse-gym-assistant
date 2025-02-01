from fastapi import FastAPI
from backend.app.routers import auth_route, user_route, calibration_route, profile_route
from backend.app.utils.database import engine
from .models.base_model import Base
from fastapi.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_route.router)
app.include_router(auth_route.router)
app.include_router(profile_route.router)
app.include_router(calibration_route.router)

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="localhost", port=8000, reload=True)