from backend.models.enums import TaskStatus
from backend.models.task import TasksModel

#from models import TasksModel, db
from sqlalchemy.exc import SQLAlchemyError
from flask import abort
from datetime import datetime, timezone

from backend.models.user import UserModel
from db import db


class ManagerTasks:
    @staticmethod
    def get_tasks():
        return TasksModel.query.all()

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
            abort(404, description="Task not found.")

        allowed_fields = {'title', 'description'}
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
            return "Task not found"

        try:
            valid_user = UserModel.query.filter_by(id=user_id).first()
            task.user_id = valid_user.id
            db.session.commit()
            return task
        except Exception as ex:
            raise Exception("Invalid user id")


    @staticmethod
    def change_task_status(new_status, task):
        status_lookup = {status.name: status for status in TaskStatus}

        if new_status in status_lookup:
            task.status = status_lookup[new_status]  # подаваме enum, не string
        else:
            return {"message": f"Invalid status: {new_status}"}, 400

        db.session.commit()
        return task
