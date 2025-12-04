import pandas as pd
from pvlib import location, irradiance
from utils.read_database import pvlib_database

def liu_jordan_pvlib(database_path, lat, lon, tilt, azimuth=180, timezone='America/Mexico_City'):
    
    # Preparar datos para pvlib
    data = pvlib_database(database_path, timezone)

    # Parámetros del sitio
    site = location.Location(latitude=lat, longitude=lon, tz=timezone)

    # Solar position
    solar_position = site.get_solarposition(data.index)

    # Descomposición de GHI en DHI y DNI usando el modelo de Erbs
    dni_dhi = irradiance.erbs(
        ghi=data['ghi'],
        zenith=solar_position['apparent_zenith'],
        datetime_or_doy=data.index
    )

    dni_estimado = dni_dhi['dni']
    dhi_estimado = dni_dhi['dhi']

    # Cálculo de irradiancia
    poa_liujordan = irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=dni_estimado,
        ghi=data['ghi'],
        dhi=dhi_estimado,
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'],
        model='isotropic'
    )

    return poa_liujordan['poa_global'].tolist()