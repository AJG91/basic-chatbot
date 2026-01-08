from typing import Union
from basic_chatbot.model_local import LocalLM
from basic_chatbot.model_openai import OpenAIChat
from basic_chatbot.memory import ChatMemory
from basic_chatbot.prompt_utils import build_prompt_with_history, extract_assistant_reply

class MyChat():
    """
    Docstring for MyChat
    """
    def __init__(
        self, 
        model_name, 
        n_turns
    ):
        if "openai" in model_name.lower():
            self.lm = OpenAIChat()
        else:
            self.lm = LocalLM(model_name)

        self.memory = ChatMemory()
        self.n_turns = n_turns

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
        reply = str(self.chat(user_message))

        if chat_history is None:
            chat_history = []

        chat_history.append({"role": "user", "content": user_message})

        try:
            reply = str(self.chat(user_message))
        except Exception as e:
            reply = f"[ERROR] {type(e).__name__}: {e}"

        chat_history.append({"role": "assistant", "content": reply})
        return chat_history, ""
