import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Get the directory where this file is located
BACKEND_DIR = Path(__file__).resolve().parent

# Path to service account key
cred_path = os.getenv("FIREBASE_CREDENTIALS") or BACKEND_DIR / "serviceAccountKey.json"

db = None
if Path(cred_path).exists():
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    print(f"Warning: Firebase credentials not found at {cred_path}")
