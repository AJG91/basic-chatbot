from basic_chatbot.model import LocalLM
from basic_chatbot.memory import ChatMemory
from basic_chatbot.prompt_utils import build_prompt_with_history, extract_assistant_reply

class Chatbot():

    def __init__(self, model_name, n_turns):
        self.lm = LocalLM(model_name)
        self.memory = ChatMemory()
        self.model_name = model_name
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
        text = self.lm.evaluate_text(prompt)
        reply = extract_assistant_reply(text)
        
        self.memory.add_user(user_message)
        self.memory.add_assistant(reply)
        return reply
