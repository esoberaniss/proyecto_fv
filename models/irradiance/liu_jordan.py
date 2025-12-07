from utils.decomposition import *
from utils.insolation import annual_insolation
from utils.plot import plot_xy
import numpy as np

pg = 0.2  # Ground reflectance

def liu_jordan(dias, horas, ghi_irrad, phi, b_angle):
    dihi_list, dhi_list = erbs_decomposition(dias, horas, ghi_irrad, phi)
        
    gt_list = []

    for d, T, dihi, dhi, ghi in zip(dias, horas, dihi_list, dhi_list, ghi_irrad):
        zenith = angulo_zenith(d,T,phi)
        thetai = angulo_incidente(d,T,phi,b_angle)

        if zenith >= 88.0:
            rb = 0
        else:
            cos_i = cosd(thetai)
            cos_z = cosd(zenith)
            Rb = cos_i / cos_z

            if Rb < 0:
                Rb = 0.0
            elif Rb > 10.0:
                Rb = 0.0
            
            rb = Rb

        gt = dihi * rb + dhi * (1 + cosd(b_angle)) / 2 + ghi * pg * (1 - cosd(b_angle)) / 2
        gt_list.append(gt)

    return gt_list

def optimal_tilt_lj(dias, horas, ghi_irrad, lat, min_tilt=20, max_tilt=50):
    angles = [20, 21, 25, 30, 35, 40, 45, 50]
    annual_values = []

    for beta in angles:
        gt = liu_jordan(dias, horas, ghi_irrad, lat, beta)
        annual = annual_insolation(gt, h=1/6) / 1000  # kWh/m²
        annual_values.append(annual)

    # Encontrar ángulo óptimo
    idx_opt = np.argmax(annual_values)
    ang_opt = angles[idx_opt]
    max_insol = annual_values[idx_opt]

    return angles, annual_values, ang_opt, max_insol
    
