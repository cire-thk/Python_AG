"""This is the simulation module of dummy_structure providing simulation options for an energy system simulation.
The dummy_structure shows a suggestion for an objective-oriented programming approach to use as a standard in the
Python-AG of the Cologne Institute for Renewable Energy (CIRE) at the University of Applied Sciences Cologne (TH Köln).
"""
__version__ = '0.1'
__author__ = 'srummmeny'

import pandas as pd
import matplotlib.pyplot as plt
# imports from dummy structure modules
from dummy_structure_constants import *
import dummy_structure.environment as en
import dummy_structure.operation as op


class Simulation:
    def __init__(self, files):
        self.df = []
        # load and format csv file from data/
        for f in range(len(files)):
            self.df.append(pd.read_csv(TIME_SERIES_PATH + files[f], sep=';', index_col=0, na_values=' '))
            self.df[-1].index = pd.to_datetime(self.df[-1].index, format='%d.%m.%y %H:%M')
            self.df[-1] = self.df[-1].stack().str.replace(',', '.').unstack()
            self.df[-1] = self.df[-1].rename(columns={'P [kW]': 'P_in'})
            self.df[-1]['P_in'] = self.df[-1]['P_in'].astype(float)
        # init environment
        t_start = self.df[-1].index[0]
        t_len = len(self.df[-1].index)
        t_step = self.df[-1].index[1] - self.df[-1].index[0]
        self.env = en.Environment(t_start, t_len, t_step)
        # init operator
        self.op = []

    def reference_scenario_sim(self, inputs):
        """ Execution of a simulation of the reference dummy_structure system design scenario
        """
        self.env.add_load(inputs[0][0], name=inputs[0][1], p_profile=self.df[0])
        self.env.Generator = []     # delete all generators if there where any
        self.op = op.Operator(self.env)
        env = self.op.reference_strategy()
        return env

    def single_scenario_sim(self, inputs, p_limit):
        """ Execution of a simulation of one particular dummy_structure system design scenario
        """
        self.env.add_load(inputs[0][0], name=inputs[0][1], p_profile=self.df[0])
        self.env.add_generator(inputs[1][0], name=inputs[1][1], p_profile=self.df[1])
        self.op = op.Operator(self.env)
        env = self.op.dummy_strategy(p_limit)
        return env


if __name__ == '__main__':
    filenames = ['sample_load_1day.csv', 'sample_pv_1day.csv']
    input_data = [[10, 'Load_Meyerstr_12'], [65, 'PV_Meyerstr_12']]
    limit = 30
    sim_ref = Simulation(filenames)
    result_env_ref = sim_ref.reference_scenario_sim(input_data)
    sim1 = Simulation(filenames)
    result_env_sim1 = sim1.single_scenario_sim(input_data, limit)

    plt.figure()
    plt.plot(result_env_ref.df['P_res'])
    plt.plot(result_env_sim1.df['P_res'])
    plt.legend(['Reference (just Load)', '+ '+str(65)+' kWp PV & feed-in-limit of '+str(limit)+' kW'])
    plt.ylabel('Residual Load [kW]')
    plt.xlabel('Time')
    plt.show()
