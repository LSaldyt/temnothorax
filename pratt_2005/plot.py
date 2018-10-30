from pprint import pprint
from collections import defaultdict

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')
def plot(history):
    state_counts, nest_counts = zip(*history)
    combined_state_counts = defaultdict(list)
    for state in state_counts:
        for k1, v1 in state.items():
            print(v1)
            for k2, v2 in v1.items():
                combined_state_counts[k1 + '-' + k2].append(v2)

    time = list(range(len(history)))
    for k, v in combined_state_counts.items():
        plt.plot(time, v, label=k)
    plt.legend()
    plt.show()
