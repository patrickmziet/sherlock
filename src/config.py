import os
import string
from itertools import chain

# Directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MYS_DIR = os.path.join(DATA_DIR, 'mysteries')
EVAL_DIR = os.path.join(DATA_DIR, 'evaluations')
VIS_DIR = os.path.join(DATA_DIR, 'visualizations')

# Categories for difficulty levels
DIF_LEVELS = ['easy', 'medium', 'hard']
COLORS = ['#009E73', '#0072B2', '#D55E00'] # See https://davidmathlogic.com/colorblind/#%23000000-%23E69F00-%2356B4E9-%23009E73-%23F0E442-%230072B2-%23D55E00-%23CC79A7
DIF_COLORS = dict(zip(DIF_LEVELS, COLORS))

# Constants for mystery generation
MAX_CHOICES = 20
LETTERS = list(string.ascii_uppercase[:MAX_CHOICES])
CHOICES = [f"({c})" for c in LETTERS]
POSSIBLE_RESPONSES = list(
    chain(*[[f"({A}", f"{A})", f"({A})"] for A in LETTERS]))

EXAMPLE = """
I am going to give you a  mystery to solve, you must read the mystery and then identify the culprit from a list of suspects. Here is an example mystery:

Detective Moore frowned at the shattered display case in the museum. The priceless Egyptian scarab was missing, and four people had been near the exhibit in the past hour: Dr. Sarah Evans, the museum's curator, who had been giving a tour; Jake Thompson, a security guard on his first day; Mira Patel, a visiting archaeologist who had been examining the scarab earlier; and Tom Chen, a frequent museum patron who claimed to have been sketching nearby artifacts. As Moore questioned each suspect, he noticed Dr. Evans fidgeting with her lanyard, Jake's uniform seemed slightly askew, Mira kept glancing at her oversized handbag, and Tom's sketchbook was suspiciously devoid of any recent drawings. With a knowing smile, Moore announced, "I know who took the scarab.

Which of the following suspects is the culprit:

(A) Detective Moore (B) Dr. Sarah Evans (C) Jake Thompson (D) Mira Patel (E) Tom Chen

Answer: B
"""
ANSWER_FORMAT = {
    "letter-only": "Only give the letter corresponding letter. For example, if you think the answer is 'A', write A. Answer: ",
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
NUM_CHUNKS = 10
