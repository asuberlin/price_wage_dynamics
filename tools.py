#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:40:32 2019

@author: JMA, GS
"""


import matplotlib.pyplot as plt

#%%

class Plots():
    def __init__(self, firmResults, householdResults, marketResults):
        self.firmResults = firmResults
        self.householdResults = householdResults
        self.marketResults = marketResults
        
        self.fig = plt.figure('results')
        plt.clf()
        # Create jelly plot
        ax1 = self.fig.add_subplot(1, 3, 1, facecolor="1.0")
        ax1.plot(self.firmResults['JSP_t'], color = 'blue', label = 'planned jelly supply')
        ax1.plot(self.firmResults['JS_t'], color = 'green', label = 'jelly supply')
        ax1.plot(self.householdResults['JD_t'], color = 'red', label = 'jelly demand')
        ax1.plot(self.marketResults['JM_t'], color = 'black', linestyle = 'dashed', label = 'jelly transactions')  
        #maxJ = max([self.firmResults['JSP_t']])
        ax1.set_ylim([0, 100])
        plt.legend()
        plt.title('jelly supply and demand')

        # Create labour plot
        ax2 = self.fig.add_subplot(1, 3, 2, facecolor="1.0")
        ax2.plot(self.firmResults['LD_t'], color = 'blue', label = 'labor demand')
        ax2.plot(self.householdResults['LS_t'], color = 'red', label = 'labor supply')
        ax2.plot(self.marketResults['LM_t'], color = 'black', linestyle = 'dashed', label = 'labor transactions')
        #maxJ = max([self.firmResults['JSP_t']])
        ax2.set_ylim([0, 400])
        plt.legend()
        plt.title('labor supply and demand')

        # Create prices plot
        ax3 = self.fig.add_subplot(1, 3, 3, facecolor="1.0")
        ax3.plot(self.firmResults['p_t'], color = 'blue', label = 'price')
        ax3.plot(self.firmResults['w_t'], color = 'red', label = 'wage')
        ax3.legend()
        ax3.set_ylim([0, 15])
        plt.legend()
        plt.title('price and wage')          



#    def stuff(self):
#        plt.figure()
#        plt.plot(self.firmResults['JSP_t'], color = 'blue', label = 'planned jelly supply')
#        plt.plot(self.firmResults['JS_t'], color = 'green', label = 'jelly supply')
#        plt.plot(self.householdResults['JD_t'], color = 'red', label = 'jelly demand')
#        plt.plot(self.marketResults['JM_t'], color = 'black', linestyle = 'dashed', label = 'jelly transactions')
#        plt.legend()
#        plt.show()
#        
#    def labor(self):
#        plt.figure()
#        plt.plot(self.firmResults['LD_t'], color = 'blue', label = 'labor demand')
#        plt.plot(self.householdResults['LS_t'], color = 'red', label = 'labor supply')
#        plt.plot(self.marketResults['LM_t'], color = 'black', linestyle = 'dashed', label = 'labor transactions')
#        plt.legend()
#        plt.show()
#        
#    def prices(self):
#        plt.figure()
#        plt.plot(self.firmResults['p_t'], color = 'blue', label = 'price')
#        plt.plot(self.firmResults['w_t'], color = 'red', label = 'wage')
#        plt.legend()
#        plt.show()

 