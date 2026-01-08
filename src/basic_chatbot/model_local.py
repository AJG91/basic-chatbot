import torch as tc
from transformers import (
    AutoModelForCausalLM, AutoTokenizer, 
    PreTrainedTokenizerBase, PreTrainedModel
)
from transformers.generation.utils import GenerateOutput
from typing import Union
from basic_chatbot.utils import get_device, to_device

class LocalLM():
    """
    A class for loading and managing a tokenizer and decoder model.

    This class contains all the functionality necessary to load
    a decoder model, as well as functions for loading and applying
    a tokenizer and a data collator.
        
    Attributes
    ----------
    model_name : str
        Name of model that will be loaded.
    device : tc.device
        Device that tensors will be moved to.
    tokenizer : PreTrainedTokenizerBase
        The tokenizer instance loaded from the pretrained model.

    Parameters
    ----------
    model_name : str
        Name of model that will be loaded.
    """
    def __init__(
        self, 
        model_name: str
    ):
        self.model_name = model_name
        self.device = get_device()
        self.tokenizer: PreTrainedTokenizerBase = AutoTokenizer.from_pretrained(model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = self.load_model()

    def tokenize_text(
        self, 
        prompt: str, 
        padding: Union[bool, str] = True, 
        truncation: Union[bool, str] = True
    ) -> dict[str, tc.Tensor]:
        """
        Tokenizes a text prompt (or list of prompts) and moves the 
        resulting tensors to the target device.

        Parameters
        ----------
        prompt : str or list[str]
            The input text or list of texts to tokenize.
        padding : bool or str, optional (default=True)
            Denotes the padding technique to use.
            If True, pad to the longest sequence in the batch.
            If False, does not pad.
        truncation : bool or str, optional (default=True)
            Denotes the truncation technique to use.
            If True, truncates to the model's maximum length.
            If False, does not truncate.
    
        Returns
        -------
        dict[str, tc.Tensor]
            A mapping from input field names (e.g. `'input_ids'`, `'attention_mask'`) 
            to PyTorch tensors located on `self.device`.
        """
        inputs = self.tokenizer(
            prompt,
            padding=padding,
            truncation=truncation,
            return_tensors="pt"
        )
        return to_device(inputs, self.device)

    def load_model(
        self,
    ) -> PreTrainedModel:
        """
        Loads a pretrained sequence classification model and 
        moves it to the target device.
    
        Returns
        -------
        PreTrainedModel
            A sequence classification model instance located on `self.device`.
        """
        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
        ).to(self.device)
        model.config.pad_token_id = self.tokenizer.pad_token_id
        return model
    
    def evaluate_text(
        self,
        prompt: Union[list[str], str],
        max_new_tokens: int = 60,
        do_sample: bool = True,
        top_k: int = 25,
        top_p: float = 0.95,
        temperature: float = 0.8,
        repetition_penalty: Union[int, float] = 1.1,
        skip_special_tokens: bool = True
    ) -> Union[tc.Tensor, GenerateOutput]:
        """
        Tokenizes an input prompt, puts the model in evaluation model, and generates 
        text based on the given prompt.
        
        Parameters
        ----------
        prompt : Union[list[str], str]
            Can be a list of prompts or a single prompt.
        max_new_tokens : int, optional(default=60)
            Total amount of tokens that will be used in the text generation.
        do_sample : bool, optional (default=True)
            Tells model to sample from probability distribution instead of 
            picking the highest-probability token.
            If False, deterministic.
            If True, random sampling.
        top_k : int, optional (default=25)
            Sorts logits, keeps top N most probably tokens, and samples from those.
            Lower k -> more deterministic.
            Higher k -> more random.
        top_p : float, optional (default=0.95)
            Keeps the smallest set of tokens whose cumulative probability >= N.
        temperature : float, optional (default=0.8)
            Denotes the fraction of temperature that will be used when sampling.
            Lower T -> more deterministic.
            Higher T -> more random.
        repetition_penalty : Union[int, float], optional (default=1.1)
            Specifies how much penalty will be added to the model when repeating text.
        skip_special_tokens : bool, optional (default=True)
            If True, skips special tokens such as classification and padding tokens 
            in the output text.
            If False, includes special tokens in the output text.

        Returns
        -------
        str
            Text generated by the model.
        """
        model = self.model
        inputs = self.tokenize_text(prompt)

        model.eval()
        with tc.no_grad():
            outputs = model.generate(
                **inputs, 
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                repetition_penalty=repetition_penalty,
                pad_token_id=self.tokenizer.pad_token_id
            )
        return self.decode_tokens(outputs[0], skip_special_tokens)
    
    def decode_tokens(
        self, 
        output_tokens: tc.Tensor,
        skip_special_tokens: bool = True
    ) -> str:
        """
        Converts the tokens outputted by the model into its corresponding string.

        Parameters
        ----------
        output_tokens : tc.Tensor
            A tensor containing the tokens generated by the model.
        skip_special_tokens : bool, optional (default=True)
            If True, skips special tokens such as classification and padding tokens 
            in the output text.
            If False, includes special tokens in the output text.

        Returns
        -------
        str
            Text generated by the model.
        """
        return self.tokenizer.decode(
            output_tokens, 
            skip_special_tokens=skip_special_tokens
            )