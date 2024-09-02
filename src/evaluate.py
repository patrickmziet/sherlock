from openai import OpenAI
import numpy as np
import string
import json
from typing import Dict, Any, List
import os
import pickle


CHOICES = list(string.ascii_lowercase[:20].upper())
CHOICES = [f"({c})" for c in CHOICES]
ANSWER_FORMAT = {
    # "letter-only": "Only give the letter correspon. For example, if you think the answer is 'A', write <ans>A</ans>.",
    "letter-only": "Only give the letter corresponding letter. For example, if you think the answer is 'A', write A.",
    # "letter-only": "Only give the letter corresponding to the culprit. The letter corresponding to the culprit is ",
    "step-by-step": "Lay out your reasoning and think step by step. Finally give the answer between the tags <ans> and </ans>. For example, if you think the answer is 'A', write <ans>A</ans>.",
}
PROMPT_TEMPLATE = """
In the following murder mystery:

{mystery}

Which of the following suspects is the culprit:

{suspects}

{answer}
"""
NUM_CHUNKS = 10


clientoa = OpenAI()


def gen_end_points(text_length: int, num_chunks: int = NUM_CHUNKS) -> List[int]:
    base_chunk_size = text_length // num_chunks
    end_points = np.arange(base_chunk_size, text_length, base_chunk_size)
    end_points[-1] = text_length
    return end_points.astype(int)


def load_json(fn: str) -> Dict[str, Any]:
    try:
        with open(fn, 'r') as f:
            mystery_data = json.load(f)
        return mystery_data
    except FileNotFoundError:
        print(f"Error: File '{fn}' not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error: '{fn}' contains invalid JSON.")
        raise


def gen_prompt(mystery: str, s: str) -> str:
    p = PROMPT_TEMPLATE.format(mystery=mystery,
                               suspects=s,
                               answer=ANSWER_FORMAT["letter-only"])
    return p


def get_completition(prompt: str) -> Any:
    completion = clientoa.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        logprobs=True,
        top_logprobs=20,
        max_tokens=1,
        temperature=0,
    )
    return completion


def eval() -> None:
    os.makedirs('data/evaluations', exist_ok=True)
    for m in os.listdir('data/mysteries'):
        print(f"evaluating {m}:")
        if m.endswith('.json'):
            print(f"--Generating prompts")
            data = load_json(f'data/mysteries/{m}')
            mystery = data["mystery"]
            reveal_index = data["reveal_index"]
            suspects = data["suspects"]
            s = " ".join([f"{CHOICES[i]} {suspect}" for i,
                          suspect in enumerate(suspects)])
            eps = gen_end_points(reveal_index)
            completions = []
            for i, e in enumerate(eps):
                prompt = gen_prompt(mystery[:e], s)
                print(f"--Getting completition {i+1}/{NUM_CHUNKS}")
                completions.append(get_completition(prompt))
            # save the completion to a file in data/evaluations
            print(f"--Saving all completitions")
            with open(f'data/evaluations/{m.replace(".json", "")}.pickle', 'wb') as f:
                evaluation = {
                    "data": data,
                    "completions": completions
                }
                pickle.dump(evaluation, f)
