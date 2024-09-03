import json
from typing import List
import os
# from enter_details import TITLE, DIFFICULTY, MYSTERY, SUSPECTS, CULPRIT, REVEAL_INDEX


def create_mystery_json(
    title: str,
    difficulty: str,
    mystery: str,
    suspects: List[str],
    culprit: str,
    reveal_index: int
) -> None:

    # Type checks
    if not isinstance(title, str):
        raise TypeError("Title must be a string")
    if not isinstance(difficulty, str):
        raise TypeError("Difficulty must be a string")
    if not isinstance(mystery, str):
        raise TypeError("Mystery must be a string")
    if not isinstance(suspects, list) or not all(isinstance(s, str) for s in suspects):
        raise TypeError("Suspects must be a list of strings")
    if not isinstance(culprit, str):
        raise TypeError("Culprit must be a string")
    if not isinstance(reveal_index, int):
        raise TypeError("Reveal index must be an integer")

    # Check difficulty is either 'easy', 'medium', or 'hard'
    if difficulty not in ['easy', 'medium', 'hard']:
        raise ValueError("Difficulty must be either 'easy', 'medium', or 'hard'")

    # Check if culprit is in suspects
    if culprit not in suspects:
        raise ValueError("Culprit must be one of the suspects")

    # Check if reveal_index is within bounds
    if reveal_index < 0 or reveal_index > len(mystery):
        raise ValueError(
            "Reveal index must be between 0 and the length of the mystery")

    mystery_dict = {
        "title": title,
        "difficulty": difficulty,
        "mystery": mystery,
        "suspects": suspects,
        "culprit": culprit,
        "reveal_index": reveal_index
    }

    # Use json.dumps() to properly encode the entire dictionary
    json_string: str = json.dumps(mystery_dict, indent=2)

    # Generate base filename
    base_filename = title.lower().replace(' ', '_')
    filename = f"data/mysteries/{base_filename}.json"

    # Check for existing files with similar names
    similar_files = [f for f in os.listdir(
        "data/mysteries") if f.startswith(base_filename)]

    # If similar files exist, warn the user
    if similar_files:
        print("Warning: The following files have similar names and should be checked:")
        for file in similar_files:
            print(f"- {file}")

    # Ensure filename is unique
    counter = 1
    while os.path.exists(filename):
        filename = f"data/mysteries/{base_filename}_{counter}.json"
        counter += 1

    # Save to file
    with open(filename, 'w') as f:
        f.write(json_string)

    print(f"Mystery '{title}' has been saved successfully.")


# if __name__ == "__main__":
#     try:
#         create_mystery_json(TITLE, DIFFICULTY, MYSTERY, SUSPECTS, CULPRIT, REVEAL_INDEX)
#     except (TypeError, ValueError) as e:
#         print(f"Error: {e}")
#         print("Please check your input and try again.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         print("Please check your input and try again.")
