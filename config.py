# config.py
import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")
ADMIN_TELEGRAM_ID = os.environ.get("ADMIN_TELEGRAM_ID")  # facultatif

# Dossiers et limites
DATA_DIR = "data"
SESSIONS_DIR = "sessions"   # utilisé par instagrapi dump/load (optionnel)
LOGS_DIR = "logs"

MAX_TASKS_PER_ACCOUNT = 100
TASK_EXECUTION_DELAY = 2  # seconds

# Fernet key file (for encrypting passwords)
FERNET_KEY_FILE = os.path.join(DATA_DIR, "fernet.key")
