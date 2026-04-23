from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database.connection import SessionLocal
from app.models.task import Task

router = APIRouter()


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Task
@router.post("/tasks")
def create_task(
    title: str,
    description: str,
    db: Session = Depends(get_db)
):

    task = Task(
        title=title,
        description=description
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "message": "Task created successfully"
    }


# Get All Tasks
@router.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db)
):

    tasks = db.query(Task).all()

    return tasks


# Mark Task Complete
@router.put("/tasks/{task_id}")
def complete_task(
    task_id: int,
    db: Session = Depends(get_db)
):

    task = db.query(Task).filter(
        Task.id == task_id
    ).first()

    if not task:
        return {"error": "Task not found"}

    task.completed = True

    db.commit()

    return {
        "message": "Task completed"
    }


# Overall Productivity
@router.get("/productivity")
def productivity_summary(
    db: Session = Depends(get_db)
):

    total_tasks = db.query(Task).count()

    completed_tasks = db.query(Task).filter(
        Task.completed == True
    ).count()

    if total_tasks == 0:
        productivity_score = 0
    else:
        productivity_score = (
            completed_tasks / total_tasks
        ) * 100

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "productivity_score": productivity_score
    }


# Today's Productivity
@router.get("/productivity/today")
def today_productivity(
    db: Session = Depends(get_db)
):

    today = datetime.utcnow().date()

    tasks = db.query(Task).all()

    today_tasks = [
        task for task in tasks
        if task.created_at.date() == today
    ]

    total_tasks = len(today_tasks)

    completed_tasks = len(
        [task for task in today_tasks if task.completed]
    )

    if total_tasks == 0:
        productivity_score = 0
    else:
        productivity_score = (
            completed_tasks / total_tasks
        ) * 100

    return {
        "date": str(today),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "productivity_score": productivity_score
    }


# Streak System
@router.get("/streak")
def get_streak(
    db: Session = Depends(get_db)
):

    tasks = db.query(Task).all()

    if not tasks:
        return {
            "current_streak": 0,
            "message": "Start completing tasks to build a streak!"
        }

    completed_dates = set()

    for task in tasks:
        if task.completed:
            completed_dates.add(
                task.created_at.date()
            )

    if not completed_dates:
        return {
            "current_streak": 0,
            "message": "Complete tasks to start your streak!"
        }

    today = datetime.utcnow().date()

    streak = 0
    current_day = today

    while current_day in completed_dates:
        streak += 1
        current_day = current_day - timedelta(days=1)

    return {
        "current_streak": streak,
        "message": f"🔥 You're on a {streak}-day streak!"
    }


# Motivation Message System
@router.get("/motivation")
def motivation_message(
    db: Session = Depends(get_db)
):

    today = datetime.utcnow().date()

    tasks = db.query(Task).all()

    today_tasks = [
        task for task in tasks
        if task.created_at.date() == today
    ]

    total_tasks = len(today_tasks)

    completed_tasks = len(
        [task for task in today_tasks if task.completed]
    )

    if total_tasks == 0:
        score = 0
    else:
        score = (
            completed_tasks / total_tasks
        ) * 100

    # Motivation Logic
    if score == 0:
        message = "🚀 Start your day and add tasks!"

    elif score <= 30:
        message = "💪 Don't give up! Keep working!"

    elif score <= 70:
        message = "👍 Good progress! Keep going!"

    else:
        message = "🔥 Excellent work! You're doing great!"

    return {
        "productivity_score": score,
        "message": message
    }
