class Task:
    def __init__(
        self,
        task_id,
        user_id,
        name,
        deadline,
        importance,
        progress=0,
        status="Not Started"
    ):
        self.task_id = task_id
        self.user_id = user_id
        self.name = name
        self.deadline = deadline
        self.importance = importance
        self.progress = progress
        self.status = status

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "name": self.name,
            "user_id": self.user_id,
            "deadline": self.deadline,
            "importance": self.importance,
            "progress": self.progress,
            "status": self.status
        }