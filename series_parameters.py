#!/usr/bin/env python
# coding: utf-8

# #### Price Dynamics via Expectations Model
# 
# Single household, single firm.
# 
# April 15, 2019
# 
# J M Applegate
# 
# from Global Climate Forum Working Paper 3/2016 by Steudle, Yang and Jaeger

def Parameters():
    directory = '../results/',
    seed = None
    duration = 10
    verbose = True

    # run variable parameters
    money_values = [False] #[True, False]
    numeraire_values = ['wage'] #['wage', 'money']

    # firm variable parameters
    gamma_values = [.7]
    zeta_0_values = [.55] #price elasticity of demand for rice in the US (2008).
    z_error_values = [-.3] #.7
    inertia_values = [.5] #[x / 10 for x in range(11)]
    eta_0_values = [1]
    x_error_values = [.3]
    mF_0_values = [0]
    expiration_values = [1] #percentage of stock which expires each timestep

    #household variable parameters
    Lmax_values = [400] 
    alpha_values = [.2] 
    beta_values = [.8] 
    mH_0_values = [0]
    saving_values = [0]

    reps = 1
    param_names = ['rep', 'money', 'numeraire', 
                   'gamma', 'zeta_0', 'z_error', 'inertia', 'eta_0', 'x_error', 'mF_0', 'expiration',
                   'Lmax', 'alpha', 'beta', 'mH_0', 'saving']

    param_sets = [[r, m, n, g, z, ze, i, e, xe, mf, ex, l, a, b, mh, s] for r in list(range(reps)) for m in money_values for n in numeraire_values for g in gamma_values for z in zeta_0_values
                  for ze in z_error_values for i in inertia_values for e in eta_0_values for xe in x_error_values
                  for mf in mF_0_values for ex in expiration_values for l in Lmax_values for a in alpha_values for b in beta_values for mh in mH_0_values for s in saving_values]

    simulation_list = [dict(zip(param_names, p)) for p in param_sets]
    runs = len(param_sets)
    print('This experiment is', runs, 'runs.')

    r = 0
    p = simulation_list[r]

    runParameters = {'duration': duration,
                        'directory': directory,
                        'seed': seed,
                        'verbose': verbose,
                        'money': p['money'],
                        'numeraire': p['numeraire']}

    firmParameters = {'gamma': p['gamma'],
                        'zeta_0': p['zeta_0'], 
                        'z_error': p['z_error'],
                        'inertia': p['inertia'],
                        'eta_0': p['eta_0'],
                        'x_error': p['x_error'],
                        'mF_0': p['mF_0'],
                        'expiration': p['expiration']}

    householdParameters = {'Lmax': p['Lmax'], 
                            'alpha': p['alpha'], 
                            'beta': p['beta'], 
                            'mH_0': p['mH_0'], 
                            'saving': p['saving']}
    
    return(runParameters, firmParameters, householdParameters)
