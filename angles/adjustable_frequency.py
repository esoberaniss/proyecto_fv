import numpy as np
from models.irradiance.hdkr import hdkr
from models.temperatures.noct import t_noct
from models.temperatures.sandia import t_sandia
from models.temperatures.skoplaki import t_skoplaki


def adjustable_tilt_energy(
        dias, horas, ghi_irrad, lat, 
        temp_amb, wind_speed,
        freq="anual",
        P_stc=700, gamma=0.003,
        min_tilt=15, max_tilt=45
    ):

    ndays = int(max(dias))
    
    # ---- Intervalos en días ----
    if freq == "diario":
        interval_days = 1
    elif freq == "semanal":
        interval_days = 7
    elif freq == "mensual":
        interval_days = 30
    elif freq == "bimestral":
        interval_days = 60
    elif freq == "estacional":
        interval_days = ndays // 4 
    elif freq == "anual":
        interval_days = ndays
    else:
        raise ValueError("Frecuencia inválida")

    # ---- Setup ----
    total_energy = 0.0
    angles_opt_per_interval = []

    start_day = 1
    while start_day <= ndays:
        end_day = min(start_day + interval_days - 1, ndays)

        # Filtrar intervalo
        idx = (dias >= start_day) & (dias <= end_day)
        dias_int = dias[idx]
        horas_int = horas[idx]
        ghi_int = ghi_irrad[idx]
        ta_int = temp_amb[idx]
        v_int = wind_speed[idx]

        angles = np.arange(min_tilt, max_tilt + 1, 1)
        energy_values = []

        # ---- Barrido de ángulos ----
        for beta in angles:

            # 1) Irradiancia efectiva (HDKR)
            gt = hdkr(dias_int, horas_int, ghi_int, lat, beta)

            # 2) Temperatura de celda
            Tc = t_sandia(ta_int, gt, v_int)
            
            gt = np.array(gt)
            Tc = np.array(Tc)

            # 3) Potencia DC
            Pdc = P_stc * (gt / 1000) * (1 - gamma * (Tc - 25))
            Pdc[Pdc < 0] = 0 # Evitar potencias negativas

            # 4) Energía del intervalo
            delta_t = 1/6
            E_beta = np.trapz(Pdc, dx=delta_t)/1000  # kWh

            energy_values.append(E_beta)

        # ---- Ángulo óptimo del intervalo ----
        idx_opt = np.argmax(energy_values)
        beta_opt = angles[idx_opt]
        E_opt = energy_values[idx_opt]

        total_energy += E_opt
        angles_opt_per_interval.append((start_day, end_day, beta_opt, E_opt))

        start_day += interval_days

    return total_energy, angles_opt_per_interval

# Ejemplo de uso:
if __name__ == "__main__":
    from utils.read_database import read_database, read_database_v, agregar_vel_viento

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

    annual_energy, angles_opt = adjustable_tilt_energy(
        dias=np.array(dias),
        horas=np.array(horas),
        ghi_irrad=np.array(ghi_irrad),
        lat=lat,
        temp_amb=np.array(temp_amb),
        wind_speed=np.array(wind_speeds_complete),
        freq="bimestral",
        P_stc=700,
        gamma=0.003,
        min_tilt=15,
        max_tilt=45
    )
    print(f"Energía anual con ángulo ajustable: {annual_energy} kWh")
    print("Ángulos óptimos por intervalo:")
    for interval in angles_opt:
        print(f"Días {interval[0]}-{interval[1]}: Ángulo óptimo = {interval[2]}°, Energía = {interval[3]} kWh")
    
    #print("Ángulos óptimos por intervalo:")


    #print(wind_speeds_complete[:16])

    
