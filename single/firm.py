from scipy.optimize import minimize, minimize_scalar, basinhopping, curve_fit
import numpy as np

class Firm:
    def __init__(self, money, firmParameters, p_star, S_star, L_star, z_star, expectation):
        self.gamma = firmParameters['gamma']
        self.p_t = p_star
        self.zeta_0 = firmParameters['zeta_0']
        self.zeta_t = self.zeta_0
        self.error = firmParameters['error']
        self.z_star = z_star
        self.z_t = z_star * (1 + self.error)
        self.inertia = firmParameters['inertia']
        self.e1 = firmParameters['e1']
        self.e2 = firmParameters['e2']
        self.mF_t = L_star if money else firmParameters['mF_0']
        self.stock = 0
        self.expiration = firmParameters['expiration']
        self.SSP_t = S_star
        self.SS_t = S_star
        self.LD_t = L_star

        self.expectation = expectation # desired expectation function
        
        self.memoryLength = 5 # for memory expectation
        self.memory = self.initMemory() # for memory expectation

    # for memory expectation
    def initMemory(self):
        memory = np.array([np.zeros(self.memoryLength),np.zeros(self.memoryLength)])
        for i in range(int(self.memoryLength)):
            memory[0][i] = max(0.001,self.SS_t*(1+np.random.normal(loc = 0.0, scale = 0.05))) 
            memory[1][i] = (self.z_star / memory[0][i] ** self.zeta_t) 
        #print(memory)
        return memory
        
    ### functions used in firm action calls
        
    # firm production function
    def rho(self, L, gamma):
        return L ** gamma

    # sugar demand function
    def phi(self, L, z, zeta, gamma): 
        return z / self.rho(L, gamma) ** zeta
        
    # used in firm decides production 
    def optimizeL(self, z, zeta, gamma, Lmax): #firm decides production ideal versions 1 & 2
        f = lambda L: abs(self.rho(L, gamma) * self.phi(L, z, zeta, gamma) - L)
        res = minimize_scalar(f, bounds=(0, Lmax), method='bounded')
        return(res.x)
        
    # original expectation function, now read in through expectations.py in parameter file and passed via simulation
        
#    def expectation(self, z_t, zeta_t, p_t, p_tp1, S_t, S_tp1, inertia, e1, e2): 
#        f = lambda x: np.sqrt((np.log(p_tp1 / (x[0] / S_tp1 ** x[1])) ** 2 + \
#                               e1 * np.log(p_t / (x[0] / S_t ** x[1])) ** 2) / (1 + e1)) + \
#                            e2 * np.sqrt(np.log(x[0] / z_t) ** 2 + np.log(x[0] / zeta_t) ** 2)
#        res = minimize(f, x0 = [z_t, zeta_t], bounds = ((0, None), (0, 1)))
#        return res.x[0], res.x[1]

    ### firm action calls
                                
    # given expected demand and expected labor supply, plan production of stuff. 
    def decideProduction(self, verbose, money, SM_t, Lmax):  
        if not money: 
            optimum = self.optimizeL(self.z_t, self.zeta_t, self.gamma, Lmax)
            budget = self.p_t * SM_t
            self.LD_tp1 = min(optimum, budget)
            self.w_tp1 = 1
            if verbose: print('Firm: optimum labor is {:.4f}, affordable is {:.4f}, so planned labor is {:.4f}.'.format(optimum, budget, self.LD_tp1))
                                
        if money:
            optimum = self.optimizeL(self.z_t, self.zeta_t, self.gamma, Lmax)
            budget = self.mF_t
            self.LD_tp1 = min(optimum, budget)
            self.w_tp1 = 1
            if verbose: print('Firm: optimum labor is {:.4f}, affordable is {:.4f}, so planned labor is {:.4f}.'.format(optimum, budget, self.LD_tp1))
                                                         
        self.SSP_tp1 = self.rho(self.LD_tp1, self.gamma)                  
        self.p_tp1 = self.phi(self.LD_tp1, self.z_t, self.zeta_t, self.gamma)
        if verbose: print('Firm: planned production is {:.4f} and price is {:.4f}'.format(self.SSP_tp1, self.p_tp1))
        
    # given market labor result, produce stuff                     
    def produce(self, verbose, LM_tp1):
        self.SS_tp1 = self.rho(LM_tp1, self.gamma)
        if verbose: print('Firm: Firm produces {:.4f}'.format(self.SS_tp1))
                         
    # update monetary holdings
    def updateLedger(self, verbose, SM_tp1, LM_tp1):
        self.mF_tp1 = self.mF_t + self.p_tp1 * SM_tp1 - LM_tp1
        if verbose: print('Firm: initial ledger balance {:.4f} and new ledger balance is {:.4f}'.format(self.mF_t, self.mF_tp1))
                         
    # update stuff demand and labor supply function parameters
    def updateExpectations(self, verbose, money, SM_t, SM_tp1, Lmax, LS_t, LS_tp1):
        if verbose: print('Old p and new p are {:.4f} and {:.4f}, old S and new S are {:.4f} and {:.4f}'.format(self.p_t, self.p_tp1, SM_t, SM_tp1))
        self.z_tp1, self.zeta_tp1 =  self.expectation(self.z_t, self.zeta_t, self.p_t, self.p_tp1, SM_t, SM_tp1, self.e1, self.e2, self.inertia, self.memory, self.memoryLength)
        if verbose: print('Firm: initial z and zeta: {:.4f} {:.4f}, and adjusted z and zeta: {:.4f} {:.4f}'.format(self.z_t, self.zeta_t, self.z_tp1, self.zeta_tp1))
