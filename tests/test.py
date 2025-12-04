from models.irradiance import liu_jordan
from models.irradiance import hdkr
from models.pvlibmodels import liu_jordan_pvlib, hdkr_pvlib
from utils.read_database import read_database
from utils.geometry import *
import pandas as pd

if __name__ == "__main__":

    # Ruta al archivo de la base de datos
    database_path = r'C:\Users\emman\Desktop\proyecto_fv\data\Base_Datos_Actualizada.xlsx'
    
    # Leer la base de datos
    data = read_database(database_path)
    
    dias = data['dias']
    horas = data['horas']
    ghi_irrad = data['irradiancias']
    
    # Parámetros del sitio
    lat = 21.0  # Latitud en grados
    long = -89.6  # Longitud en grados
    tilt = 21.0  # Ángulo de inclinación del panel en grados
    #b_angle = 21.0  # Ángulo de inclinación del panel en grados
    
    # Calcular la irradiancia total en el plano inclinado usando el modelo de HDKR
    gt_values_pvlib = hdkr_pvlib.hdkr_pvlib(database_path, lat, long, tilt)
    gt_values = hdkr.hdkr(dias, horas, ghi_irrad, lat, tilt)

    # Crear Excel con valores calculados
    output_df = pd.DataFrame({
        'Día del año': dias,
        'Hora (decimal)': horas,
        'GHI Irradiancia (W/m2)': ghi_irrad,
        'GT Irradiancia en plano inclinado PVLIB (W/m2)': gt_values_pvlib,
        'GT Irradiancia en plano inclinado (W/m2)': gt_values,
        #'Índice de anisotropía (Ai)': Ai_values,
        #'Factor de modulación (f)': f_values,
        #'DIHI estimado (W/m2)': dihi_values,
        #'Irradiancia extraterrestre (Go) (W/m2)': go_values
        
    })
    output_df.to_excel('irradiancia_calculada.xlsx', index=False)