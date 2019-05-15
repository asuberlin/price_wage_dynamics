from scipy.optimize import minimize, minimize_scalar, basinhopping
from statistics import mean
import pandas as pd
import numpy as np
import random as rand
import matplotlib.pyplot as plt

from parameters import Parameters
from firm import Firm
from household import Household
from market import Market
from simulation import Simulation
from tools2 import Plotting
from series import Start

series = 'April17'
directory = '../results/'
seed = None

duration = 10
verbose = False

series = Series(duration, verbose)
firmResults, householdResults, marketResults = series.start()
