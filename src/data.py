import os
import re

from src.config import POSSIBLE_RESPONSES, LETTERS

def list_mysteries() -> None:
    for m in os.listdir('data/mysteries'):
        print(m)


def combine_prob_entries(probs):
    combined_probs = {}
    for key, value in probs.items():
        if key.startswith('(') and len(key) > 1:
            clean_key = key[1:]  # Remove the leading parenthesis
            if clean_key in combined_probs:
                combined_probs[clean_key] += value
            else:
                combined_probs[clean_key] = value
        else:
            if key in combined_probs:
                combined_probs[key] += value
            else:
                combined_probs[key] = value

    return combined_probs

def token_to_suspect(c, suspects):
    num_suspects = len(suspects)
    suspects_dict = {LETTERS[i]: s for i, s in enumerate(suspects)}
    answer = c["content"][0]["text"]
    if answer in POSSIBLE_RESPONSES[:3*num_suspects] or answer in LETTERS[:num_suspects]:
        if answer in POSSIBLE_RESPONSES:
            answer = re.sub(r'[^A-Z]', '', answer)        
    return suspects_dict.get(answer, "")