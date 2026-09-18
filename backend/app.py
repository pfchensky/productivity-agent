from flask import Flask, render_template, request, redirect,session, jsonify, url_for
from models import Task
from services import TaskService
from firebase_admin import auth
from llm_parser import parse_check_in

app = Flask(__name__)
task_service = TaskService()
app.config["SECRET_KEY"] = "replace-this-with-a-long-random-secret"


# ---------- Page routes  ----------
@app.route("/login")
def login():
    if session.get("user_id"):
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/register")
def register():
    if session.get("user_id"):
        return redirect(url_for("home"))

    return render_template("register.html")

@app.route("/session-login", methods=["POST"])
def session_login():
    data = request.get_json()
    id_token = data.get("idToken")

    if not id_token:
        return jsonify({"error": "Missing Firebase ID token."}), 400

    try:
        decoded_token = auth.verify_id_token(id_token)
    except Exception:
        return jsonify({"error": "Invalid Firebase ID token."}), 401

    session.clear()
    session["user_id"] = decoded_token["uid"]
    session["user_email"] = decoded_token.get("email", "")
    session["user_name"] = decoded_token.get("name", "")
    return jsonify({"success": True})

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/')
def home():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    tasks = task_service.get_all_tasks(user_id)

    return render_template(
        'index.html',
        taskList=tasks,
        user_name=session.get("user_name"),
        user_email=session.get("user_email")
    )


@app.route('/add', methods=['POST'])
def add_task():
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

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
        user_id=user_id,
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
    deleted = task_service.delete_task(task_id,session.get("user_id"))

    if not deleted:
        return "Task not found.", 404

    return redirect('/')

@app.route('/edit/<string:task_id>', methods=['GET'])
def edit_task(task_id):
    task = task_service.get_task_by_id(task_id,session.get("user_id"))

    if task is None:
        return "Task not found.", 404

    return render_template('edit.html', task=task)

@app.route('/update/<string:task_id>', methods=['POST'])
def update_task(task_id):
    task = task_service.get_task_by_id(task_id,session.get("user_id"))

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
        },
        session.get("user_id")
    )

    if updated_task is None:
        return "Task not found.", 404

    return redirect('/')

@app.route('/check-in', methods=['POST'])
def check_in():

    user_id = session.get("user_id")
    selected_task_id = request.form.get("task_id", "").strip()
    check_in_text = request.form.get("user_input", "").strip()

    if not selected_task_id:
        return "Please select a task", 400
    if not user_id:
        return redirect(url_for("login"))
    if not check_in_text:
        return "Check-in text is required", 404


    task = task_service.get_task_by_id(selected_task_id, user_id)

    if not task:
        return "Task not found", 404

    task_context = {
        "name" : task.name,
        "current_progress" : task.progress,
        "importance" : task.importance,
        "deadline" : task.deadline
    }

    parsed_result = parse_check_in(check_in_text, task_context)

    return render_template("check_in_confirmation.html", 
                           task = task, 
                           parsed_result = parsed_result, 
                           check_in_text = check_in_text,
                           )

@app.route("/confirm-task/<task_id>", methods=['POST'])
def confirm_task(task_id):
    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("login"))

    task = task_service.get_task_by_id(task_id, user_id)

    if not task:
        return "Task not found", 404

    progress_value = request.form.get("progress")
    time_remaining = request.form.get("time_remaining")
    importance_signal = request.form.get("importance_signal")
    summary = request.form.get("summary")


    updates = {}

    if progress_value:
        try: 
            updated_progress = int(progress_value)

        except ValueError:
            return "Progress must be a whole number", 400

        if updated_progress >= 0 and updated_progress <= 100:
            updates["progress"] = updated_progress
        else:
            return "Invalid Progress Error", 400


    if importance_signal == "Increased":
        if task.importance == "Low":
            updated_importance = "Medium"

        elif task.importance == "Medium":
            updated_importance = "High"

        else:
            updated_importance = "High"

        updates["importance"] = updated_importance

    task_service.update_task(
        task_id,
        updates,
        user_id
    )

    return redirect(url_for("home"))   


# ---------- Run the application ----------

if __name__ == '__main__':
    app.run(debug=True)