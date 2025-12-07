from datetime import date
import pandas as pd
import datetime
import math
#------------------------------------------------------------------------------
def read_database(database_path):
  try:
    df = pd.read_excel(database_path)

    # Extraer fechas como día "n" del año
    fechas = pd.to_datetime(df['Fecha'])
    lista_dias = fechas.dt.dayofyear.tolist()

    # Extraer horas en formato decimal
    lista_horas = []
    for hora in df['Hora']:
      hora_dt = datetime.datetime.strptime(hora, '%H:%M:%S')
      hora_decimal = hora_dt.hour + hora_dt.minute / 60 + hora_dt.second / 3600
      lista_horas.append(hora_decimal)
    
    # Extraer temperatura
    lista_temp = df['Temperatura'].tolist()

    # Extraer irradiancia
    lista_irrad = df['Irradiancia'].tolist()

    # Devolver los datos en un diccionario
    data_database = {
      'dias': lista_dias,
      'horas': lista_horas,
      'temperaturas': lista_temp,
      'irradiancias': lista_irrad
    }

    return data_database
  
  except Exception as e:
    print(f"Error al leer la base de datos: {e}")
    return None, None, None, None
#------------------------------------------------------------------------------
def pvlib_database(database_path, zona_horaria='America/Mexico_City'):
  try:
    df = pd.read_excel(database_path)

    # Construir el índice de tiempo (Fecha + Hora)
    fecha_hora = df['Fecha'].astype(str) + ' ' + df['Hora'].astype(str)
    df.index = pd.to_datetime(fecha_hora)

    df.index = df.index.tz_localize(zona_horaria)

    df = df.rename(columns={
                  'Irradiancia': 'ghi',
                  'Temperatura': 'temp_air'
                  })
    
    return df[['ghi', 'temp_air']]

  except Exception as e:
    print(f"Error al leer la base de datos: {e}")
#------------------------------------------------------------------------------
def read_database_v(database_path):
  try:
    df = pd.read_csv(database_path, skiprows=9)
    lista_ws10m = df['WS10M'].tolist()
    lista_day = df['DY'].tolist()   
    lista_month = df['MO'].tolist()   
    lista_hour = df['HR'].tolist()
    year = 2023
    list_day_n = []
    for mes, dia in zip(lista_month, lista_day):
        fecha = date(year, mes, dia)
        day_year = fecha.timetuple().tm_yday  
        list_day_n.append(day_year)
    data_database = {'Velocidad_Viento': lista_ws10m,'dias': list_day_n,'horas': lista_hour}
    return data_database
  except Exception as e:
      print(f"Error al leer la base de datos: {e}")
      return None, None, None, None
#------------------------------------------------------------------------------
# Esta une la información 
def agregar_vel_viento(dias1, horas1, dias2, horas2, ws):
    mapa_ws = {}
    for d, h, w in zip(dias2, horas2, ws):
        hora_entera = int(math.floor(h))
        mapa_ws[(d, hora_entera)] = w
        nueva_columna_ws = []
    for dia_df1, hora_df1 in zip(dias1, horas1):
        clave_busqueda = (dia_df1, int(math.floor(hora_df1)))
        velocidad = mapa_ws.get(clave_busqueda, None)
        nueva_columna_ws.append(velocidad)
    return nueva_columna_ws
#------------------------------------------------------------------------------
    

# Ejemplo de uso
if __name__ == "__main__":
  database_path = 'database_path'
  data = read_database(database_path)
  print(data['dias'][:10])
  print(data['horas'][:10])
  print(data['temperaturas'][:10])
  print(data['irradiancias'][:10])