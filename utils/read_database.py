import pandas as pd
import datetime

def read_database(database_path):
  try:
    df = pd.read_excel(database_path)

    # Extraer fechas como día "n" del año
    fechas = pd.to_datetime(df['Fecha'])
    lista_dias = fechas.dt.dayofyear.tolist()

    # Extraer horas en formato decimal
    
