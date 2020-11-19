"""This is the operation module of dummy_structure providing operators for an energy system simulation.
The dummy_structure shows a suggestion for an objective-oriented programming approach to use as a standard in the
Python-AG of the Cologne Institute for Renewable Energy (CIRE) at the University of Applied Sciences Cologne (TH Köln).
"""
__version__ = '0.1'
__author__ = 'srummmeny'

import pandas as pd
import numpy as np
# imports from dummy structure modules
from dummy_structure_constants import *


class Operator:
    def __init__(self, env):
        self.env = env

    def dummy_strategy(self, p_feed_in_limit):
        """Exemplary rule based dispatch strategy how to operate the environment of the dummy_structure. Here a simple
        feed_in_limit is introduced.
        """
        for t in self.env.time:
            self.env.df['P_res'][t] = np.nansum(self.env.Load[-1].df['P_in'][t], -self.env.PV[-1].df['P_in'][t])
            if -self.env.df['P_res'][t] > p_feed_in_limit:
                self.env.PV[-1].curtail(-self.env.df['P_res'][t], t)
                self.env.df['P_res'][t] -= self.env.df['P_res'][t]
            else:
                continue
