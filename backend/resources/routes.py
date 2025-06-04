from backend.resources.auth import UserRegisterResource, UserLoginResource
from backend.resources.taskResource import CreateTasks, ChangeTaskResource, AssignTaskResource, UserTasksResource, \
    ChangeTaskStatusResource, TaskStatusesResource

routes = (
    (UserRegisterResource, '/register'),
    (UserLoginResource, '/login'),
    (CreateTasks, '/tasks'),
    (ChangeTaskResource, '/tasks/<task_id>'),
    (AssignTaskResource, '/tasks/<task_id>/assign'),
    (ChangeTaskStatusResource, '/tasks/<task_id>/status'),
    (UserTasksResource, '/users/<user_id>/tasks'),
    (TaskStatusesResource, '/task-statuses')
)


