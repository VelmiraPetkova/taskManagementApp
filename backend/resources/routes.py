from backend.resources.auth import UserRegisterResource, UserLoginResource
from backend.resources.taskResource import CreateTasks, ChangeTaskResource, AssignTaskResource, UserTasksResource, \
    ChangeTaskStatusResource

routes = (
    (UserRegisterResource, '/register'),
    (UserLoginResource, '/login'),
    (CreateTasks, '/tasks'),
    (ChangeTaskResource, '/tasks/<uuid:task_id>'),
    (AssignTaskResource, '/tasks/<task_id>/assign'),
    (ChangeTaskStatusResource, '/tasks/<uuid:task_id>/status'),
    (UserTasksResource, '/users/<uuid:user_id>/tasks'),
)
