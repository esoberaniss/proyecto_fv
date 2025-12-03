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
    return asind(sind(declinacion_solar(d))*sind(phi) + cosd(declinacion_solar(d))*cosd(phi)*cosd(angulo_w(T)))
#-------------------------------------------------------------------------------
def angulo_zenith(d,T,phi):
    return 90 - altura_solar(d,T,phi)
#-------------------------------------------------------------------------------
def angulo_azimut(d,T,phi):
    return acosd(
        (sind(altura_solar(d,T,phi))*sind(phi)-sind(declinacion_solar(d))) / (cosd(altura_solar(d,T,phi))*cosd(phi))
    )
#-------------------------------------------------------------------------------
def angulo_incidente(d,T,phi,b):
    return acosd(
        sind(angulo_zenith(d,T,phi))*sind(angulo_azimut(d,T,phi)) + sind(angulo_zenith(d,T,phi))*cosd(angulo_azimut(d,T,phi))*sind(b) + cosd(angulo_zenith(d,T,phi))*cosd(b)
    )