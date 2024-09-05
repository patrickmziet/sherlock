import numpy as np
import json
from typing import Dict, Any, List
import os
import pickle
from tqdm import tqdm

from src.models import ModelFactory
from src.serializers import LLMAPISerializer
from src.config import EVAL_DIR, MYS_DIR, CHOICES, EXAMPLE, ANSWER_FORMAT, PROMPT_TEMPLATE, NUM_CHUNKS


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
    all_models = ModelFactory.list_all_models()
    print(f"Available models: {all_models}")
    for dif in os.listdir(MYS_DIR):
        os.makedirs(f'{EVAL_DIR}/{dif}', exist_ok=True)
        print(f"Evaluating difficulty: {dif}")
        for mys in os.listdir(f'{MYS_DIR}/{dif}'):
            print(f"Evaluating mystery: {mys}:")
            if mys.endswith('.json'):
                print(f"--Generating prompts")
                data = load_json(f'{MYS_DIR}/{dif}/{mys}')
                mystery = data["mystery"]
                reveal_index = data["reveal_index"]
                suspects = data["suspects"]
                smcq = " ".join([f"{CHOICES[i]} {suspect}" for i,
                                suspect in enumerate(suspects)])
                eps = gen_end_points(reveal_index)
                fn_e = f'{EVAL_DIR}/{dif}/{mys.replace(".json", "")}.pickle'
                to_eval = all_models
                completions = {}
                if os.path.exists(fn_e):
                    with open(fn_e, 'rb') as f:
                        evaluation = pickle.load(f)
                    completions = evaluation["completions"]
                    done_eval = list(completions.keys())
                    print(f"--Already evaluated models: {done_eval}")
                    to_eval = [
                        mod for mod in all_models if mod not in done_eval]
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
