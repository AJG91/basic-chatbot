class ChatMemory:

    def __init__(self):
        self.turns = []

    def add_user(self, text):
        self.turns.append(f"User: {text}")

    def add_assistant(self, text):
        self.turns.append(f"Assistant: {text}")

    def last_n_turns(self, n=6):
        return self.turns[-n:]