import os
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
        top_logprobs_dict = {}
        for i in range(20):
            top_logprobs_dict[completion.choices[0].logprobs.content[0].top_logprobs[i]
                              .token] = completion.choices[0].logprobs.content[0].top_logprobs[i].logprob

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

        # Change background color of ylabel for the true culprit
        culprit_index = tokens.index(culprit)
        ylabels = ax.get_yticklabels()
        for i, label in enumerate(ylabels):
            if i == culprit_index:
                label.set_bbox(dict(facecolor='lightgreen',
                               edgecolor='none', alpha=0.5))

        ax.set_xlim(0, 1)  # Set fixed x-axis limits

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
