class Market:
    def __init__(self, S_star, L_star):
        self.SM_t = S_star
        self.LM_t = L_star

    #determine labor market quantity 
    def laborTransaction(self, verbose, LD_tp1, LS_tp1):
        self.LM_tp1 = min(LD_tp1, LS_tp1)
        if verbose: print('Market: market labor is {:.4f}'.format(self.LM_tp1))
    
    #determine stuff market quantity
    def stuffTransaction(self, verbose, SS_tp1, SD_tp1):
        self.SM_tp1 = min(SS_tp1, SD_tp1)
        if verbose: print('Market: market sugar is {:.4f}'.format(self.SM_tp1))
