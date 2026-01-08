import os
from typing import Union, List
from openai import OpenAI

class OpenAIChat:
    """
    Docstring for OpenAIChat
    """
    def __init__(
        self, 
        model: str = "gpt-3.5-turbo"
    ):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set.")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_text(
        self,
        prompt: Union[List[str], str],
        max_tokens: int = 100,
        top_p: float = 0.95,
        temperature: float = 0.8
    ) -> str:
        """
        Docstring for generate_text
        """
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content