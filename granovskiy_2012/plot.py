from collections import defaultdict

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

def plot(history):
    combined_state_counts = defaultdict(list)
    for state in history:
        for k, v in state.items():
            combined_state_counts[k].append(v)
    time = list(range(len(history)))
    for k, v in combined_state_counts.items():
        plt.plot(time, v, label=k)
    plt.legend()
    plt.title('Ants at each nest')
    plt.ylabel('Count of ants')
    plt.xlabel('Timestep (1/10) minutes each')
    plt.show()
