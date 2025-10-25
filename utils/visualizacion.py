import matplotlib.pyplot as plt
import numpy as np

def generar_colores(n):
    """Genera una lista de n colores distintos"""
    if n == 0:
        return []
    cmap = plt.get_cmap('tab10')
    return [cmap(i % 10) for i in range(n)]

def obtener_procesos_en_espera_por_tiempo(procesos, tiempo_maximo):
    """Calcula qué procesos estaban en espera en cada unidad de tiempo, INCLUYENDO t=0"""
    procesos_en_espera = {t: [] for t in range(tiempo_maximo + 1)}
    tiempo_ejecutado = {p['pid']: 0 for p in procesos}

    for t in range(tiempo_maximo + 1): 
        for proceso in procesos:
            pid = proceso['pid']
            tiempo_llegada = proceso['llegada']
            
            esta_ejecutando = False
            if 'ejecuciones' in proceso:
                for inicio, duracion in proceso['ejecuciones']:
                    if inicio <= t < inicio + duracion:
                        esta_ejecutando = True
                        break
            elif 'inicio' in proceso:
                 if proceso['inicio'] <= t < proceso['final']:
                     esta_ejecutando = True

            ha_llegado = t >= tiempo_llegada
            no_ha_terminado = t < proceso.get('final', tiempo_maximo + 1) 

            if ha_llegado and no_ha_terminado and not esta_ejecutando:
                 ejecutado_hasta_ahora = 0
                 if 'ejecuciones' in proceso:
                     for inicio, duracion in proceso['ejecuciones']:
                         if inicio < t: 
                            ejecutado_hasta_ahora += min(duracion, t - inicio)
                 elif 'inicio' in proceso:
                     if proceso['inicio'] < t:
                        ejecutado_hasta_ahora += min(proceso['duracion'], t - proceso['inicio'])

                 tiempo_restante = proceso['duracion'] - ejecutado_hasta_ahora
                 if tiempo_restante > 0: 
                    procesos_en_espera[t].append({'pid': pid, 'restante': tiempo_restante})

    return procesos_en_espera

def crear_grafico_gantt(procesos, tiempo_actual, algoritmo):
    """Crea un diagrama de Gantt para visualizar la ejecución y cola de espera (MODIFICADO)"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.patch.set_facecolor('#1e1f2f') 
    
    for ax in [ax1, ax2]:
        ax.set_facecolor('#292b3e')
        for spine in ax.spines.values():
            spine.set_edgecolor('#495057')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3) 
        
    ax1.set_title(f"Ejecución - Algoritmo {algoritmo}", color='white', pad=20)
    ax1.set_xlabel("Tiempo", color='white')
    ax1.set_ylabel("") 
    
    ax2.set_title("Cola de Procesos en Espera", color='white', pad=20)
    ax2.set_xlabel("Tiempo", color='white')
    ax2.set_ylabel("") 

    tiempo_maximo = max([p.get('final', 0) for p in procesos] + [tiempo_actual]) if procesos else tiempo_actual
    
    colores = generar_colores(len(procesos))
    
    for i, proceso in enumerate(procesos):
        color = colores[i]; letra = chr(65 + proceso['pid'])
        if 'ejecuciones' in proceso:
            for inicio, duracion in proceso['ejecuciones']:
                if inicio <= tiempo_actual:
                    duracion_dibujo = min(duracion, tiempo_actual - inicio)
                    if duracion_dibujo > 0: 
                        ax1.broken_barh([(inicio, duracion_dibujo)], (0, 0.8), facecolors=color, alpha=0.8)
                        ax1.text(inicio + duracion_dibujo/2, 0.4, letra, ha='center', va='center', color='white', fontweight='bold')
        elif 'inicio' in proceso and proceso['inicio'] <= tiempo_actual:
            duracion_dibujo = min(proceso['duracion'], tiempo_actual - proceso['inicio'])
            if duracion_dibujo > 0:
                ax1.broken_barh([(proceso['inicio'], duracion_dibujo)], (0, 0.8), facecolors=color, alpha=0.8)
                ax1.text(proceso['inicio'] + duracion_dibujo/2, 0.4, letra, ha='center', va='center', color='white', fontweight='bold')
                
    ax1.set_xlim(-0.5, tiempo_maximo + 1) 
    ax1.set_ylim(-0.5, 1.3)
    ax1.set_yticks([])
    ax1.set_yticklabels([])
    ax1.set_xticks(range(0, tiempo_maximo + 2, 1))
    
    procesos_en_espera = obtener_procesos_en_espera_por_tiempo(procesos, tiempo_maximo)
    
    max_procesos_espera = 0
    for t in range(tiempo_actual + 1):
        max_procesos_espera = max(max_procesos_espera, len(procesos_en_espera.get(t, [])))
    max_procesos_espera = max(1, max_procesos_espera)

    for t in range(tiempo_maximo + 1):
        if t <= tiempo_actual: 
            procesos_esperando_info = procesos_en_espera.get(t, [])
            
            procesos_esperando_info.sort(key=lambda item: item['pid'])
            
            for posicion, info_proceso in enumerate(procesos_esperando_info):
                pid = info_proceso['pid']
                restante = info_proceso['restante']
                
                proceso_idx = next(i for i, p in enumerate(procesos) if p['pid'] == pid)
                color = colores[proceso_idx]
                letra = chr(65 + pid)
                
                y_pos = max_procesos_espera - 1 - posicion 
                
                ax2.broken_barh([(t, 1)], (y_pos, 0.8), facecolors=color, alpha=0.6)
                
                texto_barra = f"{letra}{restante}"
                ax2.text(t + 0.5, y_pos + 0.4, texto_barra, ha='center', va='center', color='white', fontweight='bold', fontsize=10)
                
    ax2.set_xlim(-0.5, tiempo_maximo + 1)
    ax2.set_ylim(-0.5, max_procesos_espera - 0.5 + 0.8) 
    
    ax2.set_yticks([])
    ax2.set_xticks(range(0, tiempo_maximo + 2, 1))
    
    for ax in [ax1, ax2]:
        ax.axvline(x=tiempo_actual, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax.text(tiempo_actual, ax.get_ylim()[1], f' T={tiempo_actual}', 
               color='red', ha='left', va='top', fontweight='bold') 
        
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.3) 
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