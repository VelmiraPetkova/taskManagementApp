import uuid

from sqlalchemy import func, BINARY
from sqlalchemy.orm import Mapped, mapped_column

from db import  db

from backend.models.enums import UserRole


class UserModel(db.Model):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(100), nullable=False, unique=False)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        db.Enum(UserRole), default=UserRole.employee.name, nullable=False
    )
