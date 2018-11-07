from collections import defaultdict

from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('whitegrid')

def plot(history):
    combined_state_counts = defaultdict(list)
    for state in history:
        for k, v in state.items():
            combined_state_counts[k].append(v)
    pprint(combined_state_counts)
    time = list(range(len(history)))
    for k, v in combined_state_counts.items():
        try:
            plt.plot(time, v, label=k)
        except ValueError:
            print(k)
            raise
    plt.legend()
    plt.title('Ants at each nest')
    plt.ylabel('Count of ants')
    plt.xlabel('Timestep (1/10) minutes each')
    plt.show()
