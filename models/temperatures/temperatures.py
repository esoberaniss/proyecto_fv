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
def Tem_cel_skoplaki(Ta,I,Vv):
    Tc = Ta + (0.32/(8.91+(2*Vv)))*I
    return(Tc)
#------------------------------------------------------------------------------
def Temperatura_skoplaki(df,columna_irrd,columna_temp="temperaturas", columna_viento="Velocidad_Viento"):
    irrad = df[columna_irrd]
    temps = df[columna_temp]
    vientos = df[columna_viento]
    Tem_celda = [Tem_cel_skoplaki(t,i,v) for t,i,v in zip(temps,irrad, vientos)]
    return Tem_celda
#------------------------------------------------------------------------------
import numpy as np
def Tem_cel_sandia(Ta,I_new,Vv,Type='Glass/cell/polymer_sheet/OpenRack',):
    if Type =='Glass/Cell/galss/OpenRack':
        a = -3.47
        b = -0.0594
    if Type =='Glass/cell/galss/CloseRoofMount':
        a = -2.98
        b = -0.0471
    #ESTE 
    if Type =='Glass/cell/polymer_sheet/OpenRack':
        a = -3.56
        b = -0.0750
    if Type =='Glass/cell/polymer_sheet/InsultatedRack':
        a = -2.81
        b = -0.0455
    if Type =='Polymer/thin-fiml/steel/OpenRack':
        a = -3.58
        b = -0.113
    if Type =='22X-Linear-Concentration/Tracker': 
        a = -3.28
        b = -0.13     
    Tm = I_new*np.exp(a+b*Vv)+Ta
    Tc = Tm + (I_new/1000)*3
    return(Tc)
#------------------------------------------------------------------------------
def Temperatura_sandia(df,columna_irrd,columna_temp="temperaturas", columna_viento="Velocidad_Viento"):
    irrad = df[columna_irrd]
    temps = df[columna_temp]
    vientos = df[columna_viento]
    Tem_celda = [Tem_cel_sandia(t,i,v) for t,i,v in zip(temps,irrad, vientos)]
    return Tem_celda
#------------------------------------------------------------------------------
def Tem_cel_NOCT(Ta,I_new,NOCT):
    Tc = Ta + ((NOCT-20)/0.8)*I_new
    return(Tc)
#------------------------------------------------------------------------------
def Temperatura_NOCT(NOCT,df,columna_irrd,columna_temp="temperaturas"):
    irrad = df[columna_irrd]
    temps = df[columna_temp]
    Tem_celda = [Tem_cel_NOCT(t,i,NOCT) for t,i in zip(temps,irrad)]
    return Tem_celda
#------------------------------------------------------------------------------
def Potencia(df,columna_irrd,columna_temp_celda,P_nominal,Coeficiente_l):
    irrad = df[columna_irrd]
    temps = df[columna_temp_celda]
    Potencia = [P_nominal*i*(1-Coeficiente_l*(t-25)) for t,i in zip(temps,irrad)]
    return Potencia
#------------------------------------------------------------------------------
def Energia_anual(valores, h=10/60):
    return h * (0.5*valores[0] + sum(valores[1:-1]) + 0.5*valores[-1])
#------------------------------------------------------------------------------
