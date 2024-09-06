import os
import string
import numpy as np
import pandas as pd
import pickle
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from src.config import VIS_DIR, EVAL_DIR, DIF_LEVELS, DIF_COLORS
from src.data import combine_prob_entries, token_to_suspect


def highlight_culprit(ax, suspects, culprit):
    culprit_index = suspects.index(culprit)
    ylabels = ax.get_yticklabels()
    for i, label in enumerate(ylabels):
        if i == culprit_index:
            label.set_bbox(dict(facecolor='lightgreen',
                           edgecolor='none', alpha=0.5))


def make_viz_dir(data):
    tl = data["title"].lower().replace(" ", "_")
    dif = data["difficulty"]
    return os.path.join(f"{VIS_DIR}/{dif}", f"{tl}")


def plot_topprobs(completions, data, model_name, force_rerun=False):
    fp = make_viz_dir(data)
    os.makedirs(fp, exist_ok=True)
    base_filename = f"{model_name}_topprobs"
    extension = '.mp4'
    filename = os.path.join(fp, f"{base_filename}{extension}")

    # Check if file already exists and force_rerun is False
    if os.path.exists(filename) and not force_rerun:
        print(f"File '{filename}' already exists. Skipping plot generation.")
        return

    suspects = data['suspects']
    culprit = data['culprit']

    fig, ax = plt.subplots(figsize=(12, 10))

    # Check only the first completion for top_logprobs
    if not completions or completions[0].get('top_logprobs') is None:
        print(f"No valid top_logprobs data found for model {model_name}")
        plt.close(fig)  # Close the figure to free up memory
        return  # Exit the function without saving a file

    def animate(j):
        ax.clear()
        completion = completions[j]
        top_logprobs_dict = completion.get('top_logprobs', {})

        if not top_logprobs_dict:
            return  # Skip this frame if top_logprobs is empty

        probs = {k: np.exp(v) for k, v in top_logprobs_dict.items()}
        probs = combine_prob_entries(probs)
        letters = list(string.ascii_lowercase[:len(suspects)].upper())
        probs = {k: v for k, v in probs.items() if k in letters}
        probs = {l: probs.get(l, 0) for l in letters}
        probs = dict(
            sorted(probs.items(), key=lambda item: item[1], reverse=True))
        total = sum(probs.values())
        if total == 0:
            total = 1  # Avoid division by zero
        sus = {letters[i]: suspect for i, suspect in enumerate(suspects)}
        normalized_probs = {sus[k]: v / total for k, v in probs.items()}

        y_pos = np.arange(len(normalized_probs))
        tokens = list(normalized_probs.keys())
        probabilities = list(normalized_probs.values())
        colors = ['green' if suspect ==
                  culprit else 'blue' for suspect in tokens]

        ax.barh(y_pos, probabilities, color=colors)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(tokens, fontsize=8)
        ax.invert_yaxis()
        ax.set_xlabel('Normalized Probability')
        ax.set_title(
            f'Normalized Probabilities of Tokens (Completion {j + 1})')
        for i, v in enumerate(probabilities):
            ax.text(v, i, f'{v:.4f}', va='center')

        highlight_culprit(ax, tokens, culprit)
        ax.set_xlim(0, 1)

    anim = animation.FuncAnimation(fig, animate, frames=len(
        completions), repeat=False, interval=1000)

    anim.save(filename, writer='ffmpeg', fps=1)
    plt.close(fig)  # Close the figure to free up memory
    print(f"Plot saved as '{filename}'")


def plot_selected_suspects(completions, data, model_name, force_rerun=False):
    fp = make_viz_dir(data)
    os.makedirs(fp, exist_ok=True)
    base_filename = f"{model_name}_selected_suspects"
    extension = '.png'
    filename = os.path.join(fp, f"{base_filename}{extension}")

    # Check if file already exists and force_rerun is False
    if os.path.exists(filename) and not force_rerun:
        print(f"File '{filename}' already exists. Skipping plot generation.")
        return

    suspects = data['suspects']
    culprit = data['culprit']
    selected_suspects = []
    for completion in completions:
        selected_suspects.append(token_to_suspect(completion, suspects))
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot dots for selected suspects
    for i, suspect in enumerate(selected_suspects):
        if suspect in suspects:  # Ensure the suspect is in our list
            y_pos = suspects.index(suspect)
            ax.scatter(i+1, y_pos, color='blue', s=100)

    # Highlight the true culprit
    culprit_index = suspects.index(culprit)
    ax.axhline(y=culprit_index, color='green', linestyle='--', alpha=0.5)

    # Set up the axes
    ax.set_yticks(range(len(suspects)))
    ax.set_yticklabels(suspects)
    ax.set_xticks(range(1, len(completions) + 1))
    ax.set_xlabel('Chunk Number')
    ax.set_ylabel('Suspects')
    ax.set_title(f'Selected Suspect per Chunk - {model_name}')

    # Highlight the culprit
    highlight_culprit(ax, suspects, culprit)

    # Adjust layout and display grid
    plt.tight_layout()
    ax.grid(True, which='both', linestyle=':', alpha=0.5)

    # Save the plot
    plt.savefig(filename)
    plt.close(fig)  # Close the figure to free up memory

    print(f"Plot saved as '{filename}'")


