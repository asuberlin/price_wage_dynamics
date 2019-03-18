#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:32:40 2019

@author: JMA, GS
"""

#from scipy.optimize import minimize, minimize_scalar
#from statistics import mean
import numpy as np

from firm import Firm
from household import Household
from market import Market
from simulation import Simulation
from tools import Plots


#%% ===== configure parameters =====

simulationParameters = {'numFirms': 1, 
                        'numHouseholds': 1,
                        'duration': 100,
                        'money': False,
                        'numeraire': 'wage', # 'wage' or 'money'
                        'directory': '../results/',
                        'seed': None}

firmParameters = {'gamma': .7, 
                  'p_0': 5.64, 
                  'w_0': 1,
                  'z_0': 16, 
                  'zeta_0': 0.55, 
                  'e1': 0.99, 
                  'e2': 0.9, 
                  'x_0': 1, 
                  'xi_0': 1, 
                  'mF_0': 1}

householdParameters = {'Lmax': 400, 
                       'alpha': 0.2, 
                       'beta': 0.8, 
                       'mH_t': 1, 
                       'save': 0.5}

marketParameters = {'JM_0': 56.7,
                    'LM_0': 320}


# get equilibrium values
Lmax = householdParameters['Lmax']
alpha = householdParameters['alpha']
beta = householdParameters['beta']
gamma = firmParameters['gamma']
w = 1
p = list(range(1,10))

L_star = round(beta / (alpha + beta) * Lmax, 3)
#J_star = [(w * L_star) / i for i in p]
p_star = round(pow(L_star, 1 - gamma), 3)
J_star = round(L_star ** gamma, 3)
print('Equilibrium values are: p = ' + str(p_star) + ', L = ' + str(L_star) + ', J = ' + str(J_star))


#%% ===== run simulation =====

SimID = 1 # This and parameter files will come through wrapper
simulation = Simulation(SimID, simulationParameters, firmParameters, householdParameters, marketParameters)
firmResults, householdResults, marketResults = simulation.run()


#%% ===== plot results =====

plots = Plots(firmResults, householdResults, marketResults)

