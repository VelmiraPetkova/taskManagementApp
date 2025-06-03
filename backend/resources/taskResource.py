from flask import request
from flask_restful import Resource

from backend.managers.auth import auth
from backend.managers.taskManagers import ManagerTasks
from backend.models.enums import UserRole, TaskStatus
from backend.models.task import TasksModel
from backend.schemas.taskSchema import TaskSchema
from backend.utils.decorators import validate_schema, permission_required


# GET all, POST new task
class CreateTasks(Resource):
    @auth.login_required
    @validate_schema(TaskSchema)
    def post(self):
        data = request.get_json()
        result = ManagerTasks.create_task(data)
        return TaskSchema().dump(result),201

    # Get all tasks assigned to user
    @auth.login_required
    def get(self):
        tasks = ManagerTasks.get_tasks_by_user_id()
        return TaskSchema().dump(tasks, many=True)


 # GET, PUT, DELETE by Task ID
class ChangeTaskResource(Resource):
    @auth.login_required
    def get(self, task_id):
        task = TasksModel.query.filter_by(id=task_id).first()
        return TaskSchema().dump(task)

    @auth.login_required
    def put(self, task_id):
        data = request.get_json()
        updated_task = ManagerTasks.update_task(task_id, data)
        return TaskSchema().dump(updated_task)

    @auth.login_required
    @permission_required([UserRole.superUser])
    def delete(self, task_id):
        return ManagerTasks.delete_task(task_id)


# Assign task to user
class AssignTaskResource(Resource):
    @auth.login_required
    def post(self, task_id):
        data = request.get_json()  # взимаме user_id от body
        user_id = data.get('user_id')
        if not user_id:
            return {"message": "user_id is required"}, 400

        task = ManagerTasks.assign_task(task_id, user_id)
        return TaskSchema().dump(task), 200


class UserTasksResource(Resource):
    @auth.login_required
    def get(self, user_id):
        tasks = TasksModel.query.filter_by(user_id=user_id).all()
        return TaskSchema(many=True).dump(tasks), 200


class ChangeTaskStatusResource(Resource):
    @auth.login_required
    def patch(self, task_id):
        task = TasksModel.query.get(task_id)
        if not task:
            return {"message": "Task not found"}, 404

        data = request.get_json()
        new_status = data.get("status")

        try:
            task.status = TaskStatus[new_status].value  # Пример: "inProgress"
        except KeyError:
            return {"message": f"Invalid status: {new_status}"}, 400

        db.session.commit()
        return {"message": "Task status updated", "status": task.status}, 200