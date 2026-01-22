SYSTEM_PROMPT = "You are a helpful assistant."

def build_prompt(user_message: str) -> str:
    """Builds the output prompt template for the chatbot."""
    return (
        f"System prompt: {SYSTEM_PROMPT}\n"
        f"User: {user_message}\n"
        f"Assistant:"
    )

def build_prompt_with_history(
    history_turns: list[str], 
    user_message: str
)-> str:
    """Builds the output prompt template for the chatbot with previous history."""
    history_text = "\n".join(history_turns)
    if history_text.strip():
        return (
            f"System prompt: {SYSTEM_PROMPT}\n"
            f"{history_text}\n"
            f"User: {user_message}\n"
            f"Assistant:"
        )
    else:
        return build_prompt(user_message)

def extract_assistant_reply(text: str) -> str:
    """Extracts the chatbot's reply."""
    if "Assistant" in text:
        return text.rsplit("Assistant:", 1)[-1].strip()
    return text.strip()