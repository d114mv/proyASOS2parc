# visualizacion.py
import matplotlib.pyplot as plt
import numpy as np

def generar_colores(n):
    """Genera una lista de n colores distintos"""
    if n == 0:
        return []
    cmap = plt.get_cmap('tab10')
    return [cmap(i % 10) for i in range(n)]

def obtener_procesos_en_espera_por_tiempo(procesos, tiempo_maximo):
    """Calcula qué procesos estaban en espera en cada unidad de tiempo"""
    procesos_en_espera = {t: [] for t in range(tiempo_maximo + 1)}
    
    for proceso in procesos:
        # Un proceso está en espera si ha llegado pero no está ejecutándose
        tiempo_llegada = proceso['llegada']
        
        # Obtener todos los intervalos de ejecución
        tiempos_ejecucion = set()
        if 'ejecuciones' in proceso:
            for inicio, duracion in proceso['ejecuciones']:
                for t in range(inicio, inicio + duracion):
                    tiempos_ejecucion.add(t)
        elif 'inicio' in proceso:
            for t in range(proceso['inicio'], proceso['final']):
                tiempos_ejecucion.add(t)
        
        # Para cada unidad de tiempo, verificar si el proceso está en espera
        for t in range(tiempo_maximo + 1):
            if t >= tiempo_llegada and t < proceso.get('final', tiempo_maximo) and t not in tiempos_ejecucion:
                procesos_en_espera[t].append(proceso['pid'])
    
    return procesos_en_espera

def crear_grafico_gantt(procesos, tiempo_actual, algoritmo):
    """Crea un diagrama de Gantt para visualizar la ejecución y cola de espera"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.patch.set_facecolor('#1e1f2f')
    
    # Configurar ejes
    for ax in [ax1, ax2]:
        ax.set_facecolor('#292b3e')
        for spine in ax.spines.values():
            spine.set_edgecolor('#495057')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3)
    
    # Gráfico de ejecución (ax1)
    ax1.set_title(f"Ejecución - Algoritmo {algoritmo}", color='white', pad=20)
    ax1.set_xlabel("Tiempo", color='white')
    ax1.set_ylabel("Procesos", color='white')
    
    # Gráfico de cola de preparados (ax2)
    ax2.set_title("Cola de Procesos en Espera", color='white', pad=20)
    ax2.set_xlabel("Tiempo", color='white')
    ax2.set_ylabel("")  # Sin label en el eje Y
    
    # Calcular tiempo máximo para la visualización
    tiempo_maximo = max([p.get('final', 0) for p in procesos]) if procesos else tiempo_actual
    tiempo_maximo = max(tiempo_maximo, tiempo_actual)
    
    colores = generar_colores(len(procesos))
    
    # DIBUJAR EJECUCIÓN - TODOS LOS PROCESOS EN EL MISMO NIVEL (y=0)
    for i, proceso in enumerate(procesos):
        color = colores[i]
        letra = chr(65 + proceso['pid'])  # A, B, C, ...
        
        # Dibujar en gráfico de ejecución - TODOS EN Y=0
        if 'ejecuciones' in proceso:
            for inicio, duracion in proceso['ejecuciones']:
                if inicio <= tiempo_actual:
                    duracion_dibujo = min(duracion, tiempo_actual - inicio)
                    ax1.broken_barh([(inicio, duracion_dibujo)], (0, 0.8), 
                                  facecolors=color, alpha=0.8)
                    ax1.text(inicio + duracion_dibujo/2, 0.4, letra, 
                           ha='center', va='center', color='white', fontweight='bold')
        elif 'inicio' in proceso and proceso['inicio'] <= tiempo_actual:
            duracion_dibujo = min(proceso['duracion'], tiempo_actual - proceso['inicio'])
            ax1.broken_barh([(proceso['inicio'], duracion_dibujo)], (0, 0.8), 
                          facecolors=color, alpha=0.8)
            ax1.text(proceso['inicio'] + duracion_dibujo/2, 0.4, letra, 
                   ha='center', va='center', color='white', fontweight='bold')
    
    # Configurar límites del primer gráfico (EJECUCIÓN)
    ax1.set_xlim(0, tiempo_maximo + 1)
    ax1.set_ylim(-0.5, 1.3)
    ax1.set_yticks([0.4])
    ax1.set_yticklabels(['Ejecución'])
    
    # Configurar eje X con unidades de 1 en 1
    ax1.set_xticks(range(0, tiempo_maximo + 2, 1))
    
    # DIBUJAR COLA DE ESPERA - ORDEN ALFABÉTICO Y SIN HUECOS
    procesos_en_espera = obtener_procesos_en_espera_por_tiempo(procesos, tiempo_maximo)
    
    # Encontrar la máxima cantidad de procesos en espera en cualquier momento
    max_procesos_espera = max(len(procesos_en_espera[t]) for t in range(tiempo_maximo + 1)) if procesos_en_espera else 1
    
    for t in range(tiempo_maximo + 1):
        if t <= tiempo_actual:  # Solo mostrar hasta el tiempo actual
            procesos_esperando = procesos_en_espera[t]
            
            # Ordenar procesos alfabéticamente (A, B, C, ...)
            procesos_esperando.sort()
            
            # Dibujar cada proceso en su posición ordenada sin huecos
            for posicion, pid in enumerate(procesos_esperando):
                proceso_idx = next(i for i, p in enumerate(procesos) if p['pid'] == pid)
                color = colores[proceso_idx]
                letra = chr(65 + pid)
                
                # Posición Y: 0 para el primero, 1 para el segundo, etc. (sin huecos)
                y_pos = posicion
                
                ax2.broken_barh([(t, 1)], (y_pos, 0.8), 
                              facecolors=color, alpha=0.6)
                ax2.text(t + 0.5, y_pos + 0.4, letra, 
                       ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    
    # Configurar límites del segundo gráfico (COLA DE ESPERA)
    ax2.set_xlim(0, tiempo_maximo + 1)
    ax2.set_ylim(-0.5, max_procesos_espera + 0.5)
    
    # Remover labels del eje Y completamente
    ax2.set_yticks([])
    
    # Configurar eje X con unidades de 1 en 1
    ax2.set_xticks(range(0, tiempo_maximo + 2, 1))
    
    # Añadir línea de tiempo actual
    for ax in [ax1, ax2]:
        ax.axvline(x=tiempo_actual, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax.text(tiempo_actual, ax.get_ylim()[1] - 0.2, f'T={tiempo_actual}', 
               color='red', ha='center', va='top', fontweight='bold')
    
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