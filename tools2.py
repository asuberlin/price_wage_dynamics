def Plotting(L_star, S_star, p_star, firmResults, householdResults):
    plt.clf()
    plt.figure(1, figsize=(15,3))

    #price equilibrium and simulation
    plt.subplot(131)
    ax = plt.gca()
    firmResults.plot(kind = 'line', x = 'step', y = 'p_t', color = 'blue', ax = ax)
    plt.axhline(y = p_star, color = 'green', ls = ':')
    plt.title('price')
    ax.set_ylim([0, 10])

    #sugar supply, demand and equilibrium
    plt.subplot(132)
    ax = plt.gca()
    firmResults.plot(kind = 'line', x = 'step', y = 'SS_t', color = 'blue', ax = ax)
    householdResults.plot(kind = 'line', x = 'step', y = 'SD_t', color = 'red', ax = ax)
    plt.axhline(y = S_star, color = 'green', ls = ':')
    plt.title('sugar supply and demand')
    ax.set_ylim([0, 100])

    #labor supply, demand and equilibrium
    plt.subplot(133)
    ax = plt.gca()
    firmResults.plot(kind = 'line', x = 'step', y = 'LD_t', color = 'blue', ax = ax)
    householdResults.plot(kind = 'line', x = 'step', y = 'LS_t', color = 'red', ax = ax)
    plt.axhline(y = L_star, color = 'green', ls = ':')
    plt.title('labor supply and demand')
    ax.set_ylim([0, 400])
    
    plt.show()

    #plt.savefig('../plots/Fig7aip5.pdf')