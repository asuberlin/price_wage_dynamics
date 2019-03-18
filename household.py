#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:37:57 2019

@author: JMA, GS
"""
import numpy as np


class Household:
    def __init__(self, householdID, householdParameters):
        self.householdID = householdID
        self.Lmax = householdParameters['Lmax']
        self.alpha = householdParameters['alpha']
        self.beta = householdParameters['beta']
        self.mH_t = householdParameters['mH_t']
        self.save = householdParameters['save']
        #for multiple agents many of these parameters will become random assignments.
        
    def decideLabor(self, numeraire, w_tp1):
        if numeraire == 'wage': 
            self.LS_tp1 = self.Lmax * (self.beta / (self.alpha + self.beta))*(1 + np.random.normal(scale = 0.01))
        
        if numeraire == 'money':
            self.LS_tp1 = self.Lmax * (self.beta / (self.alpha + self.beta)) - (self.alpha / self.alpha + self.beta) * \
            (self.mH_t / ((1 - self.save) * w_tp1))

    def decideConsumption(self, money, numeraire, LM_tp1, p_tp1, w_tp1): 
        if not money:
            self.JD_tp1 = LM_tp1 / p_tp1 * (1 + np.random.normal(scale = 0.1))
            
        if money & (numeraire == 'wage'):
            self.JD_tp1 = min(self.LS_tp1 / p_tp1, self.mH_t / p_tp1) 
            
        if money & (numeraire == 'money'):
            self.JD_tp1 = min(self.beta / (self.alpha + self.beta) * ((1 - self.s) * (w_tp1 / p_tp1) * self.Lmax + \
                                                                      self.mH_t / p_tp1), self.mH_t / p_tp1)    
    
    # update monetary holdings
    def updateLedger(self, p_tp1, JM_tp1, w_tp1, LM_tp1):
        self.mH_tp1 = self.mH_t - p_tp1 * JM_tp1 + w_tp1 * LM_tp1