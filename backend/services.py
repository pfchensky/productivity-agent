class TaskService:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def generate_task_id(self):
        task_id = self.next_id
        self.next_id += 1
        return task_id

    def add_task(self, task):
        self.tasks.append(task)
        return task

    def get_all_tasks(self):
        return self.tasks

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task

        return None

    def delete_task(self, task_id):
        task = self.get_task_by_id(task_id)

        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def update_task(self, task_id, data):
        task = self.get_task_by_id(task_id)

        if task is None:
            return None

        if "name" in data:
            task.name = data["name"]

        if "deadline" in data:
            task.deadline = data["deadline"]

        if "importance" in data:
            task.importance = data["importance"]

        if "progress" in data:
            task.progress = data["progress"]

        if "status" in data:
            task.status = data["status"]

        return task