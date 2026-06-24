from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database.connection import SessionLocal
from app.models.user import User
from app.security import hash_password, verify_password
from app.auth import create_access_token, SECRET_KEY, ALGORITHM
from pydantic import BaseModel

router = APIRouter()


# ---------------- DB Dependency ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- Pydantic Schema ----------------
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# ---------------- REGISTER ----------------
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# ---------------- LOGIN ----------------
@router.post("/login")
def login_user(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Incorrect password"}

    token = create_access_token(data={"sub": db_user.username})

    return {
        "message": "Login successful",
        "access_token": token
    }


# ---------------- DASHBOARD (PROTECTED) ----------------
@router.get("/dashboard")
def dashboard(token: str = Header(...)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        return {"message": f"Welcome {username}"}

    except JWTError:
        return {"error": "Invalid token"}