from collections import defaultdict

from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

LINE_STYLES = ['solid', 'dashed', 'dashdot', 'dotted']
NUM_STYLES = len(LINE_STYLES)

#sns.reset_orig()  # get default matplotlib styles back

def plot(history):
    combined_state_counts = defaultdict(list)
    for state in history:
        for k, v in state.items():
            combined_state_counts[k].append(v)
    colors = sns.color_palette('husl', n_colors=len(combined_state_counts))  # a list of RGB tuples
    time = list(range(len(history)))
    for i, (k, v) in enumerate(combined_state_counts.items()):
        lines = plt.plot(time, v, label=k)
        lines[0].set_color(colors[i])
        lines[0].set_linestyle(LINE_STYLES[i%NUM_STYLES])
    plt.legend()
    plt.title('Ants at each nest')
    plt.ylabel('Count of ants')
    plt.xlabel('Timestep (1/10) minutes each')
    plt.show()
