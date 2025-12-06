#------------------------------------------------------------------------------
import numpy as np
def t_sandia(Ta,poa_irrad,wind_speed,Type='Glass/cell/polymer_sheet/OpenRack'):
    if Type =='Glass/Cell/galss/OpenRack':
        a = -3.47
        b = -0.0594
    elif Type =='Glass/cell/galss/CloseRoofMount':
        a = -2.98
        b = -0.0471
    #ESTE 
    elif Type =='Glass/cell/polymer_sheet/OpenRack':
        a = -3.56
        b = -0.0750
    elif Type =='Glass/cell/polymer_sheet/InsultatedRack':
        a = -2.81
        b = -0.0455
    elif Type =='Polymer/thin-fiml/steel/OpenRack':
        a = -3.58
        b = -0.113
    elif Type =='22X-Linear-Concentration/Tracker': 
        a = -3.28
        b = -0.13     

    t_sandia_list = []
    gref = 1000 # Irradiancia para STC W/m² (valor estándar)
    dT = 3  # DeltaT °C (puede agarrarse entre 2 y 5 para policristalinos)
    for ta, poa, v in zip(Ta,poa_irrad,wind_speed):
        Tm = ta + poa*np.exp(a + b*v) # Primero se calcula temperatura de módulo
        Tc = Tm + (poa/gref)*dT # Luego se calcula temperatura de celda
        t_sandia_list.append(Tc)
    return t_sandia_list