from typing import Union
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
    Docstring for MyAssistant
    """
    bot = MyChat(model, n_turns, state_dir, log_dir)
    demo = chat_interface(bot)
    demo.launch(share=share, inline=inline)

class MyChat():
    """
    Docstring for MyChat
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
        user_message, 
        chat_history
    ) -> Union[list, str]:
        """
        Docstring for respond
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
    
    def clear_chat(self):
        self.memory.clear_memory(self.state_path)
        log_output(self.log_path, "Memory cleared", "")
        return []
