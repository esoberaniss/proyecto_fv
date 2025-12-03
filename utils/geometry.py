import numpy as np
from datetime import datetime
#-------------------------------------------------------------------------------
phi = 20.967  # LATITUD
#-------------------------------------------------------------------------------
def sind(x):return np.sin(np.deg2rad(x))
def cosd(x):return np.cos(np.deg2rad(x))
def asind(x):return np.degrees(np.arcsin(np.clip(x, -1.0, 1.0)))
def acosd(x):return np.degrees(np.arccos(np.clip(x, -1.0, 1.0)))
#-------------------------------------------------------------------------------
def declinacion_solar(n): 
    return 23.45 * sind(360.0 * (n-80) / 365.0)
#-------------------------------------------------------------------------------
def Tiempo_a_decimal(hora_str):
    h, m, s = map(int, hora_str.split(':'))
    return h + m/60 + s/3600
#-------------------------------------------------------------------------------
def angulo_w(T): 
    return (15*(12-T))
#-------------------------------------------------------------------------------
def angulo_zenith(n,T):
    n = sind(phi)*sind(DECLINACION_SOLAR(n)) + cosd(phi)*cosd(DECLINACION_SOLAR(n))*cosd(W_ANGULO(T))
    return acosd(n)
#-------------------------------------------------------------------------------
def altura_solar(n,T):
    return (90 - ZENITH_ANGULO(n,T))
#-------------------------------------------------------------------------------
def angulo_azimut(n,T):
    n = (sind(DECLINACION_SOLAR(n))*sind(phi) - sind(DECLINACION_SOLAR(n)))/(cosd(DECLINACION_SOLAR(n))*cosd(phi))
    return acosd(n)
