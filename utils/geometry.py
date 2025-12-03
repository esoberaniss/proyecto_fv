import numpy as np
from datetime import datetime
#-------------------------------------------------------------------------------
def sind(x):return np.sin(np.deg2rad(x))
def cosd(x):return np.cos(np.deg2rad(x))
def asind(x):return np.degrees(np.arcsin(np.clip(x, -1.0, 1.0)))
def acosd(x):return np.degrees(np.arccos(np.clip(x, -1.0, 1.0)))
#-------------------------------------------------------------------------------
def declinacion_solar(n): 
    return 23.45 * sind(360.0 * (n-80) / 365.0)
#-------------------------------------------------------------------------------
def angulo_w(T): 
    return (15*(12-T))
#-------------------------------------------------------------------------------
def altura_solar(n,phi,T):
    return asind(sind(declinacion_solar(n))*sind(phi) + cosd(declinacion_solar(n))*cosd(phi)*cosd(angulo_w(T)))
#-------------------------------------------------------------------------------
def angulo_zenith(n,phi,T):
    return 90 - altura_solar(n,phi,T)
#-------------------------------------------------------------------------------
def angulo_azimut(n,phi,T):
    return acosd(
        (sind(altura_solar(n,phi,T))*sind(phi)-sind(declinacion_solar(n))) / (cosd(altura_solar(n,phi,T))*cosd(phi))
    )
#-------------------------------------------------------------------------------
def angulo_incidente(n,phi,T,b):
    return acosd(
        sind(angulo_zenith(n,phi,T))*sind(angulo_azimut(n,phi,T)) + sind(angulo_zenith(n,phi,T))*cosd(angulo_azimut(n,phi,T))*sind(b) + cosd(angulo_zenith(n,phi,T))*cosd(b)
    )