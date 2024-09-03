import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')
MYS_DIR = os.path.join(DATA_DIR, 'mysteries')
EVAL_DIR = os.path.join(DATA_DIR, 'evaluations')
VIS_DIR = os.path.join(DATA_DIR, 'visualizations')