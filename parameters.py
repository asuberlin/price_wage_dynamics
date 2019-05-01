#destined for parameters.py
def Parameters():
    # run variable parameters
    money_values = [False] #[True, False]
    numeraire_values = ['wage'] #['wage', 'money']

    # firm variable parameters
    gamma_values = [.7]
    zeta_0_values = [.55] #price elasticity of demand for rice in the US (2008).
    z_error_values = [.7]
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
    
    param_names = ['money', 'numeraire', 
                   'gamma', 'zeta_0', 'z_error', 'inertia', 'eta_0', 'x_error', 'mF_0', 'expiration',
                   'Lmax', 'alpha', 'beta', 'mH_0', 'saving']

    param_lists = [[m, n, g, z, ze, i, e, xe, mf, ex, l, a, b, mh, s] for m in money_values for n in numeraire_values for g in gamma_values for z in zeta_0_values
                  for ze in z_error_values for i in inertia_values for e in eta_0_values for xe in x_error_values
                  for mf in mF_0_values for ex in expiration_values for l in Lmax_values for a in alpha_values for b in beta_values for mh in mH_0_values for s in saving_values]

    param_sets = [dict(zip(param_names, p)) for p in param_lists]
    runs = len(param_lists)
    print('This session is', runs, 'runs.')
    
    return(param_sets)