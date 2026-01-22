from pathlib import Path
import json
import time

def log_output(path: str, user_text: str, assistant_text: str):
    """Logs the time, user's input, and chatbot's output to a JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "time": time.time(),
        "user": user_text,
        "assistant": assistant_text,
    }

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")