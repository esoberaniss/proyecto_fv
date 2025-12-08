import numpy as np
from models.irradiance.hdkr import hdkr
from models.temperatures.noct import t_noct
from models.temperatures.sandia import t_sandia
from models.temperatures.skoplaki import t_skoplaki
from tqdm import tqdm


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

def adjustable_tilt_energy_bar(
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

    n_intervals = int(np.ceil(ndays / interval_days))

    start_day = 1
    with tqdm(total=n_intervals, desc="Procesando intervalos", unit="intervalo") as pbar:
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
            for beta in tqdm(angles, desc=f"Ángulos {start_day}-{end_day}", leave=False, unit="ángulo"):

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
            pbar.update(1)

    return total_energy, angles_opt_per_interval

def seasonal_tilt_energy(
        dias, horas, ghi_irrad, lat,
        temp_amb, wind_speed,
        P_stc=700, gamma=0.003,
        min_tilt=15, max_tilt=45
    ):

    ndays = int(max(dias))

    seasonal_intervals = [
        ("Primavera", 80, 171),
        ("Verano",    172, 264),
        ("Otoño",     265, 354),
        ("Inv_1",     355, ndays),
        ("Inv_2",       1, 79)
    ]

    interval_results = []

    for (name, start_day, end_day) in tqdm(seasonal_intervals, desc="Estaciones"):

        idx = (dias >= start_day) & (dias <= end_day)

        dias_i  = dias[idx]
        horas_i = horas[idx]
        ghi_i   = ghi_irrad[idx]
        ta_i    = temp_amb[idx]
        v_i     = wind_speed[idx]

        angles = np.arange(min_tilt, max_tilt + 1)
        energy_values = []

        for beta in tqdm(angles, desc=f"Ángulos {name}", leave=False):

            gt = hdkr(dias_i, horas_i, ghi_i, lat, beta)
            Tc = t_sandia(ta_i, gt, v_i)

            Pdc = P_stc * (np.array(gt) / 1000) * (1 - gamma*(np.array(Tc)-25))
            Pdc[Pdc < 0] = 0

            energy_values.append(np.trapz(Pdc, dx=1/6) / 1000)

        idx_opt = np.argmax(energy_values)
        interval_results.append((name, start_day, end_day, angles[idx_opt], energy_values[idx_opt]))

    # Combinar invierno
    inv_1 = interval_results[3][4]
    inv_2 = interval_results[4][4]
    energia_inv = inv_1 + inv_2

    # Recalcular ángulo óptimo real del invierno
    angles = np.arange(min_tilt, max_tilt + 1)
    winter_energy = []

    for beta in angles:
        idx1 = (dias >= 355) & (dias <= ndays)
        idx2 = (dias >= 1)   & (dias <= 79)

        d  = np.concatenate((dias[idx1], dias[idx2]))
        h  = np.concatenate((horas[idx1], horas[idx2]))
        g  = np.concatenate((ghi_irrad[idx1], ghi_irrad[idx2]))
        ta = np.concatenate((temp_amb[idx1], temp_amb[idx2]))
        v  = np.concatenate((wind_speed[idx1], wind_speed[idx2]))

        gt = hdkr(d, h, g, lat, beta)
        Tc = t_sandia(ta, gt, v)

        Pdc = P_stc * (np.array(gt) / 1000) * (1 - gamma*(np.array(Tc)-25))
        Pdc[Pdc < 0] = 0

        winter_energy.append(np.trapz(Pdc, dx=1/6) / 1000)

    beta_opt_inv = angles[np.argmax(winter_energy)]
    energia_inv = max(winter_energy)

    final_results = [
        ("Primavera", 80, 171, interval_results[0][3], interval_results[0][4]),
        ("Verano",    172, 264, interval_results[1][3], interval_results[1][4]),
        ("Otoño",     265, 354, interval_results[2][3], interval_results[2][4]),
        ("Invierno",  355, 79, beta_opt_inv, energia_inv)
    ]

    total_energy = (interval_results[0][4] +
                    interval_results[1][4] +
                    interval_results[2][4] +
                    energia_inv)

    return total_energy, final_results

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

    annual_energy, angles_opt = seasonal_tilt_energy(
        dias=np.array(dias),
        horas=np.array(horas),
        ghi_irrad=np.array(ghi_irrad),
        lat=lat,
        temp_amb=np.array(temp_amb),
        wind_speed=np.array(wind_speeds_complete),
        P_stc=700,
        gamma=0.003,
        min_tilt=-10,
        max_tilt=60
    )


    print(f"Energía anual con ángulo ajustable: {annual_energy} kWh")
    print("Ángulos óptimos por intervalo:")

    for interval in angles_opt:

        # CASO 1: Formato estacional → ("Primavera", start, end, beta_opt, E_opt)
        if isinstance(interval[0], str):
            estacion = interval[0]
            start_day = interval[1]
            end_day = interval[2]
            beta_opt = interval[3]
            E_opt = interval[4]
            print(f"{estacion}: Días {start_day}-{end_day}: Ángulo óptimo = {beta_opt}°, Energía = {E_opt} kWh")

        # CASO 2: Formato normal → (start, end, beta_opt, E_opt)
        else:
            start_day = interval[0]
            end_day = interval[1]
            beta_opt = interval[2]
            E_opt = interval[3]
            print(f"Días {start_day}-{end_day}: Ángulo óptimo = {beta_opt}°, Energía = {E_opt} kWh")

    
    # print(f"Energía anual con ángulo ajustable: {annual_energy} kWh")
    # print("Ángulos óptimos por intervalo:")
    # for interval in angles_opt:
    #     print(f"Días {interval[0]}-{interval[1]}: Ángulo óptimo = {interval[2]}°, Energía = {interval[3]} kWh")
    
    #print("Ángulos óptimos por intervalo:")


    #print(wind_speeds_complete[:16])

    
