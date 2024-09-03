from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import json


@dataclass
class Usage:
    input_tokens: int
    output_tokens: int


@dataclass
class TextBlock:
    text: str
    type: str


@dataclass
class UnifiedMessage:
    id: str
    content: List[TextBlock]
    top_logprobs: Optional[Dict[str, float]]
    model: str
    role: str
    stop_reason: str
    usage: Usage


class LLMAPISerializer:
    @staticmethod
    def serialize_usage(usage: Usage) -> dict:
        return {
            "input_tokens": usage.input_tokens,
            "output_tokens": usage.output_tokens
        }

    @staticmethod
    def deserialize_usage(data: dict) -> Usage:
        return Usage(
            input_tokens=data["input_tokens"],
            output_tokens=data["output_tokens"]
        )

    @staticmethod
    def serialize_text_block(text_block: TextBlock) -> dict:
        return {
            "text": text_block.text,
            "type": text_block.type
        }

    @staticmethod
    def deserialize_text_block(data: dict) -> TextBlock:
        return TextBlock(
            text=data["text"],
            type=data["type"]
        )

    @staticmethod
    def serialize_unified_message(message: UnifiedMessage) -> dict:
        return {
            "id": message.id,
            "content": [LLMAPISerializer.serialize_text_block(block) for block in message.content],
            # "top_logprobs": message.top_logprobs,
            "top_logprobs": message.top_logprobs if message.top_logprobs is not None else None,
            "model": message.model,
            "role": message.role,
            "stop_reason": message.stop_reason,
            "usage": LLMAPISerializer.serialize_usage(message.usage)
        }

    @staticmethod
    def deserialize_unified_message(data: dict) -> UnifiedMessage:
        return UnifiedMessage(
            id=data["id"],
            content=[LLMAPISerializer.deserialize_text_block(
                block) for block in data["content"]],
            top_logprobs=data["top_logprobs"],
            model=data["model"],
            role=data["role"],
            stop_reason=data["stop_reason"],
            usage=LLMAPISerializer.deserialize_usage(data["usage"])
        )

    @staticmethod
    def from_claude_response(response: Any) -> UnifiedMessage:
        return UnifiedMessage(
            id=response.id,
            content=[TextBlock(text=block.text, type=block.type)
                     for block in response.content],
            top_logprobs=None,  # Claude doesn't provide top logprobs
            model=response.model,
            role=response.role,
            stop_reason=response.stop_reason,
            usage=Usage(input_tokens=response.usage.input_tokens,
                        output_tokens=response.usage.output_tokens)
        )

    @staticmethod
    def from_openai_response(response: Any) -> UnifiedMessage:
        choice = response.choices[0]
        content = choice.message.content

        # Extract top logprobs if available
        top_logprobs = None
        if choice.logprobs and choice.logprobs.content:
            first_token = choice.logprobs.content[0]
            top_logprobs = {
                logprob.token: logprob.logprob for logprob in first_token.top_logprobs}

        return UnifiedMessage(
            id=response.id,
            content=[TextBlock(text=content, type='text')],
            top_logprobs=top_logprobs,
            model=response.model,
            role=choice.message.role,
            stop_reason=choice.finish_reason,
            usage=Usage(input_tokens=response.usage.prompt_tokens,
                        output_tokens=response.usage.completion_tokens)
        )

    @staticmethod
    def to_unified_format(response: Any, api_type: str) -> dict:
        if api_type == 'claude':
            unified_message = LLMAPISerializer.from_claude_response(response)
        elif api_type == 'openai':
            unified_message = LLMAPISerializer.from_openai_response(response)
        else:
            raise ValueError(f"Unsupported API type: {api_type}")

        return LLMAPISerializer.serialize_unified_message(unified_message)

    @staticmethod
    def pretty_print(data: dict, indent: int = 2) -> None:
        """
        Print the dictionary in a nicely formatted JSON-like format.

        Args:
            data (dict): The dictionary to print.
            indent (int): The number of spaces to use for indentation.
        """
        print(json.dumps(data, indent=indent, ensure_ascii=False))
