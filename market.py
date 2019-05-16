class Market:
    def __init__(self, S_star, L_star):
        self.sugar_t = S_star
        self.labour_t = L_star

    #determine labor market quantity 
    def laborTransaction(self, verbose, labourDemand, labourSupply):
        self.labour_tp1 = min(labourDemand, labourSupply)
        if verbose: print('Market: market labor is {:.4f}'.format(self.labour_tp1))
    
    #determine stuff market quantity
    def sugarTransaction(self, verbose, sugarDemand, sugarSupply):
        self.sugar_tp1 = min(sugarDemand, sugarSupply)
        if verbose: print('Market: market sugar is {:.4f}'.format(self.sugar_tp1))
