# logger.py

import json
import datetime
from config import LOGS_FILE

def log_event(question, context, answer):
    """
    Logs the question, retrieved context, and the final answer to a JSON file.
    """
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "question": question,
        "retrieved_context": context,
        "final_answer": answer
    }
    
    try:
        with open(LOGS_FILE, 'r+') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=4)
    except FileNotFoundError:
        with open(LOGS_FILE, 'w') as f:
            json.dump([log_entry], f, indent=4)
