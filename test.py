#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:42:44 2019

@author: GS, JMA
"""

from firm import Firm
import matplotlib.pyplot as plt
import numpy as np

class TestHousehold():
    def __init__(self, z=20, zeta = 0.5, randomized = False):
        self.z = z
        self.zeta = zeta
        self.randomized = randomized
        
    def demand(self, p):
        if self.randomized:
            demand = (self.z/p)**(1/self.zeta) * min(max(1 + np.random.normal(scale=0.01),0.5),1.5)
        else: 
            demand = (self.z/p)**(1/self.zeta) 
        return demand

        
 #%% === init ===   
      
firmParameters = {'gamma': .7, 
                  'p_0': 5, 
                  'w_0': 1,
                  'z_0': 20, 
                  'zeta_0': 0.3, 
                  'e1': 0.6, 
                  'e2': 0.4, 
                  'x_0': 1, 
                  'xi_0': 1, 
                  'mF_0': 1}

marketParameters = {'JM_0': 9,
                    'LM_0': 320}

firm = Firm(0, firmParameters, marketParameters)
household = TestHousehold(z=15, zeta=0.5, randomized=True)
print(household.randomized)
prices = list()
zlist = list()
zetalist = list()

#%% === run ===

time = 30

J_t = marketParameters['JM_0']
JD_t = marketParameters['JM_0']

for time in range(time):
    prices.append(firm.p_t)
    zlist.append(firm.z_t)
    zetalist.append(firm.zeta_t)     
    firm.decideProduction(False, 'wage', J_t, 400)
    JD_tp1 = household.demand(firm.p_tp1)
    print(JD_tp1)
    J_tp1  = min(firm.JSP_tp1, JD_tp1)
    print(J_tp1)
    firm.z_tp1, firm.zeta_tp1 = firm.expectationJ(firm.z_t, firm.zeta_t, firm.p_t, firm.p_tp1, JD_t, JD_tp1, firm.e1, firm.e2)
    print([firm.z_tp1, firm.zeta_tp1])
    firm.p_t, J_t, JD_t, firm.z_t, firm.zeta_t = firm.p_tp1, J_tp1, JD_tp1, firm.z_tp1, firm.zeta_tp1


#%% === plot results ===

plt.figure('test_results')
plt.clf()
ax1 = plt.subplot(1,3,1)    
ax1.plot(prices)
ax1.set_ylim(0, None)
plt.title('prices')

ax2 = plt.subplot(1,3,2) 
ax2.plot(zlist)
ax2.plot([household.z for x in range(time)], linestyle = 'dashed')
ax2.set_ylim(0, None)
plt.title('firm: z')

ax3 = plt.subplot(1,3,3) 
ax3.plot(zetalist)
ax3.plot([household.zeta for x in range(time)], linestyle = 'dashed')
ax3.set_ylim(0, 1)
plt.title('firm: zeta')

    
        