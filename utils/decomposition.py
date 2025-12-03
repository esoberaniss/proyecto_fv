from utils.geometry import *

Gsc = 1367  # Constant solar irradiance [W/m2]

def erbs_decomposition(dias,horas,ghi_irrad,phi):

    dhi_list = []
    dni_list = []

    for d, T, ghi in zip(dias, horas, ghi_irrad):
        
        # Calcular Go (irradiancia extraterrestre)
        Go = Gsc * (1 + 0.033 * cosd((360 * d) / 365)) * cosd(angulo_zenith(d,T,phi))

        # Calcular KT
        if Go != 0:
            kT = ghi / Go 
        else:
            kT = 0
        
        if kT <= 0.22:
            dhi = ghi * (1.0 - 0.09 * kT)
        elif 0.22 < kT <= 0.8:
            dhi = ghi * (0.9511 - 0.1604 * kT + 4.388 * kT**2 - 16.638 * kT**3 + 12.336 * kT**4)
        else:
            dhi = ghi * 0.165
        
        dhi = max(dhi, 0)  # Asegurarse de que DHI no sea negativo
        dni = (ghi - dhi) / cosd(angulo_zenith(d,T,phi)) if cosd(angulo_zenith(d,T,phi)) > 0 else 0

        dhi_list.append(dhi)
        dni_list.append(dni)
    
    return dni_list, dhi_list
