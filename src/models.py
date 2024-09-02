from abc import ABC, abstractmethod
from openai import OpenAI

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


class GPT4o(Model):
    def __init__(self):
        super().__init__("gpt-4o")

    def make_call(self, prompt, **kwargs):
        print(f"Established connection with {self.model_name}")
        client = OpenAI()
        print(f"Calling {self.model_name} with prompt: {prompt}")
        response = client.chat.completions.create(
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


class ModelFactory:
    model_classes = {
        "gpt-4o": GPT4o
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