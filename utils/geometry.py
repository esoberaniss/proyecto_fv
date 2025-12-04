import numpy as np
from datetime import datetime
#-------------------------------------------------------------------------------
def sind(x):return np.sin(np.deg2rad(x))
def cosd(x):return np.cos(np.deg2rad(x))
def asind(x):return np.degrees(np.arcsin(np.clip(x, -1.0, 1.0)))
def acosd(x):return np.degrees(np.arccos(np.clip(x, -1.0, 1.0)))
#-------------------------------------------------------------------------------
def declinacion_solar(d): 
    return 23.45 * sind(360.0 * (d-80) / 365.0)
#-------------------------------------------------------------------------------
def angulo_w(T): 
    return (15*(12-T))
#-------------------------------------------------------------------------------
def altura_solar(d,T,phi):
    val = sind(declinacion_solar(d))*sind(phi) + cosd(declinacion_solar(d))*cosd(phi)*cosd(angulo_w(T))
    return asind(np.maximum(0.0, val))  # Altura solar no negativa
#-------------------------------------------------------------------------------
def angulo_zenith(d,T,phi):
    return 90 - altura_solar(d,T,phi)
#-------------------------------------------------------------------------------
def angulo_azimut(d,T,phi):
    alpha = altura_solar(d, T, phi)
    delta = declinacion_solar(d)
    w = angulo_w(T)

    if alpha < 0.1:
        return 0.0  # Sol debajo del horizonte
    
    num = sind(alpha)*sind(phi) - sind(delta)
    den = cosd(alpha)*cosd(phi)
    mag = acosd(num / den)

    return mag if w > 0 else -mag
#-------------------------------------------------------------------------------
def angulo_incidente(d,T,phi,b):
    return acosd(
        sind(angulo_zenith(d,T,phi))*cosd(angulo_azimut(d,T,phi))*sind(b) + cosd(angulo_zenith(d,T,phi))*cosd(b)
    )
#-------------------------------------------------------------------------------
def go_irrad(d, T, phi):
    Gsc = 1367  # Constante de irradiancia solar [W/m2]
    Go = Gsc * (1 + 0.033 * cosd((360 * d) / 365)) * cosd(angulo_zenith(d,T,phi))
    return Go