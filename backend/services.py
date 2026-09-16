from google.api_core.exceptions import NotFound

from firebase_config import db
from models import Task


class TaskService:
    def __init__(self):
        self.collection = db.collection("tasks")

    def generate_task_id(self):
        # Generate a document ID without writing to Firestore.
        return self.collection.document().id

    def add_task(self, task):
        self.collection.document(task.task_id).set(task.to_dict())
        return task

    def get_all_tasks(self,user_id):
        tasks = []
        query = self.collection.where("user_id", "==", user_id)

        for document in query.stream():
            data = document.to_dict()
            data["task_id"] = document.id
            tasks.append(Task(**data))

        return tasks

    def get_task_by_id(self, task_id,user_id):
        document = self.collection.document(task_id).get()

        if not document.exists:
            return None

        data = document.to_dict()
        if data.get("user_id") != user_id:
            return None

        data["task_id"] = document.id
        return Task(**data)

    def delete_task(self, task_id, user_id):
        task = self.get_task_by_id(task_id, user_id)

        if task is None:
            return False

        self.collection.document(task_id).delete()
        return True

    def update_task(self, task_id, data,user_id):
        task = self.get_task_by_id(task_id, user_id)

        if task is None:
            return None

        allowed_fields = {
            "name", "deadline", "importance", "progress", "status"
        }
        updates = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        if not updates:
            return task

        try:
            self.collection.document(task_id).update(updates)
        except NotFound:
            return None

        return self.get_task_by_id(task_id, user_id)