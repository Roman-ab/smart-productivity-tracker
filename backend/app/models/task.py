from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from app.database.connection import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)

    description = Column(String)

    completed = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
