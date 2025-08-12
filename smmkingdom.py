# smmkingdom.py
import time
from utils_session import append_log

def fetch_tasks_simulated():
    append_log("Fetching tasks (simulated)")
    time.sleep(1)
    tasks = [
        {"id": "t1", "type": "like", "target": "https://www.instagram.com/p/CFake1/"},
        {"id": "t2", "type": "comment", "target": "https://www.instagram.com/p/CFake2/", "text": "Nice!"},
        {"id": "t3", "type": "follow", "target": "example_user"}
    ]
    return tasks

def report_task_result_simulated(task_id, success, msg=""):
    append_log(f"Report {task_id}: success={success} msg={msg}")
    return True
