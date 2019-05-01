class Series():  
    def __init__(self):
        self.firmResults = pd.DataFrame()
        self.householdResults = pd.DataFrame()
        self.marketResults = pd.DataFrame()
    
    def saveResults(self):
        self.firmResults = self.firmResults.append(self.firmSimResults)
        self.householdResults = self.householdResults.append(self.householdSimResults)
        self.marketResults = self.marketResults.append(self.marketSimResults)
        
    def Start(self):
        #construct series parameter sets
        self.duration, self.verbose, self.param_sets = Parameters()

        for i, p in enumerate(self.param_sets):
            self.runParameters = {'id': i,
                                'duration': self.duration,
                                'verbose': self.verbose,
                                'money': p['money'],
                                'numeraire': p['numeraire']}

            self.firmParameters = {'gamma': p['gamma'],
                                'zeta_0': p['zeta_0'], 
                                'z_error': p['z_error'],
                                'inertia': p['inertia'],
                                'eta_0': p['eta_0'],
                                'x_error': p['x_error'],
                                'mF_0': p['mF_0'],
                                'expiration': p['expiration']}

            self.householdParameters = {'Lmax': p['Lmax'], 
                                    'alpha': p['alpha'], 
                                    'beta': p['beta'], 
                                    'mH_0': p['mH_0'], 
                                    'saving': p['saving']}

            self.sim = Simulation(self.runParameters, self.firmParameters, self.householdParameters)
            self.firmSimResults, self.householdSimResults, self.marketSimResults = self.sim.Run()
            Plotting(self.sim.L_star, self.sim.S_star, self.sim.p_star, self.firmSimResults, self.householdSimResults)
            self.saveResults()
            
        return(self.firmResults, self.householdResults, self.marketResults)
