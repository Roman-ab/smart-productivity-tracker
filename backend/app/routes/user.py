from app.auth import create_access_token
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.user import User
from app.security import hash_password, verify_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register_user(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    hashed_password = hash_password(password)

    user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        return {"error": "User not found"}

    if not verify_password(
        password,
        user.password
    ):
        return {"error": "Incorrect password"}

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "message": "Login successful",
        "access_token": access_token
    }
from fastapi import Header
from jose import JWTError, jwt
from app.auth import SECRET_KEY, ALGORITHM


@router.get("/dashboard")
def dashboard(token: str = Header(...)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        return {
            "message": f"Welcome {username}"
        }

    except JWTError:
        return {"error": "Invalid token"}
