from fastapi import FastAPI
from app.database.connection import engine, Base
from app.routes.user import router as user_router
from app.models import user
from app.models import task
from app.routes.task import router as task_router
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(task_router)

@app.get("/")
def read_root():
    return {"message": "Backend is running successfully"}


#from fastapi import FastAPI

#app = FastAPI()

#@app.get("/")
#async def root():
 #   return {"message": "Hello"}

#@app.get("/health")
#async def health():
 #   return {
  #      "status": "healthy"
   # }
