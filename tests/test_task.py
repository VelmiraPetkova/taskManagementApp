import pytest
from werkzeug.exceptions import BadRequest, NotFound

from backend.managers.taskManagers import ManagerTasks
from backend.models.task import TasksModel
from tests.factories import UserFactory


def test_get_tasks_empty(session):
    tasks = ManagerTasks.get_tasks()
    assert tasks == []

def test_get_tasks_with_data(session):
    task = TasksModel(title="Test", description="Test desc")
    session.add(task)
    session.commit()

    tasks = ManagerTasks.get_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test"


def test_create_task_success(session):
    data = {
        "title": "New Task",
        "description": "Task description"
    }
    task = ManagerTasks.create_task(data)
    assert task.id is not None
    assert task.title == data["title"]
    assert task.description == data["description"]

def test_update_task_success(session):
    task = TasksModel(title="Old", description="Old")
    session.add(task)
    session.commit()

    updated = ManagerTasks.update_task(task.id, {
        "title": "New Title",
        "description": "New Desc"
    })

    assert updated.title == "New Title"
    assert updated.description == "New Desc"
    assert updated.updated_on is not None

def test_update_task_not_found(session):
    with pytest.raises(NotFound):
        ManagerTasks.update_task(999, {"title": "Doesn't matter"})


def test_delete_task_success(session):
    task = TasksModel(title="Delete", description="Me")
    session.add(task)
    session.commit()

    response = ManagerTasks.delete_task(task.id)
    assert response == {"message": "Task deleted successfully."}
    assert TasksModel.query.filter_by(id=task.id).first() is None


def test_assign_task_success(session):
    user = UserFactory()
    task = TasksModel(title="Task", description="Assign me")
    session.add(task)
    session.commit()

    result = ManagerTasks.assign_task(task.id, user.id)
    assert result.user_id == user.id

def test_assign_task_invalid_user(session):
    task = TasksModel(title="Task", description="Assign me")
    session.add(task)
    session.commit()

    with pytest.raises(Exception) as exc:
        ManagerTasks.assign_task(task.id, user_id=999)

    assert "Invalid user id" in str(exc.value)

def test_assign_task_not_found(session):
    result = ManagerTasks.assign_task(task_id=999, user_id=1)
    assert result == "Task not found"


def test_change_task_status_success(session):
    task = TasksModel(title="Status", description="Change me")
    session.add(task)
    session.commit()

    updated = ManagerTasks.change_task_status("inProgress", task)
    assert updated.status.name == "inProgress"

def test_change_task_status_invalid(session):
    task = TasksModel(title="Invalid", description="Status")
    session.add(task)
    session.commit()

    response, status_code = ManagerTasks.change_task_status("nonexistent", task)
    assert status_code == 400
    assert "Invalid status" in response["message"]




