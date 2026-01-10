from pathlib import Path
import json

class ChatMemory:

    def __init__(self):
        self.turns = []

    def add_user(self, text):
        self.turns.append(f"User: {text}")

    def add_assistant(self, text):
        self.turns.append(f"Assistant: {text}")

    def last_n_turns(self, n=6):
        return self.turns[-n:]

    def save(self, path="conversation_state.json"):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            json.dump({"turns": self.turns}, f, ensure_ascii=False, indent=2)

    def load(self, path="conversation_state.json"):
        path = Path(path)

        if not path.exists():
            self.turns = []
            return

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self.turns = data.get("turns", [])