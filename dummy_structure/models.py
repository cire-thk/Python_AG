"""This is the model module of dummy_structure.
The dummy_structure shows a suggestion for an objective-oriented programming approach to use as a standard in the
Python-AG of the Cologne Institute for Renewable Energy (CIRE) at the University of Applied Sciences Cologne (TH Köln).
"""
__version__ = '0.1'
__author__ = 'srummmeny'

# from dummy_constants import *
import pandas as pd
import matplotlib.pyplot as plt


class Component:
    """
    class to describe any type of component in an energy system.
    """
    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.status = pd.DataFrame({'Connected': [False], 'Running': [False]})

    def get_status(self):
        print(self.status)


class Photovoltaic(Component):
    """
    class to describe any type of Photovoltaic system as a component in an energy system.
    """
    def __init__(self, p_n: int, name=None, p_profile=None):
        super().__init__(name=name)
        self.p_n = p_n
        self.df = pd.DataFrame({'before': [], 'after': []})
        if p_profile is not None:
            self.df = pd.concat([self.df, p_profile])

    def curtail(self, p_c, t_start=0, t_end=2**100000):
        t = t_start
        while t <= min(self.df.index[-1], t_end):
            self.df['after'][t] = max(self.df['before'][t] - p_c, 0)
            t += 1

    def limit(self, p_l, t_start=0, t_end=2**100000):
        t = t_start
        while t <= min(self.df.index[-1], t_end):
            self.df['after'][t] = min(self.df['before'][t], p_l)
            t += 1


if __name__ == '__main__':
    df = pd.DataFrame({'before': [0, 0, 0, 0.5, 1.7, 3.4, 6.8, 8.1, 8.5, 7.1, 4.2, 1.8, 0.4, 0, 0, 0]})

    PV = Photovoltaic(12, name='PV_Meyerstr_12', p_profile=df)
    PV.limit(4)
    PV.df.plot()
    plt.show()
