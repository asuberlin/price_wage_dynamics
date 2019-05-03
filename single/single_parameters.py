#!/usr/bin/env python
# coding: utf-8

# #### Price Dynamics via Expectations Model
# 
# Single household, single firm.
# 
# May 1, 2019
# 
# J M Applegate
# 
# from Global Climate Forum Working Paper 3/2016 by Steudle, Yang and Jaeger

# commonly modified: duration, verbose, expectation, money mF_0, mH_0

# allows for selection of expectation algorithm from expectations.py
from expectations import original, differential, functional, memoryEx

def Parameters():
    directory = '../results/',
    seed = None
    duration = 50
    verbose = True
    expectation = functional # which expectation function to use: one of those imported from expectations
    demandKnown = True     #determines whether the firm knows the actual stuff demand

    # run variable parameters
    money = True #[True, False]

    # firm variable parameters
    gamma  = .7
    zeta_0 = .55
    # own price elasticity of demand for rice is .55 (US 2008, Wikipedia)
    # own price elasticity of demand for sugar is .79 (UK 1988 - 2000 Lechene)
    error = -.7  # percentage error in z_0; z_star * (1 + self.error)
    e1 = .9      # for original and differential expectation functions 
    e2 = .1
    inertia = .5 # for functional expectation function
    mF_0 = 320   # ignored if money False
    expiration = 1 # percentage of stock which expires each timestep

    # household variable parameters
    Lmax  = 400
    alpha = .2
    beta  = .8
    mH_0  = 30    # ignored if money False

    runParameters = {'duration': duration,
                    'directory': directory,
                    'seed': seed,
                    'verbose': verbose,
                    'money': money,
                    'expectation': expectation, 
                    'demandKnown': demandKnown}

    firmParameters = {'gamma': gamma,
                      'zeta_0': zeta_0,
                      'error': error,
                      'inertia': inertia,
                      'e1': e1,
                      'e2':  e2,
                      'mF_0': mF_0,
                      'expiration': expiration}

    householdParameters = {'Lmax': Lmax,
                           'alpha': alpha,
                           'beta': beta,
                           'mH_0': mH_0}
    
    return(runParameters, firmParameters, householdParameters)
