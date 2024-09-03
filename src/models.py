from abc import ABC, abstractmethod
from typing import Any
from openai import OpenAI
from anthropic import Anthropic

API_TYPES = {
    "openai": ["gpt-4o-2024-05-13"],
    "claude": ["claude-3-5-sonnet-20240620"],
}


class Model(ABC):
    def __init__(self, model_name):
        self.model_name = model_name
        self.api_type = next(
            (api for api, models in API_TYPES.items() if model_name in models), None)
        if self.api_type is None:
            raise ValueError(f"Unknown model: {model_name}")

    @abstractmethod
    def make_call(self, prompt, **kwargs):
        pass

    def get_metadata(self):
        return {
            "model_name": self.model_name,
            "api_type": self.api_type
        }

    def __call__(self):
        return f"{self.model_name}"


class GPT4o240513(Model):
    def __init__(self):
        super().__init__("gpt-4o-2024-05-13")
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
        "gpt-4o-2024-05-13": GPT4o240513,
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

    @staticmethod
    def list_models_by_api():
        return API_TYPES
