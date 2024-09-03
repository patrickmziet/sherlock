import os


def list_mysteries() -> None:
    for m in os.listdir('data/mysteries'):
        print(m)
