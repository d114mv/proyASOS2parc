import matplotlib.pyplot as plt
import numpy as np

def ejecutar_sjf(procesos):
    """Ejecuta el algoritmo SJF no preemptivo"""
    # Ordenar por duración (SJF)
    procesos_sorted = sorted(procesos, key=lambda x: x['duracion'])
    
    tiempo_actual = 0
    for i, p in enumerate(procesos_sorted):
        p['llegada'] = 0  # SJF típicamente asume llegada simultánea
        p['inicio'] = tiempo_actual
        p['final'] = p['inicio'] + p['duracion']
        p['espera'] = p['inicio']  # En SJF, espera = tiempo hasta que empieza
        p['retorno'] = p['final']  # Retorno = final (con llegada en 0)
        p['ejecuciones'] = [(p['inicio'], p['duracion'])]
        p['algoritmo'] = "SJF"
        
        tiempo_actual = p['final']
    
    return procesos_sorted

def crear_grafico_sjf(procesos):
    """Crea un diagrama de Gantt para SJF"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Diagrama de Gantt
    ax1.set_title('🟡 Diagrama de Gantt - SJF (Shortest Job First)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Procesos')
    ax1.grid(True, alpha=0.3)
    
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(procesos)))
    
    for i, proc in enumerate(procesos):
        ax1.broken_barh([(proc['inicio'], proc['duracion'])], (i-0.4, 0.8), 
                       facecolors=colors[i], edgecolor='black', linewidth=1)
        ax1.text(proc['inicio'] + proc['duracion']/2, i, f"P{proc['pid']}", 
                ha='center', va='center', fontweight='bold')
    
    ax1.set_yticks(range(len(procesos)))
    ax1.set_yticklabels([f'P{proc["pid"]}' for proc in procesos])
    
    # Tabla de resultados
    ax2.axis('off')
    tabla_data = []
    for proc in procesos:
        tabla_data.append([
            f"P{proc['pid']}",
            proc['duracion'],
            proc['espera'],
            proc['retorno']
        ])
    
    tabla = ax2.table(
        cellText=tabla_data,
        colLabels=['Proceso', 'Duración', 'Espera', 'Retorno'],
        loc='center',
        cellLoc='center'
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)
    
    # Estilo de la tabla
    for i in range(len(procesos) + 1):
        for j in range(4):
            if i == 0:
                tabla[(i, j)].set_facecolor('#FF9800')
                tabla[(i, j)].set_text_props(weight='bold', color='white')
            else:
                tabla[(i, j)].set_facecolor('#FFF3E0' if i % 2 == 0 else '#FFE0B2')
    
    plt.tight_layout()
    return fig

def calcular_metricas_sjf(procesos):
    """Calcula métricas del algoritmo SJF"""
    tiempo_espera_promedio = sum(p['espera'] for p in procesos) / len(procesos)
    tiempo_retorno_promedio = sum(p['retorno'] for p in procesos) / len(procesos)
    utilizacion_cpu = sum(p['duracion'] for p in procesos) / procesos[-1]['final'] * 100
    
    return {
        'espera_promedio': tiempo_espera_promedio,
        'retorno_promedio': tiempo_retorno_promedio,
        'utilizacion_cpu': utilizacion_cpu
    }