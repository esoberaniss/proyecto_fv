from utils.geometry import *
from utils.decomposition import erbs_decomposition
import numpy as np

pg = 0.2  # Ground reflectance

def hdkr(dias, horas, ghi_irrad, phi, b_angle):
    dihi_list, dhi_list = erbs_decomposition(dias, horas, ghi_irrad, phi)
    gt_list = []

    #Ai_list = []
    #f_list = []
    #Go_list = []

    for d, T, dihi, dhi, ghi in zip(dias, horas, dihi_list, dhi_list, ghi_irrad):
        zenith = angulo_zenith(d,T,phi)
        thetai = angulo_incidente(d,T,phi,b_angle)

        if zenith >= 88.0:
            Rb = 0
        else:
            cos_i = cosd(thetai)
            cos_z = cosd(zenith)
            rb = cos_i / cos_z

            if Rb < 0:
                rb = 0.0
            elif Rb > 10.0:
                rb = 0.0
            
            Rb = rb
        
        Go = go_irrad(d, T, phi)
        #Go_list.append(Go)
        
        Ai = dihi / Go if Go > 0.1 and dihi<Go else 0    # Anisotropy index
        #Ai_list.append(Ai)

        f = np.sqrt(dihi/ghi) if ghi != 0 else 0    # Modulating factor
        #f_list.append(f)

        gt = (dihi + dhi * Ai) * Rb + dhi * (1 - Ai)*((1 + cosd(b_angle))/2)*(1 + f*(sind(b_angle/2))**3) + ghi * pg * ((1 - cosd(b_angle))/2)
        gt = np.maximum(0.0, gt)
        gt_list.append(gt)

    return gt_list
