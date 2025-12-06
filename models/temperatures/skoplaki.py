#------------------------------------------------------------------------------
def agregar_vel_viento(df1, df2, nombre_columna="Velocidad_Viento"):
    dias1 = df1["dias"]
    dias2 = df2["dias"]
    ws = df2["Velocidad_Viento"]
    mapa_ws = {d: w for d, w in zip(dias2, ws)}
    nueva_columna = [mapa_ws.get(d, None) for d in dias1]
    df1[nombre_columna] = nueva_columna
    return df1
#------------------------------------------------------------------------------
def t_skoplaki(Ta,poa_irrad,wind_speed):
    t_skoplaki_list = []
    for ta, poa, v in zip(Ta,poa_irrad,wind_speed):
        Tc = ta + (0.32/(8.91+(2*v)))*poa
        t_skoplaki_list.append(Tc)
    return t_skoplaki_list
#------------------------------------------------------------------------------
# def temperatura_skoplaki(df, columna_irrd, columna_temp="temperaturas", columna_viento="Velocidad_Viento"):
#     ghi = df[columna_irrd]
#     temps = df[columna_temp]
#     vientos = df[columna_viento]
#     Tem_celda = [tem_cel_skoplaki(t,i,v) for t,i,v in zip(temps,ghi,vientos)]
#     return Tem_celda