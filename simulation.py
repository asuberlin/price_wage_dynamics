#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:40:09 2019

@author: JMA, GS
"""

import numpy as np
import pandas as pd

from firm import Firm
from household import Household
from market import Market

#%%

class Simulation:
    def __init__(self, SimID, simulationParameters, firmParameters, householdParameters, marketParameters):
        self.SimID = SimID
        
        self.firmParameters = firmParameters
        self.householdParameters = householdParameters
        self.marketParameters = marketParameters
        
        self.numFirms = simulationParameters['numFirms']
        self.numHouseholds = simulationParameters['numHouseholds']
        self.duration = simulationParameters['duration']
        self.money = simulationParameters['money']
        self.numeraire = simulationParameters['numeraire']
        self.directory = simulationParameters['directory']
        self.seed = simulationParameters['seed']
        
    #create agent
    def createFirms(self):
        self.firms = []
        for i in range(self.numFirms):
            self.firms.append(Firm(i, self.firmParameters, self.marketParameters))
        return self.firms
        
    #create households
    def createHouseholds(self):
        self.households = []
        for i in range(self.numHouseholds):
            self.households.append(Household(i, self.householdParameters))
        return self.households
    
    def saveResults(self):
        for f in self.firms:
            self.firmResults = self.firmResults.append(f.__dict__, ignore_index = True)
        for h in self.households: 
            self.householdResults = self.householdResults.append(h.__dict__, ignore_index = True)
        self.marketResults = self.marketResults.append(self.market.__dict__, ignore_index = True)
        
    def advanceAttributes(self):
        self.market.JM_t, self.market.LM_t = self.market.JM_tp1, self.market.LM_tp1
            
        for f in self.firms:
            f.LD_t, f.JSP_t, f.JS_t = f.LD_tp1, f.JSP_tp1, f.JS_tp1 
            f.p_t, f.w_t = f.p_tp1, f.w_tp1
            if self.money: f.mF_t, f.x_t, f.xi_t = f.mF_tp1, f.x_tp1, f.xi_tp1
            f.z_t, f.zeta_t = f.z_tp1, f.zeta_tp1
                
        for h in self.households:
            h.LS_t, h.JD_t = h.LS_tp1, h.JD_tp1
            if self.money: h.mH_t = h.mH_tp1
    
    def run(self):

        self.firms = self.createFirms() 
        self.households = self.createHouseholds()
        self.market = Market(self.marketParameters)
        
        self.firmResults = pd.DataFrame()
        self.householdResults = pd.DataFrame()
        self.marketResults = pd.DataFrame()

        for t in range(self.duration):
            
            #add time step as instance attribute
            self.market.step = t
            for f in self.firms: f.step = t
            for h in self.households: h.step = t
    
            #calculate mean Lmax for firm production estimates
            self.meanLmax = np.mean([h.Lmax for h in self.households])
            
            #firms plan production
            for f in self.firms:
                f.decideProduction(self.money, self.numeraire, self.market.JM_t, self.meanLmax)
            
            #aggregate and average firm production plans
            self.AggLD = sum([f.LD_tp1 for f in self.firms])
            self.AggJSP = sum([f.JSP_tp1 for f in self.firms])
            self.meanWage = np.mean([f.w_tp1 for f in self.firms])
            self.meanPrice = np.mean([f.p_tp1 for f in self.firms])
            
            #households decide labor supply
            for h in self.households:
                h.decideLabor(self.numeraire, self.meanWage)
            
            #aggregate household labor supply
            self.AggLS = sum([h.LS_tp1 for h in self.households])
            
            #market decides labor supply
            self.market.laborTransaction(self.AggLD, self.AggLS)
            
            #firms produce
            for f in self.firms:
                f.produce(self.market.LM_tp1)
            
            #aggregate firm production
            self.AggJS = sum([f.JS_tp1 for f in self.firms])
            
            #households decide consumption
            for h in self.households:
                h.decideConsumption(self.money, self.numeraire, self.market.LM_tp1, self.meanPrice, self.meanWage)
            
            #aggregate household consumption
            self.AggJD = sum([h.JD_tp1 for f in self.households])
            
            #market decides demand for stuff
            self.market.stuffTransaction(self.AggJS, self.AggJD)
        
            #update firm ledgers
            if self.money: 
                for f in self.firms:
                    f.updateLedger(self.AggJD / self.numFirms, self.market.LM_tp1 / self.numFirms) 
                    ##Wrong, needs to be heterogenously divided between firms.
        
            #no labor curve updating first round
            if t == 0: self.market.LM_t = self.market.LM_tp1 
            
            #update stuff demand function parameters
            for f in self.firms:
                f.updateDemandFunction(self.market.LM_t, self.market.LM_tp1)

            #update labor supply function parameters
            if self.money: 
                for f in self.firms:
                    f.updateLaborFunction(self.meanLmax, self.market.LM_t, self.market.LM_tp1)
            
            #update household ledgers
            if self.money: 
                for h in self.households:
                    h.updateLedger(self.meanPrice, self.market.JM_tp1 / self.numHouseholds, self.meanWage, 
                                   self.market.LM_tp1 / self.numHouseholds)
                    ##Wrong, needs to be heterogenously divided between households.
                    
            #save step results
            self.saveResults()
            
            # update timed variables
            self.advanceAttributes()
                    
            #print('step', t, 'complete')
            
        return self.firmResults, self.householdResults, self.marketResults