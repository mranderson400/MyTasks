from bson import ObjectId
from config.database import tasks_collection, users_collection

from config.database import tasks_collection

class Task:
    @classmethod
    def create_task(cls, data):
        task_data = {
            "title": data["title"],
            "description": data["description"],
            "status": data["status"],
            "due_date": data["due_date"],
            "user_id": ObjectId(data["user_id"]),
        }
        result = tasks_collection.insert_one(task_data)
        return str(result.inserted_id)

    @classmethod
    def get_all(cls, user_id):
        tasks_cursor = tasks_collection.find({"user_id": ObjectId(user_id)})
        tasks = list(tasks_cursor)

        for task in tasks:
            task["_id"] = str(task["_id"])
            task["user_id"] = str(task["user_id"])
            
            # Add `creator` like in the old project
            user = users_collection.find_one({"_id": ObjectId(task["user_id"])})
            if user:
                task["creator"] = {
                    "first_name": user.get("first_name", ""),
                    "email": user.get("email", "")
                }
        

        return tasks

    @classmethod
    def get_one(cls, task_id):
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            task["_id"] = str(task["_id"])
            task["user_id"] = str(task["user_id"])
        return task

    @classmethod
    def delete(cls, task_id):
        return tasks_collection.delete_one({"_id": ObjectId(task_id)})

    @classmethod
    def update(cls, task_id, data):
        updated_data = {
            "title": data["title"],
            "description": data["description"],
            "due_date": data["due_date"],
            "status": data["status"]
        }
        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": updated_data}
        )
        return result.modified_count > 0
