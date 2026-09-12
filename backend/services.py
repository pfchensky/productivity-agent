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

    def get_all_tasks(self):
        tasks = []

        for document in self.collection.stream():
            data = document.to_dict()
            data["task_id"] = document.id
            tasks.append(Task(**data))

        return tasks

    def get_task_by_id(self, task_id):
        document = self.collection.document(task_id).get()

        if not document.exists:
            return None

        data = document.to_dict()
        data["task_id"] = document.id
        return Task(**data)

    def delete_task(self, task_id):
        document_ref = self.collection.document(task_id)

        if not document_ref.get().exists:
            return False

        document_ref.delete()
        return True

    def update_task(self, task_id, data):
        document_ref = self.collection.document(task_id)

        allowed_fields = {
            "name", "deadline", "importance", "progress", "status"
        }
        updates = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        if not updates:
            return self.get_task_by_id(task_id)

        try:
            document_ref.update(updates)
        except NotFound:
            return None

        return self.get_task_by_id(task_id)