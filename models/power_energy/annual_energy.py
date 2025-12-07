import numpy as np

def annual_energy(preal_list, h=1/6):
    energy = np.trapz(preal_list, dx=h)/1000 # kWh
    return energy