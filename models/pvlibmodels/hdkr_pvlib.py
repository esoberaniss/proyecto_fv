import pandas as pd
from pvlib import location, irradiance
from utils.read_database import pvlib_database

def hdkr_pvlib(database_path, lat, lon, tilt, azimuth=180, timezone='America/Mexico_City'):
    
    # Preparar datos para pvlib
    data = pvlib_database(database_path, timezone)

    # Parámetros del sitio
    site = location.Location(latitude=lat, longitude=lon, tz=timezone)

    # Solar position
    solar_position = site.get_solarposition(data.index)

    # Cálculo de radiación extraterrestre
    dni_extra = irradiance.get_extra_radiation(data.index)

    # Descomposición de GHI en DHI y DNI usando el modelo de Erbs
    dni_dhi = irradiance.erbs(
        ghi=data['ghi'],
        zenith=solar_position['apparent_zenith'],
        datetime_or_doy=data.index
    )

    dni_estimado = dni_dhi['dni']
    dhi_estimado = dni_dhi['dhi']

    # Cálculo de irradiancia
    poa_hdkr = irradiance.get_total_irradiance(
        surface_tilt=tilt,
        surface_azimuth=azimuth,
        dni=dni_estimado,
        ghi=data['ghi'],
        dhi=dhi_estimado,
        solar_zenith=solar_position['apparent_zenith'],
        solar_azimuth=solar_position['azimuth'],
        dni_extra=dni_extra,
        model='reindl'
    )

    return poa_hdkr['poa_global'].tolist()