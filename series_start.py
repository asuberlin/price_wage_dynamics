from scipy.optimize import minimize, minimize_scalar, basinhopping, curve_fit
from statistics import mean
import pandas as pd
import numpy as np
import random as rand
import matplotlib.pyplot as plt

series = 'April17'
directory = '../results/'
seed = None

def log(x): return np.log(x)
    
def sqrt(x): return np.sqrt(x)

series = Series()
firmResults, householdResults, marketResults = series.Start()

#firmResults.to_csv(runParameters['directory'] + 'Series' + str(series) + 'Firm.csv')
#householdResults.to_csv(runParameters['directory'] + 'Series' + str(series) + 'Household.csv')
#marketResults.to_csv(runParameters['directory'] + 'Series' + str(series) + 'Market.csv')
