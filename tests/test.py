from models.irradiance import ideal, liu_jordan, hdkr
from models.power_energy.annual_energy import annual_energy
from models.power_energy.real_power import real_power
from utils.read_database import *
from utils.geometry import *
from utils.insolation import *
from utils.plot import *
from models.temperatures.sandia import t_sandia
import pandas as pd
import numpy as np

if __name__ == "__main__":

    # Ruta al archivo de la base de datos
    database_path = r'C:\Users\emman\Desktop\proyecto_fv\data\Base_Datos_Actualizada.xlsx'
    database_path_wind = r'C:\Users\emman\Desktop\proyecto_fv\data\Base_Datos_Viento.csv'
    
    # Leer las bases de datos
    data = read_database(database_path)
    data_wind = read_database_v(database_path_wind)
    
    # Extraer datos de la base de datos principal
    dias = data['dias']
    horas = data['horas']
    ghi_irrad = data['irradiancias']
    temp_amb = data['temperaturas']

    # Extraer datos de la base de datos de viento
    dias_wind = data_wind['dias']
    horas_wind = data_wind['horas']
    wind_speeds = data_wind['Velocidad_Viento']
    wind_speeds_complete = agregar_vel_viento(dias, horas, dias_wind, horas_wind, wind_speeds)

    # Parámetros del sitio
    lat = 20.96  # Latitud en grados
    long = -89.62  # Longitud en grados
    tilt = 24  # Ángulo de inclinación en grados

    # Calcular la irradiancia total en el plano inclinado usando el modelo hdkr
    gt_values = hdkr.hdkr(dias, horas, ghi_irrad, lat, tilt)

    # Calcular la temperatura de celda
    t_cell = t_sandia(temp_amb, gt_values, wind_speeds_complete)

    # Calcular la potencia real y la energía anual
    power_list = real_power(gt_values, t_cell, p_nominal=700, gamma_coeff=0.003)
    annual_e = np.trapz(power_list, dx=1/6)/1000  # kWh
    #annual_e = annual_energy(power_list, h=1/6)  # kWh
    print(f"Energía anual: {annual_e} kWh")


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