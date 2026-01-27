from pathlib import Path
import json

class ChatMemory:
    """
    A class for managing the memory of the chatbot.
        
    Attributes
    ----------
    turns : list[str]
        Keeps track of the chat context by saving the different instances
        of conversation with the chatbot.
    """
    def __init__(self):
        self.turns = []

    def add_user(self, text: str):
        "Adds the user's text to turns list."
        self.turns.append(f"User: {text}")

    def add_assistant(self, text: str):
        "Adds the Assistant's text to turns list."
        self.turns.append(f"Assistant: {text}")

    def last_n_turns(self, n: int = 6) -> list[str]:
        "Grabs the last n turns in the list."
        return self.turns[-n:]
    
    def clear_memory(self, path: str = "conversation_state.json"):
        """Clears the stored conversation (memory) in turns."""
        self.turns = []
        self.save(path)

    def save(self, path: str = "conversation_state.json"):
        """Saves the conversation state to a JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", encoding="utf-8") as f:
            json.dump({"turns": self.turns}, f, ensure_ascii=False, indent=2)

    def load(self, path: str = "conversation_state.json"):
        """Loads the conversation state from a JSON file and adds it to turns."""
        path = Path(path)

        if not path.exists():
            self.turns = []
            return

        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        self.turns = data.get("turns", [])