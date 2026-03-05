import json
import bcrypt

USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE,"r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE,"w") as f:
        json.dump(users,f)

def register(username,password):

    users = load_users()

    if username in users:
        return False

    hashed = bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

    users[username] = hashed
    save_users(users)

    return True

def login(username,password):

    users = load_users()

    if username not in users:
        return False

    stored = users[username].encode()

    return bcrypt.checkpw(password.encode(),stored)
