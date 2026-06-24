from fastapi import FastAPI

from app.database.connection import engine, Base
from app.routes.user import router as user_router
from app.routes.task import router as task_router

app = FastAPI()


# ---------------- Create DB tables ----------------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# ---------------- Root ----------------
@app.get("/")
def read_root():
    return {"message": "Backend is running successfully"}


# ---------------- Routers ----------------
app.include_router(user_router)
app.include_router(task_router)
  
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "smart-productivity-tracker"
    }
