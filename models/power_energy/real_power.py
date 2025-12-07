def real_power (poa_irrad, cell_temps, p_nominal, gamma_coeff):
    power_list = []
    gref = 1000  # Reference irradiance in W/m² (STC)
    for poa, temp in zip(poa_irrad, cell_temps):
        power = p_nominal * (poa/gref) * (1 - gamma_coeff * (temp - 25))
        power_list.append(power)
    return power_list