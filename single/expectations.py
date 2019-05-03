from scipy.optimize import minimize, curve_fit
import numpy as np

# original ##########################################################
def original(z_t, zeta_t, p_t, p_tp1, S_t, S_tp1, e1, e2, inertia, memory, memoryLength): 
    f = lambda x: np.sqrt((np.log(p_tp1 / (x[0] / S_tp1 ** x[1])) ** 2 + \
                           e1 * np.log(p_t / (x[0] / S_t ** x[1])) ** 2) / (1 + e1)) + \
                        e2 * np.sqrt(np.log(x[0] / z_t) ** 2 + np.log(x[0] / zeta_t) ** 2)
    res = minimize(f, x0 = [z_t, zeta_t], bounds = ((0, None), (0, 1)))
    return res.x[0], res.x[1]

        
# differential ##########################################################
def differential(z_t, zeta_t, p_t, p_tp1, S_t, S_tp1, e1, e2, inertia, memory, memoryLength):
#    f = lambda x: (p_tp1 - (x[0] / S_tp1 ** x[1])) ** 2 + e1 * (p_t - (x[0] / S_t ** x[1])) ** 2 + \
#    e2 * ((x[0] - z_t) ** 2 + (x[1] - zeta_t) ** 2)
    f = lambda x: (p_tp1 - (x[0] / S_tp1 ** x[1])) ** 2 + e1 * (p_t - (x[0] / S_t ** x[1])) ** 2 + \
    e2 * (((x[0] - z_t)/z_t) ** 2 + ((x[1] - zeta_t)/zeta_t) ** 2)
    res = minimize(f, x0 = [z_t, zeta_t], bounds = ((0, None), (0, 1)))
    return res.x[0], res.x[1]
    
# functional ############################################################
def calcZandZeta(S1, p1, S2, p2):
    zeta = abs(np.log(p2 / p1) / np.log(S1 / S2))
    z = p1 * S1 ** zeta
    return z, zeta

def functional(z_t, zeta_t, p_t, p_tp1, S_t, S_tp1, e1, e2, inertia, memory, memoryLength):
    z, zeta = calcZandZeta(S_t, p_t, S_tp1, p_tp1)
    z_tp1 = inertia * z_t + (1 - inertia) * z
    zeta_tp1 = inertia * zeta_t + (1 - inertia) * zeta
    return z_tp1, zeta_tp1
    
# memory #################################################################
# need to set memory and memoryLength in init    
def updateMemory(s_new, p_new, memory, memoryLength):
    oldMemory = memory
    memLen = int(memoryLength)
    #print(oldMemory)
    newMemory = np.array([np.zeros(memLen),np.zeros(memLen)])
    for i in range(1, memLen):
        newMemory[0][memLen-i] = oldMemory[0][memLen-1-i]
        newMemory[1][memLen-i] = oldMemory[1][memLen-1-i]
    newMemory[0][0], newMemory[1][0] = s_new, p_new
    #print(newMemory)
    return newMemory
    
def memoryEx(z_t, zeta_t, p_t, p_tp1, S_t, S_tp1, e1, e2, inertia, memory, memoryLength):
    memory = updateMemory(S_tp1, p_tp1, memory, memoryLength)
    def phi(stuff, z, zeta): 
        return z/(stuff**zeta)
    fit = curve_fit(phi, memory[0], memory[1],[z_t,zeta_t])
    z, zeta = max(0.01,fit[0][0]), min(0.99,max(0.01,fit[0][1]))
    #print(z,zeta)
    return z, zeta

