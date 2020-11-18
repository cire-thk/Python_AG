"""This is the model module of dummy_structure providing models for an energy system simulation.
The dummy_structure shows a suggestion for an objective-oriented programming approach to use as a standard in the
Python-AG of the Cologne Institute for Renewable Energy (CIRE) at the University of Applied Sciences Cologne (TH Köln).
"""
__version__ = '0.1'
__author__ = 'srummmeny'

from dummy_structure_constants import TIME_SERIES_PATH
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
            self.status['Running'] = True

    def curtail(self, p_c, t_start=0, t_end=2**100000):
        t = t_start
        while t <= min(len(self.df.index)-1, t_end):
            self.df['after'][df.index[t]] = max(self.df['before'][df.index[t]] - p_c, 0)
            t += 1

    def limit(self, p_l, t_start=0, t_end=2**100000):
        t = t_start
        while t <= min(len(self.df.index)-1, t_end):
            self.df['after'][df.index[t]] = min(self.df['before'][df.index[t]], p_l)
            t += 1


if __name__ == '__main__':

    # load and format csv file from data/
    filename = 'sample_pv_1day.csv'
    df = pd.read_csv(TIME_SERIES_PATH+filename, sep=';', index_col=0, na_values=' ')
    df.index = pd.to_datetime(df.index, format='%d.%m.%y %H:%M')
    df = df.stack().str.replace(',', '.').unstack()
    df = df.rename(columns={'P [kW]': 'before'})
    df['before'] = df['before'].astype(float)

    # apply Photovoltaic model
    PV = Photovoltaic(65, name='PV_Meyerstr_12', p_profile=df)
    PV.get_status()
    PV.limit(0.66*PV.p_n)

    # plot
    PV.df.plot()
    plt.show()
