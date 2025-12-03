from utils.geometry import *

def ideal_irrad(dias, horas, ghi_irrad, phi, b_angle):
  ideal_irrad = []
  eps = 1e-6 # Evitar divisiones por cero

  for d, T, ghi in zip(dias, horas, ghi_irrad):
    cos_z = cosd(angulo_zenith(d,T,phi))
    cos_i = cosd(angulo_incidente(d,T,phi,b_angle))
    
    if cos_z <= eps or cos_i <= 0 or ghi <= 0:
      irrad = 0
    else:
      irrad = ghi * (cos_i / cos_z)

    ideal_irrad.append(irrad)

  return ideal_irrad




    