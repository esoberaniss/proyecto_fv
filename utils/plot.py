import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

def plot_xy(lista_x, lista_y, titulo="Gráfica",etiqueta_x="Eje X", etiqueta_y="Eje Y", nombre_linea="Datos"):
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(lista_x,lista_y,label=nombre_linea,color='#1f77b4',linewidth=2,marker='o',markersize=7,linestyle='--')
    # ------------- GRID AVANZADO -------------
    ax.xaxis.set_major_locator(MultipleLocator(10))   # Cada 10 unidades
    ax.xaxis.set_minor_locator(MultipleLocator(5))    # Cada 5 unidades
    ax.grid(which='major', linestyle='--', linewidth=0.8, color='gray', alpha=0.6)
    ax.grid(which='minor', linestyle=':', linewidth=0.5, color='gray', alpha=0.5)
    # ---------- TÍTULOS Y ETIQUETAS ----------
    ax.set_title(titulo, fontsize=16, pad=20)
    ax.set_xlabel(etiqueta_x, fontsize=13)
    ax.set_ylabel(etiqueta_y, fontsize=13)
    ax.legend(loc='best', fontsize=12)
    # ------------ ANOTACIÓN DE MÁXIMO ------------
    idx_opt = np.argmax(lista_y)
    opt_x = lista_x[idx_opt]
    opt_val = lista_y[idx_opt]
    ax.set_ylim(0, opt_val * 1.15)
    texto_opt = f'Óptimo: {opt_x:.2f}\n{opt_val:.2f}'
    ax.annotate(
        texto_opt,
        xy=(opt_x, opt_val),
        xytext=(opt_x, opt_val * 0.8),
        fontsize=11, ha='center',
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.85),
        arrowprops=dict(facecolor='black', shrink=0.05)
    )

    plt.tight_layout()
    plt.show()
#------------------------------------------------------------------------------
def plot_xy_multi(lista_x, listas_y, titulo="Gráfica",
                  etiqueta_x="Eje X", etiqueta_y="Eje Y",
                  nombres_lineas=None):
    fig, ax = plt.subplots(figsize=(10, 7))

    # Si no se dan nombres de líneas, generarlos automáticamente
    if nombres_lineas is None:
        nombres_lineas = [f"Serie {i+1}" for i in range(len(listas_y))]

    # ------ Graficar cada lista de Y ------
    for y, nombre in zip(listas_y, nombres_lineas):
        ax.plot(
            lista_x, y,
            label=nombre,
            linewidth=2,
            marker='o',
            markersize=6,
            linestyle='--'
        )

    # ------ GRID AVANZADO ------
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    ax.grid(which='major', linestyle='--', linewidth=0.8, color='gray', alpha=0.6)
    ax.grid(which='minor', linestyle=':', linewidth=0.5, color='gray', alpha=0.5)

    # ------ TÍTULOS ------
    ax.set_title(titulo, fontsize=15, pad=20)
    ax.set_xlabel(etiqueta_x, fontsize=13)
    ax.set_ylabel(etiqueta_y, fontsize=13)
    ax.legend(loc='best', fontsize=12)

    # ------ ANOTAR MÁXIMO DE CADA CURVA ------
    for y, nombre in zip(listas_y, nombres_lineas):
        idx_opt = np.argmax(y)
        opt_x = lista_x[idx_opt]
        opt_val = y[idx_opt]

        ax.annotate(
            f'{nombre}\nMáx: {opt_val:.2f}',
            xy=(opt_x, opt_val),
            xytext=(opt_x, opt_val * 1.05),
            fontsize=10,
            ha='center',
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", alpha=0.85),
            arrowprops=dict(facecolor='black', shrink=0.05)
        )

    plt.tight_layout()
    plt.show()