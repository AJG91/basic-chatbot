SYSTEM_PROMPT = "You are a helpful assistant."

def build_prompt(message):
    return (
        f"System prompt: {SYSTEM_PROMPT}\n"
        f"User: {message}\n"
        f"Assistant:"
    )

def extract_assistant_reply(text):
    if "Assistant" in text:
        return text.split("Assistant:", 1)[-1].strip()
    return text.split()