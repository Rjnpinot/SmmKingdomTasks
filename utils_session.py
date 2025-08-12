# utils_session.py
import os
import json
from cryptography.fernet import Fernet
import datetime
from config import DATA_DIR, LOGS_DIR, FERNET_KEY_FILE

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

def ensure_fernet_key():
    if not os.path.exists(FERNET_KEY_FILE):
        key = Fernet.generate_key()
        with open(FERNET_KEY_FILE, "wb") as f:
            f.write(key)
        return key
    with open(FERNET_KEY_FILE, "rb") as f:
        return f.read()

FERNET_KEY = ensure_fernet_key()
fernet = Fernet(FERNET_KEY)

def encrypt_password(pw: str) -> str:
    return fernet.encrypt(pw.encode()).decode()

def decrypt_password(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()

def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path: str, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default if default is not None else []

def append_log(msg: str):
    ts = datetime.datetime.now().isoformat()
    line = f"[{ts}] {msg}\n"
    with open(os.path.join(LOGS_DIR, "log.txt"), "a", encoding="utf-8") as f:
        f.write(line)
