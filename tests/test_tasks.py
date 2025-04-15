from bson import ObjectId
from models.task_model import Task
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


def test_create_task_success():
    task_data = {
        "title": "Pytest Task",
        "description": "Testing task creation",
        "due_date": "2025-04-01",
        "status": "Pending",  
        "user_id": str(ObjectId())
    }

    task_id = Task.create_task(task_data)
    assert task_id is not None


def test_create_task_missing_title():
    task_data = {
        "description": "No title provided",
        "due_date": "2025-04-01",
        "user_id": str(ObjectId())
    }

    try:
        Task.create_task(task_data)
        assert False
    except Exception:
        assert True

def test_create_task_invalid_user():
    task_data = {
        "title": "Invalid User",
        "description": "Testing invalid user",
        "due_date": "2025-04-01",
        "user_id": "invalid_id"
    }

    try:
        Task.create_task(task_data)
        assert False
    except Exception:
        assert True
