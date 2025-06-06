from backend.resources.auth import UserRegisterResource, UserLoginResource, UserTakeResource
from backend.resources.taskResource import CreateTasks, ChangeTaskResource, AssignTaskResource,\
    ChangeTaskStatusResource, TaskStatusesResource

routes = (
    (UserRegisterResource, '/register'),
    (UserLoginResource, '/login'),
    (CreateTasks, '/tasks'),
    (ChangeTaskResource, '/tasks/<task_id>'),
    (AssignTaskResource, '/tasks/<task_id>/assign'),
    (ChangeTaskStatusResource, '/tasks/<task_id>/status'),
    (UserTakeResource, '/users'),
    (TaskStatusesResource, '/task-statuses')
)


