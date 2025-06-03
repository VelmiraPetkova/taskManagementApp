import uuid
from datetime import datetime,timezone

from sqlalchemy import func, ForeignKey, BINARY
from sqlalchemy.orm import Mapped, mapped_column, relationship



from db import  db

from backend.models.enums import TaskStatus
from backend.models.user import UserModel


class TasksModel(db.Model):
    __tablename__ = 'tasks'
    id: Mapped[str] = mapped_column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    updated_on: Mapped[datetime] = mapped_column(onupdate=func.now(), default=datetime.now(timezone.utc))
    status:Mapped[TaskStatus] = mapped_column(
        db.Enum(TaskStatus), default = TaskStatus.notStarted.name, nullable=False
    )

    user_id: Mapped[str] = mapped_column(db.String(36), ForeignKey('users.id'), nullable=True)