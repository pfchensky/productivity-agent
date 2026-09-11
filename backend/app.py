from flask import Flask, render_template, request, redirect, jsonify
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

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    deleted = task_service.delete_task(task_id)

    if not deleted:
        return "Task not found.", 404

    return redirect('/')


# ---------- API input validation ----------

def validate_task_data(data, partial=False):
    if not isinstance(data, dict) or not data:
        return "A non-empty JSON object is required."

    required_fields = ['name', 'deadline', 'importance']

    if not partial:
        for field in required_fields:
            if field not in data:
                return f"{field} is required."

    for field in ['name', 'deadline']:
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                return f"{field} must be a non-empty string."

    if 'importance' in data:
        if data['importance'] not in ['Low', 'Medium', 'High']:
            return "Invalid importance."

    if 'progress' in data:
        progress = data['progress']
        if type(progress) is not int or not 0 <= progress <= 100:
            return "Progress must be a whole number between 0 and 100."

    if 'status' in data:
        if data['status'] not in ['Not Started', 'In Progress', 'Completed']:
            return "Invalid status."

    allowed_fields = {'name', 'deadline', 'importance', 'progress', 'status'}
    if any(field not in allowed_fields for field in data):
        return "Request contains unsupported fields."

    return None


# ---------- JSON API routes ----------

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        "status": "ok",
        "message": "Productivity Agent backend is running"
    }), 200


@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    data = request.get_json(silent=True)

    error = validate_task_data(data)
    if error:
        return jsonify({"error": error}), 400

    task = Task(
        task_id=task_service.generate_task_id(),
        name=data['name'].strip(),
        deadline=data['deadline'],
        importance=data['importance'],
        progress=data.get('progress', 0),
        status=data.get('status', 'Not Started')
    )

    task_service.add_task(task)

    return jsonify({
        "message": "Task added successfully",
        "task": task.to_dict()
    }), 201


@app.route('/api/tasks', methods=['GET'])
def api_get_tasks():
    tasks = task_service.get_all_tasks()

    return jsonify([
        task.to_dict() for task in tasks
    ]), 200


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def api_get_task(task_id):
    task = task_service.get_task_by_id(task_id)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_dict()), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    deleted = task_service.delete_task(task_id)

    if not deleted:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


@app.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def api_update_task(task_id):
    data = request.get_json(silent=True)

    error = validate_task_data(data, partial=True)
    if error:
        return jsonify({"error": error}), 400

    if 'name' in data:
        data['name'] = data['name'].strip()

    task = task_service.update_task(task_id, data)

    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "message": "Task updated successfully",
        "task": task.to_dict()
    }), 200


# ---------- Run the application ----------

if __name__ == '__main__':
    app.run(debug=True)