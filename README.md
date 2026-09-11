# Productivity Agent

A task management app built with Flask and Firestore.

## Features

- Add, view, and delete tasks through the web interface.
- Create, read, update, and delete tasks through JSON APIs.
- Save tasks in Firestore.

## 1. Clone the Repository

```bash
git clone https://github.com/pfchensky/productivity-agent.git
cd productivity-agent/backend
```

## 2. Set Up the Python Environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Activate the virtual environment whenever you open a new terminal.

## 3. Configure Firebase

Ask the project maintainer for Firebase access and development credentials.

Place your service account JSON file at:

```text
backend/firebase-service-account.json
```

Ensure the Firebase project has a Cloud Firestore database.

Do not commit the credentials or `.venv` folder to GitHub.

## 4. Run the App

Run from the `backend` folder with the virtual environment activated:

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser.

Press `Ctrl+C` to stop the server.

## Project Structure

| Path | Purpose |
| --- | --- |
| `backend/app.py` | Flask application and routes |
| `backend/models.py` | Task model |
| `backend/services.py` | Firestore task operations |
| `backend/firebase_config.py` | Firebase configuration |
| `backend/requirements.txt` | Python dependencies |
| `backend/templates/` | HTML pages |
| `backend/static/` | CSS and static assets |