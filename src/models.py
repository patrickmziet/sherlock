from abc import ABC, abstractmethod
from typing import Any
from openai import OpenAI
from anthropic import Anthropic


class Model(ABC):
    def __init__(self, model_name):
        self.model_name = model_name

    @abstractmethod
    def make_call(self, prompt, **kwargs):
        pass

    def get_metadata(self):
        return {
            "model_name": self.model_name
        }

    def __call__(self):
        return f"{self.model_name}"


class GPT4o(Model):
    def __init__(self):
        super().__init__("gpt-4o")
        self.client = OpenAI()
        print(f"Established connection with {self.model_name}")

    def make_call(self, prompt, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            logprobs=True,
            top_logprobs=20,
            max_tokens=1,
            temperature=0,
            **kwargs
        )
        return response


class Claude35Sonnet240620(Model):
    def __init__(self):
        super().__init__("claude-3-5-sonnet-20240620")
        self.client = Anthropic()
        print(f"Established connection with {self.model_name}")

    def make_call(self, prompt, **kwargs):
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0,
            **kwargs
        )

        return response


class ModelFactory:
    model_classes = {
        "gpt-4o": GPT4o,
        "claude-3-5-sonnet-20240620": Claude35Sonnet240620
    }

    @staticmethod
    def get_model(model_type):
        if model_type in ModelFactory.model_classes:
            return ModelFactory.model_classes[model_type]()
        else:
            raise ValueError("Model type not supported")

    @staticmethod
    def list_all_models():
        return list(ModelFactory.model_classes.keys())
