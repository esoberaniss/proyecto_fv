from models.irradiance import liu_jordan
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
    phi = 21.0  # Latitud en grados
    b_angle = 21.0  # Ángulo de inclinación del panel en grados
    
    # Calcular la irradiancia total en el plano inclinado usando el modelo de Liu-Jordan
    gt_values = liu_jordan.liu_jordan(dias, horas, ghi_irrad, phi, b_angle)

    # Crear Excel con valores calculados
    output_df = pd.DataFrame({
        'Día del año': dias,
        'Hora (decimal)': horas,
        'GHI Irradiancia (W/m2)': ghi_irrad,
        'GT Irradiancia en plano inclinado (W/m2)': gt_values
    })
    output_df.to_excel('irradiancia_calculada.xlsx', index=False)

    # rb = []
    # for d, T in zip(dias, horas):
    #     zenith = angulo_zenith(d,T,phi)
    #     thetai = angulo_incidente(d,T,phi,b_angle)

    #     if zenith >= 88.0:
    #         rb.append(0)
    #     else:
    #         cos_i = cosd(thetai)
    #         cos_z = cosd(zenith)
    #         Rb = cos_i / cos_z

    #         if Rb < 0:
    #             Rb = 0.0
    #         elif Rb > 10.0:
    #             Rb = 0.0
            
    #         rb.append(Rb)
            
    
    # output_df = pd.DataFrame({
    #     'Día del año': dias,
    #     'Hora (decimal)': horas,
    #     'GHI Irradiancia (W/m2)': ghi_irrad,
    #     'R_b': rb
    # })

    # output_df.to_excel('rb_calculado.xlsx', index=False)