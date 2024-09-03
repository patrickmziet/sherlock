import numpy as np
import string
import json
from typing import Dict, Any, List
import os
import pickle
from tqdm import tqdm

from src.models import ModelFactory
from src.serializers import LLMAPISerializer

MAX_CHOICES = 20
CHOICES = list(string.ascii_lowercase[:MAX_CHOICES].upper())
CHOICES = [f"({c})" for c in CHOICES]
EXAMPLE = """
I am going to give you a  mystery to solve, you must read the mystery and then identify the culprit from a list of suspects. Here is an example mystery:

Detective Moore frowned at the shattered display case in the museum. The priceless Egyptian scarab was missing, and four people had been near the exhibit in the past hour: Dr. Sarah Evans, the museum's curator, who had been giving a tour; Jake Thompson, a security guard on his first day; Mira Patel, a visiting archaeologist who had been examining the scarab earlier; and Tom Chen, a frequent museum patron who claimed to have been sketching nearby artifacts. As Moore questioned each suspect, he noticed Dr. Evans fidgeting with her lanyard, Jake's uniform seemed slightly askew, Mira kept glancing at her oversized handbag, and Tom's sketchbook was suspiciously devoid of any recent drawings. With a knowing smile, Moore announced, "I know who took the scarab.

Which of the following suspects is the culprit:

(A) Detective Moore (B) Dr. Sarah Evans (C) Jake Thompson (D) Mira Patel (E) Tom Chen

Answer: B
"""
ANSWER_FORMAT = {
    "letter-only": "Only give the letter corresponding letter. For example, if you think the answer is 'A', write A. Answer: ",
    # "letter-only": "Only give the letter corresponding to the culprit. The letter corresponding to the culprit is ",
    "step-by-step": "Lay out your reasoning and think step by step. Finally give the answer between the tags <ans> and </ans>. For example, if you think the answer is 'A', write <ans>A</ans>.",
}
PROMPT_TEMPLATE = """
{example}

Now in the following murder mystery:

{mystery}

Which of the following suspects is the culprit:

{suspects}

{answer} 
"""
NUM_CHUNKS = 3


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


def gen_prompt(mystery: str, suspect_mcq: str) -> str:
    p = PROMPT_TEMPLATE.format(example=EXAMPLE,
                               mystery=mystery,
                               suspects=suspect_mcq,
                               answer=ANSWER_FORMAT["letter-only"])
    return p


def eval() -> None:
    os.makedirs('data/evaluations', exist_ok=True)
    all_models = ModelFactory.list_all_models()
    print(f"Available models: {all_models}")
    for mys in os.listdir('data/mysteries'):
        print(f"Evaluating mystery: {mys}:")
        if mys.endswith('.json'):
            print(f"--Generating prompts")
            data = load_json(f'data/mysteries/{mys}')
            mystery = data["mystery"]
            reveal_index = data["reveal_index"]
            suspects = data["suspects"]
            smcq = " ".join([f"{CHOICES[i]} {suspect}" for i,
                             suspect in enumerate(suspects)])
            eps = gen_end_points(reveal_index)
            fn_e = f'data/evaluations/{mys.replace(".json", "")}.pickle'
            to_eval = all_models
            completions = {}
            if os.path.exists(fn_e):
                with open(fn_e, 'rb') as f:
                    evaluation = pickle.load(f)
                completions = evaluation["completions"]
                done_eval = list(completions.keys())
                print(f"--Already evaluated models: {done_eval}")
                to_eval = [mod for mod in all_models if mod not in done_eval]
                print(f"--Models to evaluate: {to_eval}")
            prompts = [gen_prompt(mystery[:e], smcq) for e in eps]
            completions.update({mod: [] for mod in to_eval})
            for mod in to_eval:
                model = ModelFactory.get_model(mod)
                print(f"--Evaluating model: {mod}")
                for p in tqdm(prompts, desc="Getting completions", unit="chunk"):
                    completions[mod].append(LLMAPISerializer.to_unified_format(
                        model.make_call(p), model.api_type))
            print(f"--Saving all completitions")
            with open(fn_e, 'wb') as f:
                evaluation = {
                    "data": data,
                    "completions": completions
                }
                pickle.dump(evaluation, f)
