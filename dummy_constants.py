"""This is the dummy_constants module of dummy_structure providing global system constants.
The dummy_structure shows a suggestion for an objective-oriented programming approach to use as a standard in the
Python-AG of the Cologne Institute for Renewable Energy (CIRE) at the University of Applied Sciences Cologne (TH Köln).
"""
__version__ = '0.1'
__author__ = 'srummmeny'

import os
import datetime as dt

ROOT_PATH: str = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/') + '/'
TIME_SERIES_PATH: str = os.path.join(ROOT_PATH, 'dummy_structure/data/')
GRID_PATH: str = os.path.join(ROOT_PATH, 'dummy_structure/grids/data/')
CONFIG_PATH: str = os.path.join(ROOT_PATH, 'dummy_structure/config/')

START_TIME = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(dt.datetime.now().year, dt.datetime.now().month,
                                                           dt.datetime.now().day, dt.datetime.now().hour,
                                                           dt.datetime.now().minute, dt.datetime.now().second)
RESULT_PATH = os.path.join(ROOT_PATH, 'dummy_structure/results/', START_TIME)
os.mkdir(RESULT_PATH)
