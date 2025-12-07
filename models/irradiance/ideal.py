from utils.geometry import *
from utils.insolation import annual_insolation

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

def optimal_tilt_ideal(dias, horas, ghi_irrad, lat, min_tilt=20, max_tilt=50):
    angles = [20, 21, 25, 30, 35, 40, 45, 50]
    annual_values = []

    for beta in angles:
        gt = ideal_irrad(dias, horas, ghi_irrad, lat, beta)
        annual = annual_insolation(gt, h=1/6) / 1000  # kWh/m²
        annual_values.append(annual)

    # Encontrar ángulo óptimo
    idx_opt = np.argmax(annual_values)
    ang_opt = angles[idx_opt]
    max_insol = annual_values[idx_opt]

    return angles, annual_values, ang_opt, max_insol




    