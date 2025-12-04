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