def make_confusion():
    """
    Creates confusion matrix data from evaluation pickle files.
    """
    results = defaultdict(lambda: defaultdict(int))
    difficulty_results = defaultdict(lambda: defaultdict(list))
    model_names = set()
    model_names.add('Random')
    for difficulty in DIF_LEVELS:
        difficulty_path = os.path.join(EVAL_DIR, difficulty)
        if os.path.isdir(difficulty_path):
            for filename in os.listdir(difficulty_path):
                if filename.endswith('.pickle'):
                    filepath = os.path.join(difficulty_path, filename)
                    with open(filepath, 'rb') as f:
                        data = pickle.load(f)
                    story_name = filename.replace('.pickle', '')
                    culprit = data['data']['culprit']
                    suspects = data['data']['suspects']
                    rand_clas = 1 / len(suspects)
                    results[story_name]['Random'] = rand_clas
                    difficulty_results[difficulty]['Random'].append(rand_clas)
                    for model, completions in data['completions'].items():
                        model_names.add(model)
                        selected_suspect = token_to_suspect(
                            completions[-1], suspects)
                        correct = int(selected_suspect == culprit)
                        results[story_name][model] = correct
                        difficulty_results[difficulty][model].append(correct)
    print(f"Model names: {model_names}")
    # Create detailed DataFrame
    df_detailed = pd.DataFrame(results).T.fillna(0)
    # Create difficulty-based DataFrame
    df_difficulty = {}
    for diff, model_results in difficulty_results.items():
        df_difficulty[diff] = {model: sum(
            results)/len(results) for model, results in model_results.items()}
    df_difficulty = pd.DataFrame(df_difficulty).T.fillna(0)

    return df_detailed, df_difficulty


def to_TeX(df):
    """
    Converts a DataFrame to a LaTeX table.
    """
    return df.to_latex(float_format="%.3f", index=True, escape=False)

def to_md(df):
    """
    Converts a DataFrame to a Markdown table.
    """
    return df.to_markdown(floatfmt=".3f", index=True)
    
def plot_perf(df):
    """
    Plots grouped bar plots of accuracy by model for each difficulty level.

    Args:
    df (pd.DataFrame): DataFrame with models as columns and difficulties as rows.

    Returns:
    None (displays the plot)
    """
    # Set up the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Define width of each bar and positions of the bars
    bar_width = 0.25

    # Get the model names and number of models
    models = df.columns
    n_models = len(models)

    # Create x-positions for the bars
    indices = np.arange(n_models)

    # Plot bars for each difficulty
    for i, difficulty in enumerate(DIF_LEVELS):
        values = df.loc[difficulty] * 100  # Convert to percentage
        ax.bar(indices + i*bar_width, values, bar_width,
               label=difficulty.capitalize(), color=DIF_COLORS.get(difficulty))

        ax.axhline(y=df["Random"][difficulty] * 100,
                   color='red', linestyle='--', alpha=0.7)
    
    # Add the random performance line to the plot (for legend purposes)
    ax.plot([], [], color='red', linestyle='--', label='Random performance')

    # Customize the plot
    ax.set_ylabel('Accuracy (%)')
    ax.set_xlabel('Model')
    ax.set_title('Model Performance by Difficulty Level')
    ax.set_xticks(indices + bar_width)
    ax.set_xticklabels(models, rotation=22.5, ha='right')
    ax.legend(loc='upper right')

    # Set y-axis to show full range from 0 to 100%
    ax.set_ylim(0, 100)

    # Add gridlines for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.9)

    # Adjust layout and display the plot
    plt.tight_layout()
    fn = os.path.join(VIS_DIR, "model_performance.png")
    plt.savefig(fn)
    plt.close(fig)  # Close the figure to free up memory
    print(f"Plot saved as '{fn}'")
    # plt.show()