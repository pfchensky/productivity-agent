from flask import Flask, render_template, request, redirect
from models import Task
from services import TaskService

app = Flask(__name__)
task_service = TaskService()


# ---------- Page routes  ----------

@app.route('/')
def home():
    tasks = task_service.get_all_tasks()
    return render_template('index.html', taskList=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    name = request.form.get('user_input', '').strip()
    deadline = request.form.get('deadline', '')
    importance = request.form.get('importance', 'Medium')
    status = request.form.get('status', 'Not Started')

    if not name or not deadline:
        return "Task name and deadline are required.", 400

    try:
        progress = int(request.form.get('progress', '0'))
    except ValueError:
        return "Progress must be a whole number.", 400

    if not 0 <= progress <= 100:
        return "Progress must be between 0 and 100.", 400

    if importance not in ['Low', 'Medium', 'High']:
        return "Invalid importance.", 400

    if status not in ['Not Started', 'In Progress', 'Completed']:
        return "Invalid status.", 400

    task = Task(
        task_id=task_service.generate_task_id(),
        name=name,
        deadline=deadline,
        importance=importance,
        progress=progress,
        status=status
    )

    task_service.add_task(task)
    return redirect('/')

@app.route('/delete/<string:task_id>', methods=['POST'])
def delete_task(task_id):
    deleted = task_service.delete_task(task_id)

    if not deleted:
        return "Task not found.", 404

    return redirect('/')

@app.route('/edit/<string:task_id>', methods=['GET'])
def edit_task(task_id):
    task = task_service.get_task_by_id(task_id)

    if task is None:
        return "Task not found.", 404

    return render_template('edit.html', task=task)

@app.route('/update/<string:task_id>', methods=['POST'])
def update_task(task_id):
    task = task_service.get_task_by_id(task_id)

    if task is None:
        return "Task not found.", 404

    name = request.form.get('user_input', '').strip()
    deadline = request.form.get('deadline', '').strip()
    importance = request.form.get('importance', 'Medium')
    status = request.form.get('status', 'Not Started')

    if not name or not deadline:
        return "Task name and deadline are required.", 400

    try:
        progress = int(request.form.get('progress', '0'))
    except ValueError:
        return "Progress must be a whole number.", 400

    if not 0 <= progress <= 100:
        return "Progress must be between 0 and 100.", 400

    if importance not in ['Low', 'Medium', 'High']:
        return "Invalid importance.", 400

    if status not in ['Not Started', 'In Progress', 'Completed']:
        return "Invalid status.", 400

    updated_task = task_service.update_task(
        task_id,
        {
            "name": name,
            "deadline": deadline,
            "importance": importance,
            "progress": progress,
            "status": status
        }
    )

    if updated_task is None:
        return "Task not found.", 404

    return redirect('/')


# ---------- Run the application ----------

if __name__ == '__main__':
    app.run(debug=True)