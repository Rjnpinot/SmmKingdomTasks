# instagram_manager.py
import os
import time
from instagrapi import Client
from colorama import Fore, init
from config import DATA_DIR, SESSIONS_DIR, MAX_TASKS_PER_ACCOUNT, TASK_EXECUTION_DELAY
from utils_session import load_json, save_json, encrypt_password, decrypt_password, append_log

init(autoreset=True)

ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
os.makedirs(SESSIONS_DIR, exist_ok=True)

class InstagramManager:
    def __init__(self):
        self.accounts = load_json(ACCOUNTS_FILE, default=[])
        for a in self.accounts:
            a.setdefault("tasks_done", 0)
            a.setdefault("status", "idle")
        self.current_index = 0

    def save_accounts(self):
        save_json(ACCOUNTS_FILE, self.accounts)

    def list_accounts(self):
        return [a["username"] for a in self.accounts]

    def add_account(self, username, password):
        token = encrypt_password(password)
        self.accounts.append({
            "username": username,
            "password": token,
            "tasks_done": 0,
            "status": "idle"
        })
        self.save_accounts()
        append_log(f"Account added: {username}")

    def remove_account(self, username):
        self.accounts = [a for a in self.accounts if a["username"] != username]
        self.save_accounts()
        append_log(f"Account removed: {username}")

    def get_next_account(self):
        if not self.accounts:
            return None
        attempts = 0
        n = len(self.accounts)
        while attempts < n:
            acc = self.accounts[self.current_index]
            if acc.get("status") != "blocked" and acc.get("tasks_done", 0) < MAX_TASKS_PER_ACCOUNT:
                return acc
            self.current_index = (self.current_index + 1) % n
            attempts += 1
        return None

    def mark_task_done(self, username):
        for a in self.accounts:
            if a["username"] == username:
                a["tasks_done"] = a.get("tasks_done", 0) + 1
                a["status"] = "idle"
                self.save_accounts()
                append_log(f"Task done by {username} (total {a['tasks_done']})")
                return

    def _login_client(self, username, password_plain, session_file):
        cl = Client()
        try:
            # try to load existing session
            if os.path.exists(session_file):
                try:
                    cl.load_settings(session_file)
                except Exception:
                    pass
            cl.login(username, password_plain)
            try:
                cl.dump_settings(session_file)
            except Exception:
                pass
            return cl
        except Exception as e:
            append_log(f"Login error for {username}: {e}")
            raise

    def perform_like(self, username, media_url):
        acc = next((a for a in self.accounts if a["username"] == username), None)
        if not acc:
            raise ValueError("Account not found")
        pwd = decrypt_password(acc["password"])
        session_file = os.path.join(SESSIONS_DIR, f"{username}.json")
        try:
            cl = self._login_client(username, pwd, session_file)
            media_pk = cl.media_pk_from_url(media_url)
            cl.media_like(media_pk)
            append_log(f"Like: {username} -> {media_url}")
            time.sleep(TASK_EXECUTION_DELAY)
            self.mark_task_done(username)
            return True
        except Exception as e:
            append_log(f"perform_like error ({username}): {e}")
            raise

    def perform_follow(self, username, target_username):
        acc = next((a for a in self.accounts if a["username"] == username), None)
        if not acc:
            raise ValueError("Account not found")
        pwd = decrypt_password(acc["password"])
        session_file = os.path.join(SESSIONS_DIR, f"{username}.json")
        try:
            cl = self._login_client(username, pwd, session_file)
            user_id = cl.user_id_from_username(target_username)
            cl.user_follow(user_id)
            append_log(f"Follow: {username} -> {target_username}")
            time.sleep(TASK_EXECUTION_DELAY)
            self.mark_task_done(username)
            return True
        except Exception as e:
            append_log(f"perform_follow error ({username}): {e}")
            raise

    def perform_comment(self, username, media_url, text):
        acc = next((a for a in self.accounts if a["username"] == username), None)
        if not acc:
            raise ValueError("Account not found")
        pwd = decrypt_password(acc["password"])
        session_file = os.path.join(SESSIONS_DIR, f"{username}.json")
        try:
            cl = self._login_client(username, pwd, session_file)
            media_pk = cl.media_pk_from_url(media_url)
            cl.media_comment(media_pk, text)
            append_log(f"Comment: {username} -> {media_url} : {text}")
            time.sleep(TASK_EXECUTION_DELAY)
            self.mark_task_done(username)
            return True
        except Exception as e:
            append_log(f"perform_comment error ({username}): {e}")
            raise

# convenience functions matching original bot.py names

_manager = InstagramManager()

def login_instagram():
    username = input("Nom d'utilisateur Instagram: ").strip()
    password = input("Mot de passe: ").strip()
    _manager.add_account(username, password)
    print(Fore.GREEN + f"[√] Compte {username} ajouté.")

def recover_accounts():
    accounts = _manager.list_accounts()
    if not accounts:
        print(Fore.YELLOW + "Aucun compte trouvé.")
    else:
        print(Fore.CYAN + "Comptes:")
        for u in accounts:
            print("- " + u)

def list_accounts():
    accounts = _manager.list_accounts()
    if not accounts:
        print(Fore.YELLOW + "Aucun compte.")
    else:
        print(Fore.CYAN + "Liste des comptes:")
        for i, u in enumerate(accounts, 1):
            print(f"{i}. {u}")

def delete_account():
    list_accounts()
    username = input("Entrez le nom d'utilisateur à supprimer: ").strip()
    _manager.remove_account(username)
    print(Fore.GREEN + f"[√] Compte supprimé: {username}")

def show_trash():
    trash_file = os.path.join(DATA_DIR, "trash.json")
    trash = load_json(trash_file, default=[])
    if not trash:
        print(Fore.YELLOW + "Corbeille vide.")
        return
    print(Fore.CYAN + "Corbeille:")
    for t in trash:
        print("- " + t.get("username", "unknown"))
