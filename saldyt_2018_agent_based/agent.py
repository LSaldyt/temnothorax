from random      import random, choice
from collections import defaultdict
from copy        import deepcopy
from pprint      import pprint
from functools   import reduce
from time        import sleep

import pandas
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')

class Agent:
    def __init__(self):
        self.commitment = 0.0
        self.current = 0

    def __str__(self):
        return 'ant {}({})'.format(self.current, self.commitment)

    def __repr__(self):
        return str(self)

    def encounter(self, nest, weights):
        if self.commitment < weights[nest]:
            self.commitment = weights[nest]
            self.current    = nest

