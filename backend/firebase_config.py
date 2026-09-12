from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore


# Locate the credentials relative to this file.
credential_path = (
    Path(__file__).resolve().parent / "firebase-service-account.json"
)

# Reuse the default Firebase app if it already exists.
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(str(credential_path))
    firebase_app = firebase_admin.initialize_app(cred)

# Create the Firestore client.
db = firestore.client(app=firebase_app)