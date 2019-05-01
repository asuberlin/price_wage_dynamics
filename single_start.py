from single_parameters import Parameters
from simulation import Simulation
from plotting import Plotting

#construct parameters dictionaries
runParameters, firmParameters, householdParameters = Parameters()

#run simulation
sim = Simulation(runParameters, firmParameters, householdParameters)
firmResults, householdResults, marketResults = sim.Run()

Plotting(sim.L_star, sim.S_star, sim.p_star, firmResults, householdResults)

