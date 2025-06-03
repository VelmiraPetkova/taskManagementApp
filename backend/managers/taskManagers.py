from backend.managers.auth import auth
from backend.models.enums import TaskStatus
from backend.models.task import TasksModel

#from models import TasksModel, db
from sqlalchemy.exc import SQLAlchemyError
from flask import abort
from datetime import datetime, timezone

from db import db


class ManagerTasks:
    @staticmethod
    def get_tasks_by_user_id():
        current_user = auth.current_user()
        return TasksModel.query.filter_by(user_id=current_user.id).all()

    @staticmethod
    def create_task(data):
        try:
            task = TasksModel(**data)
            db.session.add(task)
            db.session.commit()
            return task
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(400, description=str(e))

    @staticmethod
    def update_task(task_id, data):
        task = TasksModel.query.filter_by(id=task_id).first()

        if not task:
            abort(404, message="Task not found.")

        allowed_fields = {'title', 'description', 'status', 'user_id'}
        for key, value in data.items():
            if key in allowed_fields:
                setattr(task, key, value)

        task.updated_on = datetime.now(timezone.utc)
        db.session.commit()
        return task

    @staticmethod
    def delete_task(task_id):
        task = TasksModel.query.filter_by(id=task_id).first()
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully."}

    @staticmethod
    def assign_task(task_id, user_id):
        task = TasksModel.query.filter_by(id=task_id).first()
        if not task:
            return None  # или хвърли грешка, ако искаш

        task.user_id = user_id
        db.session.commit()
        return task

    @staticmethod
    def change_task_status(task_id, new_status_str):
        try:
            new_status = TaskStatus[new_status_str]  # Името на Enum члена, не стойността!
        except KeyError:
            abort(400, description=f"Invalid status '{new_status_str}'. Valid values are: {', '.join([s.name for s in TaskStatus])}")

        task = TasksModel.query.filter_by(id=task_id).first()
        task.status = new_status
        db.session.commit()
        return task
