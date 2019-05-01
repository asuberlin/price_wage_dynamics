class Household:
    def __init__(self, householdParameters, p_star, S_star, z_star, zeta_0):
        self.Lmax = householdParameters['Lmax']
        self.alpha = householdParameters['alpha']
        self.beta = householdParameters['beta']
        self.z = z_star
        self.zeta = zeta_0
        self.mH_t = householdParameters['mH_0'] # L_star for household has money
        self.SD_t = 0
        self.LS_t = 0
  
    # sugar demand function
    def phi(self, p): 
        return (self.z / p) ** (1 / self.zeta)

    # choose labor that maximizes utility, U = (Lmax - L) ** alpha * S ** beta, with budget p * S = w * L.
    def utility(self, alpha, beta, Lmax): 
        return (Lmax * beta) / (alpha + beta)
        
    def decideLabor(self, verbose):
        self.LS_tp1 = self.utility(self.alpha, self.beta, self.Lmax)
        if verbose: print('Household: optimal labor supply is {:.4f}'.format(self.LS_tp1))

    def decideConsumption(self, verbose, money, LM_tp1, p_tp1): 
        if not money:
            #optimum = LM_tp1 / p_tp1
            optimum = self.phi(p_tp1)
            budget = LM_tp1 / p_tp1
            self.SD_tp1 = min(optimum, budget)
            if verbose: print('Household: optimum consumption is {:.4f}, affordable is {:.4f}, so consumption is {:.4f}.'.format(optimum, budget, self.SD_tp1))
            
        if money:
            #optimum = (LM_tp1  + self.mH_t) / p_tp1
            optimum = self.phi(p_tp1) + self.mH_t / p_tp1
            if verbose: print('Household account is {:.4f}'.format(self.mH_t))
            budget = (LM_tp1 + self.mH_t) / p_tp1
            self.SD_tp1 = min(optimum, budget)
            if verbose: print('Household: optimum consumption is {:.4f}, affordable is {:.4f}, so consumption is {:.4f}.'.format(optimum, budget, self.SD_tp1))

    # update monetary holdings
    def updateLedger(self, verbose, p_tp1, SM_tp1, LM_tp1):
        self.mH_tp1 = self.mH_t + LM_tp1 - p_tp1 * SM_tp1
        if verbose: print('Household: initial ledger balance {:.4f} and new ledger balance is {:.4f}'.format(self.mH_t, self.mH_tp1))
