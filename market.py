#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:39:01 2019

@author: JMA, GS
"""


class Market:
    def __init__(self, marketParameters):
        self.JM_t = marketParameters['JM_0']
        self.LM_t = marketParameters['LM_0']

    #determine stuff market quantity **LD and and JS are firm attributes, LS and JD are household attributes
    def laborTransaction(self, LD_tp1, LS_tp1):
        self.LM_tp1 = min(LD_tp1, LS_tp1)
    
    #determine labor market quantity
    def stuffTransaction(self, JS_tp1, JD_tp1):
        self.JM_tp1 = min(JS_tp1, JD_tp1)