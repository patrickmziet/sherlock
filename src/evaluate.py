from openai import OpenAI
import numpy as np
import string
import json
from typing import Dict, Any
import os
import pickle


CHOICES = list(string.ascii_lowercase[:20].upper())
CHOICES = [f"({c})" for c in CHOICES]
ANSWER_FORMAT = {
    "letter-only": "Only give the corresponding letter between the tags <ans> and </ans>. For example, if you think the answer is 'A', write <ans>A</ans>.",
    "step-by-step": "Lay out your reasoning and think step by step. Finally give the answer between the tags <ans> and </ans>. For example, if you think the answer is 'A', write <ans>A</ans>.",
}

PROMPT_TEMPLATE = """
In the following murder mystery:

{mystery}

Which of the following suspects is the culprit:

{suspects}

{answer}
"""


clientoa = OpenAI()


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


def gen_prompt(fn: str) -> str:
    data = load_json(fn)
    mystery = data["mystery"]
    reveal_index = data["reveal_index"]
    suspects = data["suspects"]
    s = " ".join([f"{CHOICES[i]} {suspect}" for i,
                 suspect in enumerate(suspects)])
    p = PROMPT_TEMPLATE.format(mystery=mystery[:reveal_index],
                               suspects=s,
                               answer=ANSWER_FORMAT["letter-only"])
    return p


def get_completition(prompt):
    completion = clientoa.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        logprobs=True,
        top_logprobs=20
    )
    return completion


def eval() -> None:
    # TODO: make a table of of story x model to see if the it has completed the story. Keep in data folder

    # Create the directory if it doesn't exist
    os.makedirs('data/evaluations', exist_ok=True)

    # loop through all the files in the data/mysteries folder and get the completions
    for m in os.listdir('data/mysteries'):
        print(f"evaluating {m}:")
        if m.endswith('.json'):
            print(f"--Generating prompt")
            prompt = gen_prompt(f'data/mysteries/{m}')
            print(f"--Getting completition")
            completion = get_completition(prompt)
            # save the completion to a file in data/evaluations
            print(f"--Saving completition")
            with open(f'data/evaluations/{m.replace(".json", "")}.pickle', 'wb') as f:
                pickle.dump(completion, f)
            # print(f"Completion:\n{completion}")
