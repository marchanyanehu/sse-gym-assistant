from fastapi import FastAPI
from backend.app.routers import user
from backend.app.utils.database import engine
from .models.base import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Gym Assistant API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="localhost", port=8000, reload=True)