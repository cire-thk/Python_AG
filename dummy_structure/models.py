"""This is the model module of dummy_structure providing models for an energy system simulation.
The dummy_structure shows a suggestion for an objective-oriented programming approach to use as a standard in the
Python-AG of the Cologne Institute for Renewable Energy (CIRE) at the University of Applied Sciences Cologne (TH Köln).
"""
__version__ = '0.1'
__author__ = 'srummmeny'

import pandas as pd
import matplotlib.pyplot as plt
# imports from dummy structure modules
from dummy_structure_constants import *


class Component:
    """
    class to describe any type of component in an energy system.
    """

    def __init__(self, name=None, parent=None):
        self.name = name
        self.parent = parent
        self.status = pd.DataFrame({'Connected': [False], 'Running': [False]})

    def get_status(self):
        print('Status of', self.name, ':')
        print(self.status)


class Photovoltaic(Component):
    """
    class to describe any type of Photovoltaic system as a component in an energy system.
    """

    def __init__(self, p_n: int, name=None, p_profile=None):
        super().__init__(name=name)
        self.p_n = p_n
        self.df = pd.DataFrame({'P_in': [], 'P_out': []})
        if p_profile is not None:
            self.df = pd.concat([self.df, p_profile])
            self.status['Running'] = True

    def curtail(self, p_to_curtail, t):
        """ curtail the PV power by power amount p_to_curtail in time step t.
        """
        self.df['P_out'][self.df.index[t]] = max(self.df['P_in'][self.df.index[t]] - p_to_curtail, 0)

    def limit(self, p_limit, t):
        """ limit the PV power to power limit p_limit in time step t.
        """
        self.df['P_out'][self.df.index[t]] = min(self.df['P_in'][self.df.index[t]], p_limit)


class Load(Component):
    """
        class to describe any type of Load system as a component in an energy system.
    """
    def __init__(self, p_n, name=None, p_profile=None):
        super().__init__(name=name)
        self.p_n = p_n
        self.df = pd.DataFrame({'P_in': [], 'P_out': []})
        if p_profile is not None:
            self.df = pd.concat([self.df, p_profile])
            self.status['Running'] = True


if __name__ == '__main__':

    # load and format csv file from data/
    filename_pv = 'sample_pv_1day.csv'
    df_pv = pd.read_csv(TIME_SERIES_PATH+filename_pv, sep=';', index_col=0, na_values=' ')
    df_pv.index = pd.to_datetime(df_pv.index, format='%d.%m.%y %H:%M')
    df_pv = df_pv.stack().str.replace(',', '.').unstack()
    df_pv = df_pv.rename(columns={'P [kW]': 'P_in'})
    df_pv['P_in'] = df_pv['P_in'].astype(float)
    filename_load = 'sample_load_1day.csv'
    df_load = pd.read_csv(TIME_SERIES_PATH + filename_load, sep=';', index_col=0, na_values=' ')
    df_load.index = pd.to_datetime(df_load.index, format='%d.%m.%y %H:%M')
    df_load = df_load.stack().str.replace(',', '.').unstack()
    df_load = df_load.rename(columns={'P [kW]': 'P_in'})
    df_load['P_in'] = df_load['P_in'].astype(float)

    # apply Photovoltaic model
    PV = Photovoltaic(65, name='PV_Meyerstr_12', p_profile=df_pv)
    Load = Load(120, name='Load_Meyerstr_12', p_profile=df_load)
    for i in range(len(PV.df.index)):
        PV.limit(0.66 * PV.p_n, i)

    # plot
    PV.get_status()
    PV.df.plot()
    plt.show()
    Load.df.plot()
    plt.show()
