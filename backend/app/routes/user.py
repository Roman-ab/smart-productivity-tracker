from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import BaseModel

from app.logger import logger
from app.database.connection import SessionLocal
from app.models.user import User
from app.security import hash_password, verify_password
from app.auth import create_access_token, SECRET_KEY, ALGORITHM
from app.redis_client import r

import json

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

    logger.info(f"New user registered: {user.username}")

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# ---------------- LOGIN ----------------
@router.post("/login")
def login_user(user: UserCreate, db: Session = Depends(get_db)):

    cache_key = f"user:{user.username}"

    # Check Redis cache first
    cached_user = r.get(cache_key)

    if cached_user:
        logger.info(
            f"User login served from Redis cache: {user.username}"
        )

        return {
            "message": "Login successful (cache)",
            "data": json.loads(cached_user)
        }

    # Database lookup
    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        logger.warning(
            f"Login failed - user not found: {user.username}"
        )
        return {"error": "User not found"}

    if not verify_password(
        user.password,
        db_user.password
    ):
        logger.warning(
            f"Login failed - incorrect password for user: {user.username}"
        )
        return {"error": "Incorrect password"}

    # Store user data in Redis for 5 minutes
    r.setex(
        cache_key,
        300,
        json.dumps({
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        })
    )

    logger.info(
        f"User logged in successfully: {user.username}"
    )

    access_token = create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "message": "Login successful",
        "access_token": access_token
    }


# ---------------- DASHBOARD (PROTECTED) ----------------
@router.get("/dashboard")
def dashboard(
    token: str = Header(...),
    db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        cache_key = f"dashboard:{username}"

        # Check Redis first
        cached = r.get(cache_key)

        if cached:
            logger.info(
                f"Dashboard served from Redis cache for user: {username}"
            )

            return {
                "source": "cache",
                "data": json.loads(cached)
            }

        # Database fallback
        user = db.query(User).filter(
            User.username == username
        ).first()

        if not user:
            logger.warning(
                f"Dashboard access failed - user not found: {username}"
            )
            return {"error": "User not found"}

        data = {
            "username": user.username,
            "email": user.email
        }

        # Store in Redis for 10 minutes
        r.setex(
            cache_key,
            600,
            json.dumps(data)
        )

        logger.info(
            f"Dashboard served from PostgreSQL for user: {username}"
        )

        return {
            "source": "database",
            "data": data
        }

    except JWTError:
        logger.warning(
            "Dashboard access failed - invalid token"
        )

        return {
            "error": "Invalid token"
        }