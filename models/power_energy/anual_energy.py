def anual_energy(preal_list, h=1/6):
    energy = 0
    for i in range(len(preal_list)-1):
        energy += (preal_list[i] + preal_list[i+1]) * h / 2
    return energy