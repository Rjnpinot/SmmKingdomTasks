# task_handler.py
from instagram_manager import InstagramManager
from smmkingdom import fetch_tasks_simulated, report_task_result_simulated
from utils_session import append_log
from colorama import Fore

class TaskHandler:
    def __init__(self):
        self.ig = InstagramManager()

    def run_once(self):
        tasks = fetch_tasks_simulated()
        if not tasks:
            print(Fore.YELLOW + "Aucune tâche.")
            return

        for t in tasks:
            task_id = t.get("id")
            ttype = t.get("type")
            target = t.get("target")
            text = t.get("text", "")
            success = False
            message = ""

            acc = self.ig.get_next_account()
            if not acc:
                message = "No available accounts"
                append_log(message)
                print(Fore.RED + message)
                report_task_result_simulated(task_id, False, message)
                continue

            username = acc["username"]
            print(Fore.CYAN + f"Executing {ttype} using {username} on {target}")

            try:
                if ttype == "like":
                    self.ig.perform_like(username, target)
                elif ttype == "follow":
                    self.ig.perform_follow(username, target)
                elif ttype == "comment":
                    self.ig.perform_comment(username, target, text)
                else:
                    raise ValueError("Unknown task type")
                success = True
                message = "OK"
                # rotate
                self.ig.current_index = (self.ig.current_index + 1) % max(1, len(self.ig.accounts))
            except Exception as e:
                message = str(e)
                append_log(f"Task error {task_id}: {message}")
                # rotate on failure
                self.ig.current_index = (self.ig.current_index + 1) % max(1, len(self.ig.accounts))

            report_task_result_simulated(task_id, success, message)
            print(Fore.GREEN + f"Task {task_id}: {message}")
