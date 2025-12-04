from utils.decomposition import *

pg = 0.2  # Ground reflectance

def liu_jordan(dias, horas, ghi_irrad, phi, b_angle):
    dihi, dhi = erbs_decomposition(dias, horas, ghi_irrad, phi)
    
    gt_list = []
    
    for d, T, dihi, dhi, ghi in zip(dias, horas, dihi, dhi, ghi_irrad):
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