import pandas as pd

from firm import Firm
from household import Household
from market import Market

class Simulation():
    def __init__(self, runParameters, firmParameters, householdParameters):
        
        self.runParameters = runParameters
        self.firmParameters = firmParameters
        self.householdParameters = householdParameters
        
        self.duration = runParameters['duration']
        self.money = runParameters['money']
        self.stock = runParameters['stock']
        self.verbose = runParameters['verbose']
        self.expectation = runParameters['expectation']
        self.demandKnown = runParameters['demandKnown']
        
    def equilibrium(self, money, householdParameters, firmParameters):
        Lmax = householdParameters['Lmax']
        alpha = householdParameters['alpha']
        beta = householdParameters['beta']
        gamma = firmParameters['gamma']
        zeta_0 = firmParameters['zeta_0']

        L_star = beta / (alpha + beta) * Lmax
        p_star = L_star ** (1 - gamma)
        S_star = L_star ** gamma
        z_star = p_star * S_star ** zeta_0
        print('Equilibrium values are: p = {:.4f}, S = {:.4f}, L = {:.4f}, z = {:.4f}'.format(p_star, S_star, L_star, z_star))
    
        return(p_star, L_star, S_star, z_star)
   
    def saveSimResults(self):
        self.firmSimResults = self.firmSimResults.append(self.firm.__dict__, ignore_index = True)
        self.householdSimResults = self.householdSimResults.append(self.household.__dict__, ignore_index = True)
        self.marketSimResults = self.marketSimResults.append(self.market.__dict__, ignore_index = True)
        
    def advanceAttributes(self):
        self.market.SM_t, self.market.LM_t = self.market.SM_tp1, self.market.LM_tp1
            
        self.firm.LD_t, self.firm.SSP_t, self.firm.SS_t = self.firm.LD_tp1, self.firm.SSP_tp1, self.firm.SS_tp1 
        self.firm.p_t = self.firm.p_tp1
        self.firm.z_t, self.firm.zeta_t = self.firm.z_tp1, self.firm.zeta_tp1
        if self.stock: self.firm.stock_t = self.firm.stock_tp1
        if self.money: self.firm.mF_t = self.firm.mF_tp1
                
        self.household.LS_t, self.household.SD_t = self.household.LS_tp1, self.household.SD_tp1
        if self.money: self.household.mH_t = self.household.mH_tp1
    
    def Run(self):
        self.p_star, self.L_star,self.S_star, self.z_star = self.equilibrium(self.money, self.householdParameters, self.firmParameters)
        
        self.firm = Firm(self.money, self.firmParameters, self.p_star, self.S_star, self.L_star, self.z_star, self.expectation) 
        self.household = Household(self.householdParameters, self.p_star, self.S_star, self.z_star, self.firm.zeta_0)
        self.market = Market(self.S_star, self.L_star)
        
        self.firmSimResults = pd.DataFrame()
        self.householdSimResults = pd.DataFrame()
        self.marketSimResults = pd.DataFrame()

        for t in range(self.duration):
            
            if self.verbose: print('\nstep ', str(t + 1))
            #add time step as instance attribute
            self.market.step = t + 1
            self.firm.step = t + 1
            self.household.step = t + 1
            
            #firms plan sugar production
            self.firm.decideProduction(self.verbose, self.money, self.market.SM_t, self.household.Lmax)

            #households decide labor supply
            self.household.decideLabor(self.verbose)
            
            #market decides labor supply
            self.market.laborTransaction(self.verbose, self.firm.LD_tp1, self.household.LS_tp1)
            
            #firms produce sugar
            self.firm.produce(self.verbose, self.market.LM_tp1)
            
            #households decide sugar consumption
            self.household.decideConsumption(self.verbose, self.money, self.market.LM_tp1, self.firm.p_tp1)
            
            #market decides demand for sugar
            self.market.stuffTransaction(self.verbose, self.firm.SS_tp1, self.household.SD_tp1)
            
            #update firm stock
            if self.stock: self.firm.updateStock(self.verbose, self.market.SM_tp1)
        
            #update firm ledgers
            if self.money: self.firm.updateLedger(self.verbose, self.market.SM_tp1, self.market.LM_tp1) 
        
            #no labor curve updating first round
            if t == 0: self.market.LM_t = self.market.LM_tp1 
            
            #update sugar demand an labor supply function parameters
            if self.demandKnown:
                self.firm.updateExpectations(self.verbose, self.money, self.household.SD_t, self.household.SD_tp1, self.market.LM_tp1, self.market.LM_t, self.market.LM_tp1)
            else:
                self.firm.updateExpectations(self.verbose, self.money, self.market.SM_t, self.market.SM_tp1, self.market.LM_tp1, self.market.LM_t, self.market.LM_tp1)
                        
            #update household ledgers
            if self.money: 
                self.household.updateLedger(self.verbose, self.firm.p_tp1, self.market.SM_tp1, self.market.LM_tp1)
                    
            #save step results
            self.saveSimResults()
            
            # update timed variables
            self.advanceAttributes()
                    
            #print('step', t + 1, 'complete')
        
        print('Final simulation values are: p = {:.4f}, S = {:.4f}, L = {:.4f}'.format(self.firm.p_tp1, self.market.SM_t, self.market.LM_t))
            
        return self.firmSimResults, self.householdSimResults, self.marketSimResults
