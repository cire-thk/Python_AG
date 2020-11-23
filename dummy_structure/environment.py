"""This is the environment module of dummy_structure providing the environment for an energy system simulation.
The dummy_structure shows a suggestion for an objective-oriented programming approach to use as a standard in the
Python-AG of the Cologne Institute for Renewable Energy (CIRE) at the University of Applied Sciences Cologne (TH Köln).
"""
__version__ = '0.1'
__author__ = 'srummmeny'

import datetime as dt
import pandas as pd
import pandapower as pp
# imports from dummy structure modules
from dummy_structure_constants import *
import dummy_structure.models as mo


class Environment:
    def __init__(self, t_start: dt.datetime, t_len: int, t_step: dt.timedelta):
        self.Grid = pp.create_empty_network()
        self.Grid.Bus = []
        self.Grid.Line = []
        self.Grid.Transformer = []
        self.Load = []
        self.Generator = []
        self.Storage = []
        self.time = [t_start]
        self.clock = self.time[0]
        self.t_step = t_step.seconds/60
        for _ in range(t_len-1):
            self.time.append(self.time[-1]+t_step)
        print(self.time)
        self.df = pd.DataFrame(columns=['P_res', 'Blackout'], index=self.time)

    # def build_grid(self, filename):
    #     df = pd.read_csv(GRID_PATH+filename)
    #     for i in range(len(df['Bus'])):
    #         self.Grid.Bus.append(pp.create_bus(self.Grid, vn_kv=df['Bus_voltage'][i],
    #                                            name=df['Bus'][i], index=i))
    #     for i in range(len(df['Line'])):
    #         self.Grid.Line.append(pp.create_line(self.Grid, from_bus=df['LineBus1'][i], to_bus=df['LineBus2'][i],
    #                                              length_km=df['Line_length'][i], std_type=df['Line_type'][i],
    #                                              name=df['Line'][i], index=i))
    #     for i in range(len(df['Transformer'])):
    #         self.Grid.Transformer.append(pp.create_transformer())
    #
    # def add_load(self, profile, name=None):
    #     self.Load.append(mo.Load(profile, name))
    #
    # def add_blackouts(self, profile):
    #     self.df['Blackout'].append(profile)

    def add_generator(self, p_n, name=None, p_profile=None, gen_type='PV'):
        if gen_type == 'PV':
            self.Generator.append(mo.Photovoltaic(p_n, name=name, p_profile=p_profile))
        if gen_type == 'WEA':
            print('dummy print to add WEA')
        if gen_type == 'Diesel':
            print('dummy print to add Diesel Generator')

    def add_load(self, p_n, name=None, p_profile=None):
        self.Load.append(mo.Load(p_n, name=name, p_profile=p_profile))

    # def add_storage(self, p_n, c_n, soc=1, soc_min=0, soc_max=1, eff=1, model=None):
    #     self.Storage.append(mo.Storage(p_n, c_n, soc, soc_min, soc_max, eff, model))
