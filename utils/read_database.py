import pandas as pd
import datetime

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

# Ejemplo de uso
if __name__ == "__main__":
  database_path = 'database_path'
  data = read_database(database_path)
  print(data['dias'][:10])
  print(data['horas'][:10])
  print(data['temperaturas'][:10])
  print(data['irradiancias'][:10])