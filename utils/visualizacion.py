import matplotlib.pyplot as plt
import numpy as np

def generar_colores(n):
    """Genera una lista de n colores distintos"""
    if n == 0:
        return []
    cmap = plt.get_cmap('tab10')
    return [cmap(i % 10) for i in range(n)]

def crear_grafico_gantt(procesos, tiempo_actual, algoritmo):
    """Crea un diagrama de Gantt para visualizar la ejecución"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.patch.set_facecolor('#1e1f2f')
    
    # Configurar ejes
    for ax in [ax1, ax2]:
        ax.set_facecolor('#292b3e')
        for spine in ax.spines.values():
            spine.set_edgecolor('#495057')
    
    # Gráfico de ejecución (ax1)
    ax1.set_title(f"Ejecución - Algoritmo {algoritmo}", color='white', pad=20)
    ax1.set_xlabel("Tiempo", color='white')
    ax1.set_ylabel("Procesos", color='white')
    ax1.tick_params(colors='white')
    ax1.grid(True, alpha=0.3)
    
    # Gráfico de cola de preparados (ax2)
    ax2.set_title("Cola de Preparados", color='white', pad=20)
    ax2.set_xlabel("Tiempo", color='white')
    ax2.set_ylabel("Procesos", color='white')
    ax2.tick_params(colors='white')
    ax2.grid(True, alpha=0.3)
    
    # Lógica de visualización específica por algoritmo
    colores = generar_colores(len(procesos))
    
    # Dibujar ejecución hasta tiempo_actual
    for i, proceso in enumerate(procesos):
        color = colores[i]
        letra = chr(65 + proceso['pid'])
        
        # Dibujar en gráfico de ejecución
        if 'ejecuciones' in proceso:
            for inicio, duracion in proceso['ejecuciones']:
                if inicio + duracion <= tiempo_actual:
                    ax1.broken_barh([(inicio, duracion)], (i-0.4, 0.8), 
                                  facecolors=color, alpha=0.8)
                    ax1.text(inicio + duracion/2, i, letra, 
                           ha='center', va='center', color='white', fontweight='bold')
        elif 'inicio' in proceso and proceso['inicio'] <= tiempo_actual:
            duracion_dibujo = min(proceso['duracion'], tiempo_actual - proceso['inicio'])
            ax1.broken_barh([(proceso['inicio'], duracion_dibujo)], (i-0.4, 0.8), 
                          facecolors=color, alpha=0.8)
            ax1.text(proceso['inicio'] + duracion_dibujo/2, i, letra, 
                   ha='center', va='center', color='white', fontweight='bold')
    
    plt.tight_layout()
    return fig

def mostrar_metricas(procesos):
    """Muestra las métricas de desempeño"""
    if not procesos:
        return {}
    
    retorno_prom = sum(p['retorno'] for p in procesos) / len(procesos)
    espera_prom = sum(p['espera'] for p in procesos) / len(procesos)
    
    return {
        'retorno_promedio': retorno_prom,
        'espera_promedio': espera_prom,
        'procesos_completados': len(procesos)
    }