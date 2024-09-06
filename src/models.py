from abc import ABC, abstractmethod
from typing import Any
from openai import OpenAI
from anthropic import Anthropic

API_TYPES = {
    "openai": ["gpt-4o-2024-05-13", 
               "gpt-4o-mini-2024-07-18", 
               "gpt-4-turbo-2024-04-09", 
               "gpt-4-0613"],
    "claude": ["claude-3-5-sonnet-20240620", 
               "claude-3-opus-20240229", 
               "claude-3-sonnet-20240229", 
               "claude-3-haiku-20240307"],
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


class GPT4oMini240718(Model):
    def __init__(self):
        super().__init__("gpt-4o-mini-2024-07-18")
        self.client = OpenAI()

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


class GPT4oTurbo240409(Model):
    def __init__(self):
        super().__init__("gpt-4-turbo-2024-04-09")
        self.client = OpenAI()

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


class GPT40613(Model):
    def __init__(self):
        super().__init__("gpt-4-0613")
        self.client = OpenAI()

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

    def make_call(self, prompt, **kwargs):
        response = self.client.messages.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0,
            **kwargs
        )

        return response


class Claude3Opus240229(Model):
    def __init__(self):
        super().__init__("claude-3-opus-20240229")
        self.client = Anthropic()

    def make_call(self, prompt, **kwargs):
        response = self.client.messages.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0,
            **kwargs
        )

        return response


class Claude3Sonnet240229(Model):
    def __init__(self):
        super().__init__("claude-3-sonnet-20240229")
        self.client = Anthropic()

    def make_call(self, prompt, **kwargs):
        response = self.client.messages.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1,
            temperature=0,
            **kwargs
        )

        return response


class Claude3Haiku240307(Model):
    def __init__(self):
        super().__init__("claude-3-haiku-20240307")
        self.client = Anthropic()

    def make_call(self, prompt, **kwargs):
        response = self.client.messages.create(
            model=self.model_name,
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
        "gpt-4o-mini-2024-07-18": GPT4oMini240718,
        "gpt-4-turbo-2024-04-09": GPT4oTurbo240409,
        "gpt-4-0613": GPT40613,
        "claude-3-5-sonnet-20240620": Claude35Sonnet240620,
        "claude-3-opus-20240229": Claude3Opus240229,
        "claude-3-sonnet-20240229": Claude3Sonnet240229,
        "claude-3-haiku-20240307": Claude3Haiku240307,
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
