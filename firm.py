#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:36:36 2019

@author: JMA, GS
"""

import numpy as np
from scipy.optimize import minimize, minimize_scalar

class Firm:
    def __init__(self, firmID, firmParameters, marketParameters):  #** firm parameters in main
        self.firmID = firmID
        self.p_t = firmParameters['p_0']
        self.w_t = firmParameters['w_0']
        self.gamma = firmParameters['gamma']
        self.z_t = firmParameters['z_0']
        self.zeta_t = firmParameters['zeta_0']
        self.e1 = firmParameters['e1']
        self.e2 = firmParameters['e2']
        self.x_t = firmParameters['x_0']
        self.xi_t = firmParameters['xi_0']
        self.mF_t = firmParameters['mF_0']
        self.JSP_t = marketParameters['JM_0']
        self.JS_t = marketParameters['JM_0']
        self.LD_t = marketParameters['LM_0']
        #for multiple agents many of these parameters will become random assignments.
        
    ###functions used in firm action calls

    def phi(self, L, z, zeta, gamma):   # expected stuff demand function **
        return z / (L ** (gamma * zeta))

    def psi(self, L, x, xi, Lmax):      # expected labor supply function
        return (x / (Lmax - L)) ** (1 / xi)
        
    def optimizeL1(self, z, zeta, gamma, Lmax): #firm decides production ideal versions 1 & 2
        def f(L):
            return abs(z/L * L **(gamma*(1-zeta)) - 1)
        res = minimize_scalar(f, bounds=(0, Lmax), method='bounded')
        return(res.x)

    def optimizeL2(self, z, zeta, gamma, Lmax, x, xi): #firm decides production ideal version 3
        f = lambda L: -1 * abs(L ** gamma * (z /  L ** (gamma * zeta)) - (x / (Lmax - L)) ** (1 / xi) * L)
        res = minimize_scalar(f, bounds=(0, Lmax), method='bounded')
        return(res.x)
    
    # change optimizeL1 and optimizeL2 to maximize for more than one firm?

    def optimizeL3(self, x, xi, Lmax, m): #minimum alternative for firm decides production version 3 
        f = lambda L: abs(self.psi(L, x, xi, Lmax) - (m / L))
        res = minimize_scalar(f, bounds=(0, Lmax), method='bounded')
        return(res.x)
    
#     def expectationJ(self, z_t, zeta_t, p_t, p_tp1, gamma, L_t, L_tp1, e1, e2): 
#         f = lambda x: sqrt((np.log(p_tp1 / (x[1] / (L_tp1 ** (gamma * x[0])))) ** 2 + \
#                              e1 * np.log(p_t / (x[1] / (L_t ** (gamma * x[0]))) ** 2) / (1 + e1)) + \
#                             e2 * sqrt(np.log(x[0] / zeta_t) ** 2 + np.log(x[1] / z_t) ** 2))
#         res = minimize(f, x0 = [zeta_t, z_t], bounds = ((0, 1), (0, None)))
#         return res.x[0], res.x[1]

#     def expectationL(self, x_t, xi_t, w_t, w_tp1, Lmax, L_t, L_tp1, e1, e2): 
#         f = lambda x: sqrt((np.log(w_tp1 / ((x[1] / (Lmax - L_tp1))) ** (1 / x[0])) ** 2 + \
#                              e1 * np.log(w_t / ((x[1] / (Lmax - L_t))) ** (1 / x[0])) ** 2) / (1 + e1) + \
#                             e2 * sqrt(np.log(x[0] / xi_t) ** 2 + np.log(x[1] / x_t) ** 2 ))
#         res = minimize(f, x0 = [xi_t, x_t], bounds = ((0, None), (0, None)))
#         return res.x[0], res.x[1]
    
    def expectationJ(self, z_t, zeta_t, p_t, p_tp1, J_t, J_tp1, e1, e2):
        def f(zzeta): 
            return np.sqrt( ((np.log(p_tp1/zzeta[0]*J_tp1**zzeta[1]))**2 + e1*(np.log(p_t/zzeta[0]*J_t**zzeta[1]))**2)/(1+e1) )  + \
                e2 * np.sqrt( (np.log(zzeta[0]/z_t))**2 + (np.log(zzeta[1]/zeta_t))**2 )
        res = minimize(f, x0 = [z_t, zeta_t], method='L-BFGS-B', bounds = ((0.01, None), (0.0, 1.0)), options = {'ftol': 0.0005})
        return res.x[0], res.x[1]
    
#    def expectationL(self, x_t, xi_t, w_t, w_tp1, Lmax, L_t, L_tp1, e1, e2):
#        f = lambda x: (w_tp1 - (x[0] / (Lmax - L_tp1) ** (1 / x[1]))) ** 2 + \
#                    e1 * (w_t - (x[0] / (Lmax - L_t) ** (1 / x[1]))) ** 2 + \
#                    e2 * ((x[0] - x_t) ** 2 + np.log(x[1] - xi_t) ** 2) 
#        res = minimize(f, x0 = [x_t, xi_t], bounds = ((0, None), (0, None)))
#        return res.x[0], res.x[1]   
    
    ### firm action calls
                                
    # given expected demand and expected labor supply, plan production of stuff. 
    def decideProduction(self, money, numeraire, JM_t, Lmax):  
        if not money:                       
            #self.LD_tp1 = min(self.optimizeL1(self.z_t, self.zeta_t, self.gamma, self.p_t * JM_t), self.p_t * JM_t)
            self.LD_tp1 = min(self.optimizeL1(self.z_t, self.zeta_t, self.gamma, Lmax), self.p_t * JM_t)
            self.w_tp1 = 1
                                
        if money & (numeraire == 'wage'):
            self.LD_tp1 = min(self.optimizeL1(self.z_t, self.zeta_t, self.gamma, Lmax), self.mF_t)
            self.w_tp1 = 1
                                
        if money & (numeraire == 'money'):
            self.LD_tp1 = min(self.optimizeL2(self.z_t, self.zeta_t, self.gamma, self.x_t, self.xi_t, Lmax), 
                              self.optimizeL3(self.x_t, self.xi_t, Lmax, self.mF_t))
            self.w_tp1 = self.psi(self.LD_tp1, self.x_t, self.xi_t, Lmax)
                         
        self.JSP_tp1 = self.LD_tp1 ** self.gamma
                         
        self.p_tp1 = self.phi(self.LD_tp1, self.z_t, self.zeta_t, self.gamma)

    # given market labor result, produce stuff                     
    def produce(self, LM_tp1):
        self.JS_tp1 = LM_tp1 ** self.gamma
                         
    # update monetary holdings
    def updateLedger(self, JM_tp1, LM_tp1):
        self.mF_tp1 = self.mF_t + self.p_tp1 * JM_tp1 - self.w_tp1 * LM_tp1
                         
    # update stuff demand and labor supply function parameters
    def updateDemandFunction(self, JD_t, JD_tp1):
        #print(self.z_t, self.zeta_t)
        self.z_tp1, self.zeta_tp1 = \
            self.expectationJ(self.z_t, self.zeta_t, self.p_t, self.p_tp1, JD_t, JD_tp1, self.e1, self.e2)
    
    def updateLaborFunction(self, Lmax, LS_t, LS_tp1):                   
        self.x_tp1, self.xi_tp1 =  \
        self.expectationL(self.x_t, self.xi_t, self.w_t, self.w_tp1, Lmax, LS_t, LS_tp1, self.e1, self.e2)