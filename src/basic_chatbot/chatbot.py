from basic_chatbot.model_local import LocalLM
from basic_chatbot.model_openai import OpenAIChat
from basic_chatbot.memory import ChatMemory
from basic_chatbot.gradio_ui import chat_interface
from basic_chatbot.logging import log_output
from basic_chatbot.prompt_utils import build_prompt_with_history, extract_assistant_reply

def MyAssistant(
    model: str, 
    n_turns: int, 
    state_dir: str, 
    log_dir: str, 
    share: bool = False, 
    inline: bool = True
):
    """
    Wrapper for the `MyChat` class and `chat_interface` function.
    Creates an instance of `MyChat` and launches a Gradio UI.

    Parameters
    ----------
    model : str
        Name of model that will be loaded.
    n_turns : int
        Number of chat instances saved for context.
    state_dir : str
        Directory where the conversation state is saved.
    log_dir : str
        Directory where the conversation log is saved.
    share : bool, optional (default=False)
        Creates a shareable link if set to True.
    inline : bool, optional (default=True)
        Opens Gradio UI inline if set to True.
        Otherwise, opens a new window for UI.
    """
    bot = MyChat(model, n_turns, state_dir, log_dir)
    demo = chat_interface(bot)
    demo.launch(share=share, inline=inline)

class MyChat():
    """
        
    Attributes
    ----------
    lm : LocalLM | OpenAIChat
        Model that will be used for the chatbot.
    memory : ChatMemory
        A class used to keep track of the chatbot's memory.
    n_turns : int
        Number of chat instances saved for context.
    state_path : str
        Path to directory where the conversation state is saved.
    log_path : str
        Path to directory where the log state is saved.

    Parameters
    ----------
    model_name : str
        Name of model that will be loaded.
    n_turns : int
        Number of chat instances saved for context.
    state_dir : str
        Directory where the conversation state is saved.
    log_dir : str
        Directory where the conversation log is saved.
    state_fname : str, optional (default="conversation_state.json")
        Name of conversation state JSON file.
    log_fname : str, optional (default="chat_logs.jsonl")
        Name of conversation log JSON file.
    """
    def __init__(
        self, 
        model_name: str, 
        n_turns: int,
        state_dir: str,
        log_dir: str,
        state_fname: str = "conversation_state.json",
        log_fname: str = "chat_logs.jsonl"
    ):
        if "openai" in model_name.lower():
            self.lm = OpenAIChat()
        else:
            self.lm = LocalLM(model_name)

        state_path = state_dir + state_fname
        log_path = log_dir + log_fname

        self.memory = ChatMemory()
        self.memory.load(state_path)

        self.n_turns = n_turns
        self.state_path = state_path
        self.log_path = log_path

    def chat(
        self, 
        user_message: str
    ) -> str:
        """
        Generates an output from the language model using previous `n_turns`.
        The user message and model response is then passed into the memory class.

        Parameters
        ----------
        user_message : str
            The message from the user.
        """
        prompt = build_prompt_with_history(
            self.memory.last_n_turns(self.n_turns), 
            user_message
        )
        text = self.lm.generate_text(prompt)
        reply = extract_assistant_reply(text)
        
        self.memory.add_user(user_message)
        self.memory.add_assistant(reply)
        return reply
    
    def respond(
        self,
        user_message: str, 
        chat_history: list | None
    ) -> tuple[list, str]:
        """
        Wrapper for `chat` method.
        Generates a response from the language model using `user_text` input.
        Saves the conversation and log state of the chatbot to directory.

        Parameters
        ----------
        user_message : str
            The message from the user.
        chat_history : list or None

        Returns
        -------
        tuple[list, str]
            Chat history and an empty string.
        """
        if chat_history is None:
            chat_history = []

        chat_history.append({"role": "user", "content": user_message})

        try:
            reply = str(self.chat(user_message))
        except Exception as e:
            reply = f"[ERROR] {type(e).__name__}: {e}"

        log_output(self.log_path, user_message, reply)
        self.memory.save(self.state_path)
        chat_history.append({"role": "assistant", "content": reply})
        return chat_history, ""
    
    def clear_chat(self) -> list:
        "Clears chat memory and returns empty list."
        self.memory.clear_memory(self.state_path)
        log_output(self.log_path, "Memory cleared", "")
        return []
