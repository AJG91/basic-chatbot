from pathlib import Path
import json
import time

def log_output(path, user_text, assistant_text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "time": time.time(),
        "user": user_text,
        "assistant": assistant_text,
    }

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")