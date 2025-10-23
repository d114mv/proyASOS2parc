import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

def ejecutar_srt(procesos):
    """Ejecuta el algoritmo SRT y retorna los procesos con métricas"""
    # Ordenar por tiempo de llegada
    procesos_sorted = sorted(procesos, key=lambda x: x['llegada'])
    
    tiempo_actual = 0
    ejecuciones = {p['pid']: [] for p in procesos_sorted}
    restante = {p['pid']: p['duracion'] for p in procesos_sorted}
    completados = 0
    total_procesos = len(procesos_sorted)
    
    esperando = {}
    en_preparado = set()
    
    # Simulación
    while completados < total_procesos:
        # Agregar procesos que han llegado
        for p in procesos_sorted:
            pid = p['pid']
            if p['llegada'] <= tiempo_actual and restante[pid] > 0:
                if pid not in en_preparado:
                    esperando[pid] = tiempo_actual
                    en_preparado.add(pid)
        
        # Procesos disponibles
        disponibles = [p for p in procesos_sorted 
                      if p['llegada'] <= tiempo_actual and restante[p['pid']] > 0]
        
        if disponibles:
            # Ordenar por tiempo restante y tiempo de espera
            disponibles.sort(key=lambda p: (restante[p['pid']], esperando.get(p['pid'], float('inf'))))
            actual = disponibles[0]
            pid_actual = actual['pid']
            
            # Registrar ejecución
            if ejecuciones[pid_actual] and ejecuciones[pid_actual][-1][0] + ejecuciones[pid_actual][-1][1] == tiempo_actual:
                ejecuciones[pid_actual][-1] = (ejecuciones[pid_actual][-1][0], ejecuciones[pid_actual][-1][1] + 1)
            else:
                ejecuciones[pid_actual].append((tiempo_actual, 1))
            
            restante[pid_actual] -= 1
            tiempo_actual += 1
            
            if restante[pid_actual] == 0:
                completados += 1
                actual['final'] = tiempo_actual
                en_preparado.discard(pid_actual)
        else:
            tiempo_actual += 1
    
    # Calcular métricas
    for p in procesos_sorted:
        pid = p['pid']
        p['ejecuciones'] = ejecuciones[pid]
        p['inicio'] = ejecuciones[pid][0][0] if ejecuciones[pid] else p['llegada']
        p['final'] = ejecuciones[pid][-1][0] + ejecuciones[pid][-1][1] if ejecuciones[pid] else p['llegada']
        p['retorno'] = p['final'] - p['llegada']
        p['espera'] = p['retorno'] - p['duracion']
        p['algoritmo'] = "SRT"
    
    return procesos_sorted

def crear_grafico_srt(procesos):
    """Crea un diagrama de Gantt para SRT"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Diagrama de Gantt
    ax1.set_title('⚡ Diagrama de Gantt - SRT (Shortest Remaining Time)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Procesos')
    ax1.grid(True, alpha=0.3)
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(procesos)))
    
    for i, proc in enumerate(procesos):
        for inicio, duracion in proc['ejecuciones']:
            ax1.broken_barh([(inicio, duracion)], (i-0.4, 0.8), 
                           facecolors=colors[i], edgecolor='black', linewidth=1)
            # Mostrar tiempo restante
            tiempo_ejecutado = sum(d for ini, d in proc['ejecuciones'] if ini <= inicio)
            restante = proc['duracion'] - tiempo_ejecutado
            ax1.text(inicio + duracion/2, i, f"P{proc['pid']}({restante})", 
                    ha='center', va='center', fontweight='bold')
    
    ax1.set_yticks(range(len(procesos)))
    ax1.set_yticklabels([f'P{proc["pid"]}' for proc in procesos])
    
    # Tabla de resultados
    ax2.axis('off')
    tabla_data = []
    for proc in procesos:
        tabla_data.append([
            f"P{proc['pid']}",
            proc['llegada'],
            proc['duracion'],
            proc['espera'],
            proc['retorno']
        ])
    
    tabla = ax2.table(
        cellText=tabla_data,
        colLabels=['Proceso', 'Llegada', 'Duración', 'Espera', 'Retorno'],
        loc='center',
        cellLoc='center'
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    tabla.scale(1, 1.5)
    
    # Estilo de la tabla
    for i in range(len(procesos) + 1):
        for j in range(5):
            if i == 0:
                tabla[(i, j)].set_facecolor('#4CAF50')
                tabla[(i, j)].set_text_props(weight='bold', color='white')
            else:
                tabla[(i, j)].set_facecolor('#E8F5E8' if i % 2 == 0 else '#F0F8F0')
    
    plt.tight_layout()
    return fig

def calcular_metricas_srt(procesos):
    """Calcula métricas del algoritmo SRT"""
    tiempo_espera_promedio = sum(p['espera'] for p in procesos) / len(procesos)
    tiempo_retorno_promedio = sum(p['retorno'] for p in procesos) / len(procesos)
    utilizacion_cpu = sum(p['duracion'] for p in procesos) / procesos[-1]['final'] * 100
    
    return {
        'espera_promedio': tiempo_espera_promedio,
        'retorno_promedio': tiempo_retorno_promedio,
        'utilizacion_cpu': utilizacion_cpu
    }