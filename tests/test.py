from models.irradiance import liu_jordan
from models.irradiance import hdkr
from models.pvlibmodels import liu_jordan_pvlib, hdkr_pvlib
from models.irradiance import ideal
from utils.read_database import read_database
from utils.geometry import *
from utils.insolation import anual_insolation
from utils.plot import plot_xy_multi, plot_xy
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
    lat = 20.96  # Latitud en grados
    long = -89.62  # Longitud en grados
    tilt = 50  # Ángulo de inclinación del panel en grados

    gt_values = hdkr_pvlib.hdkr_pvlib(database_path, lat, long, tilt)
    anual_insol = anual_insolation(gt_values, h=1/6)/1000  # Convertir a kWh/m²
    print(f"Insolación anual en el plano inclinado (Liu-Jordan): {anual_insol} Wh/m²")


    # Barrido de ángulos para encontrar el óptimo con Liu-Jordan
    #angles, annual_values, ang_opt, max_insol = liu_jordan.optimal_tilt_lj(dias, horas, ghi_irrad, lat)
    #angles_lj, annual_values_lj, ang_opt_lj, max_insol_lj = liu_jordan.optimal_tilt_lj(dias, horas, ghi_irrad, lat)
    #angle_hdkr, annual_values_hdkr, ang_opt_hdkr, max_insol_hdkr = hdkr.optimal_tilt_hdkr(dias, horas, ghi_irrad, lat)

    # plot_xy(
    #     lista_x = angles,
    #     lista_y = annual_values,
    #     titulo = "Insolación anual vs Ángulo de Inclinación",
    #     etiqueta_x = "Ángulo de Inclinación (°)",
    #     etiqueta_y = "Insolación Anual (kWh/m²)",
    #     nombre_linea = "Ideal",
    # )

    # plot_xy_multi(
    #     lista_x = angles,
    #     listas_y = [annual_values, annual_values_lj, annual_values_hdkr],
    #     titulo = "Insolación anual vs Ángulo de Inclinación",
    #     etiqueta_x = "Ángulo de Inclinación (°)",
    #     etiqueta_y = "Insolación Anual (kWh/m²)",
    #     nombres_lineas = ["Ideal", "Liu-Jordan", "HDKR"]
    # )

    #anual_insol = anual_insolation(gt_values, h=1/6)/1000  # Convertir a kWh/m²
    #print(f"Insolación anual en el plano inclinado (Liu-Jordan): {anual_insol} Wh/m²")




# Calcular la irradiancia total en el plano inclinado usando el modelo de HDKR
    #gt_values_pvlib = hdkr_pvlib.hdkr_pvlib(database_path, lat, long, tilt)
    # gt_values = liu_jordan.liu_jordan(dias, horas, ghi_irrad, lat, tilt)

    # Crear Excel con valores calculados
    # output_df = pd.DataFrame({
    #     'Día': dias,
    #     'Hora': horas,
    #     'GHI (W/m²)': ghi_irrad,
    #     'Irradiancia en plano inclinado (W/m²)': gt_values
    # })
    # output_df.to_excel('irradiancia_calculada.xlsx', index=False)