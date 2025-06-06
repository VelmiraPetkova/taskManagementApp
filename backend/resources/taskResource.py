from flask import request, jsonify
from flask_restful import Resource

from backend.managers.auth import auth
from backend.managers.taskManagers import ManagerTasks
from backend.models.enums import TaskStatus
from backend.models.task import TasksModel
from backend.schemas.taskSchema import TaskSchema
from backend.utils.decorators import validate_schema


# Create & List Tasks
class CreateTasks(Resource):
    @auth.login_required
    @validate_schema(TaskSchema)
    def post(self):
        data = request.get_json()
        result = ManagerTasks.create_task(data)
        return TaskSchema().dump(result), 201

    @auth.login_required
    def get(self):
        tasks = ManagerTasks.get_tasks()
        return TaskSchema().dump(tasks, many=True)


# GET, PUT, DELETE by Task ID

class ChangeTaskResource(Resource):
    @auth.login_required
    def put(self, task_id):
        data = request.get_json()
        updated_task = ManagerTasks.update_task(task_id, data)
        return TaskSchema().dump(updated_task)

    @auth.login_required
    #@permission_required([UserRole.superUser])
    def delete(self, task_id):
        return ManagerTasks.delete_task(task_id)

# Assign task to a user
class AssignTaskResource(Resource):
    @auth.login_required
    def put(self, task_id):
        data = request.get_json()
        user_id = data.get('user_id')
        if not user_id:
            return {"message": "User not found"}, 404

        task = ManagerTasks.assign_task(task_id, user_id)
        return TaskSchema().dump(task), 200


#  Change task status by ID
class ChangeTaskStatusResource(Resource):
    @auth.login_required
    def put(self, task_id):
        task = TasksModel.query.filter_by(id=task_id).first()
        if not task:
            return "Task not found"

        data = request.get_json()
        new_status = data.get("status")
        if not new_status:
            return {"message": "Missing 'status' in request body"}, 400

        ManagerTasks.change_task_status(new_status, task)
        return {
            "message": "Task status updated",
            "status": task.status.value
        }, 200


class TaskStatusesResource(Resource):
    @auth.login_required
    def get(self):
        statuses = [{"key": status.name, "value": status.value} for status in TaskStatus]
        t = jsonify(statuses)
        return t