import json
import os

DB_FILE = "db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user(user_id):
    db = load_db()
    return db.get(str(user_id), None)

def save_user(user_id, data):
    db = load_db()
    db[str(user_id)] = data
    save_db(db)
