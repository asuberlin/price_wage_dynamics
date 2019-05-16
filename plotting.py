import matplotlib.pyplot as plt

def plotting(L_star, S_star, p_star, firmResults, householdResults):
    #plt.clf()
    plt.figure('market results', figsize=(15,6))

    #price equilibrium and simulation
    plt.subplot(221)
    ax = plt.gca()
    firmResults.plot(kind = 'line', x = 'step', y = 'p_t', color = 'blue', ax = ax)
    plt.axhline(y = p_star, color = 'green', ls = ':')
    plt.title('price')
    ax.set_ylim([0, 50])
    
    #sugar supply, demand and equilibrium
    plt.subplot(222)
    ax = plt.gca()
    firmResults.plot(kind = 'line', x = 'step', y = 'SS_t', color = 'blue', ax = ax)
    householdResults.plot(kind = 'line', x = 'step', y = 'sugarDemand_t', color = 'red', ax = ax)
    plt.axhline(y = S_star, color = 'green', ls = ':')
    plt.title('sugar supply and demand')
    ax.set_ylim([0, 200])
    
    #labor supply, demand and equilibrium
    plt.subplot(223)
    ax = plt.gca()
    firmResults.plot(kind = 'line', x = 'step', y = 'LD_t', color = 'blue', ax = ax)
    householdResults.plot(kind = 'line', x = 'step', y = 'labourSupply_t', color = 'red', ax = ax)
    plt.axhline(y = L_star, color = 'green', ls = ':')
    plt.title('labor supply and demand')
    ax.set_ylim([0, 500])
    
    plt.show()

    #plt.savefig('../plots/Fig7aip5.pdf')


def plotZandZeta(firmResults):
    #plt.clf()
    plt.figure('expectations', figsize=(15,3))

    plt.subplot(121)
    ax = plt.gca()
    firmResults.plot(kind = 'line', x = 'step', y = 'z_t', color = 'blue', ax = ax)
    plt.title('z')
    ax.set_ylim([0, 300])

    plt.subplot(122)
    ax = plt.gca()
    firmResults.plot(kind = 'line', x = 'step', y = 'zeta_t', color = 'blue', ax = ax)
    plt.title('zeta')
    ax.set_ylim([0, 2])
    
    plt.show()
