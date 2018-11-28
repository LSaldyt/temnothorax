from mesa import Agent, Model
from mesa.time import RandomActivation
import random

class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def step(self):
        if self.wealth == 0:
            return
        other_agent = random.choice(self.model.schedule.agents)
        other_agent.wealth += 1
        self.wealth -= 1

class MoneyModel(Model):
    """A model with some number of agents."""
    def __init__(self, N):
        self.num_agents = N
        self.schedule = RandomActivation(self)
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)
            self.schedule.add(a)

    def step(self):
        self.schedule.step()

import matplotlib.pyplot as plt
import seaborn as sns

model = MoneyModel(10)
for i in range(10):
    model.step()

sns.set_style('darkgrid')

agent_wealth = [a.wealth for a in model.schedule.agents]
print(agent_wealth)
plt.hist(agent_wealth)
plt.show()
