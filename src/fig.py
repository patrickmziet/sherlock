import os
import re
import string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

VIS_DIR = 'data/visualizations'


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


def plot_topprobs(completions, data, model_name):
    suspects = data['suspects']
    culprit = data['culprit']

    fig, ax = plt.subplots(figsize=(12, 10))

    def animate(j):
        ax.clear()
        completion = completions[j]
        top_logprobs_dict = completion.get('top_logprobs', {})

        if not top_logprobs_dict:
            print(f"No top_logprobs data for completion {j}")
            return

        probs = {k: np.exp(v) for k, v in top_logprobs_dict.items()}
        probs = combine_prob_entries(probs)
        letters = list(string.ascii_lowercase[:len(suspects)].upper())
        probs = {k: v for k, v in probs.items() if k in letters}
        probs = {l: probs.get(l, 0) for l in letters}
        probs = dict(
            sorted(probs.items(), key=lambda item: item[1], reverse=True))
        total = sum(probs.values())
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

        culprit_index = tokens.index(culprit)
        ylabels = ax.get_yticklabels()
        for i, label in enumerate(ylabels):
            if i == culprit_index:
                label.set_bbox(dict(facecolor='lightgreen',
                               edgecolor='none', alpha=0.5))

        ax.set_xlim(0, 1)

    anim = animation.FuncAnimation(fig, animate, frames=len(
        completions), repeat=False, interval=1000)
    tl = data["title"].lower().replace(" ", "_")
    fp = os.path.join(VIS_DIR, f"{tl}")
    os.makedirs(fp, exist_ok=True)
    base_filename = f"{model_name}_topprobs"
    extension = '.mp4'
    filename = os.path.join(fp, f"{base_filename}{extension}")
    anim.save(filename, writer='ffmpeg', fps=1)
    plt.close(fig)  # Close the figure to free up memory


def plot_selected_suspects(completions, data, model_name):
    suspects = data['suspects']
    culprit = data['culprit']

    # Extract the selected suspect from the content of each completion
    selected_suspects = []
    for completion in completions:
        content = completion.get('content', [])
        if content:
            text = content[0].get('text', '')
            selected_suspect = re.sub(r'[^A-Z]', '', text)
            selected_suspects.append(selected_suspect)
        else:
            selected_suspects.append('')

    letters = list(string.ascii_lowercase[:len(suspects)].upper())
    sus = {letters[i]: suspect for i, suspect in enumerate(suspects)}
    selected_suspects = [sus.get(suspect) for suspect in selected_suspects]

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

    # Adjust layout and display grid
    plt.tight_layout()
    ax.grid(True, which='both', linestyle=':', alpha=0.5)

    # Save the plot
    tl = data["title"].lower().replace(" ", "_")
    fp = os.path.join(VIS_DIR, f"{tl}")
    os.makedirs(fp, exist_ok=True)
    base_filename = f"{model_name}_selected_suspects"
    extension = '.png'
    filename = os.path.join(fp, f"{base_filename}{extension}")
    plt.savefig(filename)
    plt.close(fig)  # Close the figure to free up memory

    print(f"Plot saved as '{filename}'")