import matplotlib.pyplot as plt
import numpy as np

def generar_colores(n):
    """Genera una lista de n colores distintos"""
    if n == 0:
        return []
    cmap = plt.get_cmap('tab10') # Mantenemos el colormap original del amigo
    return [cmap(i % 10) for i in range(n)]

def obtener_procesos_en_espera_por_tiempo(procesos, tiempo_maximo):
    """Calcula qué procesos estaban en espera en cada unidad de tiempo, INCLUYENDO t=0"""
    # CAMBIO 1: Incluimos t=0 correctamente
    procesos_en_espera = {t: [] for t in range(tiempo_maximo + 1)}
    tiempo_ejecutado = {p['pid']: 0 for p in procesos} # Para calcular restante

    for t in range(tiempo_maximo + 1): # Iteramos desde t=0
        for proceso in procesos:
            pid = proceso['pid']
            tiempo_llegada = proceso['llegada']
            
            # ¿Está ejecutándose EN ESTE MOMENTO (t)?
            esta_ejecutando = False
            if 'ejecuciones' in proceso:
                for inicio, duracion in proceso['ejecuciones']:
                    if inicio <= t < inicio + duracion:
                        esta_ejecutando = True
                        break
            elif 'inicio' in proceso:
                 if proceso['inicio'] <= t < proceso['final']:
                     esta_ejecutando = True

            # ¿Está en espera? (Llegó, no ha terminado, no está ejecutando)
            ha_llegado = t >= tiempo_llegada
            no_ha_terminado = t < proceso.get('final', tiempo_maximo + 1) # Aseguramos que termine después

            if ha_llegado and no_ha_terminado and not esta_ejecutando:
                 # Calculamos cuánto tiempo ha ejecutado HASTA ANTES de este tick 't'
                 ejecutado_hasta_ahora = 0
                 if 'ejecuciones' in proceso:
                     for inicio, duracion in proceso['ejecuciones']:
                         if inicio < t: # Solo contar ejecuciones pasadas
                            ejecutado_hasta_ahora += min(duracion, t - inicio)
                 elif 'inicio' in proceso:
                     if proceso['inicio'] < t:
                        ejecutado_hasta_ahora += min(proceso['duracion'], t - proceso['inicio'])

                 tiempo_restante = proceso['duracion'] - ejecutado_hasta_ahora
                 if tiempo_restante > 0: # Solo añadir si aún queda por ejecutar
                    procesos_en_espera[t].append({'pid': pid, 'restante': tiempo_restante})

    return procesos_en_espera

def crear_grafico_gantt(procesos, tiempo_actual, algoritmo):
    """Crea un diagrama de Gantt para visualizar la ejecución y cola de espera (MODIFICADO)"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.patch.set_facecolor('#1e1f2f') # Mantenemos estilo original
    
    # Configurar ejes (Mantenemos estilo original)
    for ax in [ax1, ax2]:
        ax.set_facecolor('#292b3e')
        for spine in ax.spines.values():
            spine.set_edgecolor('#495057')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.3) # Mantenemos rejilla original
        
    # Gráfico de ejecución (ax1)
    ax1.set_title(f"Ejecución - Algoritmo {algoritmo}", color='white', pad=20)
    ax1.set_xlabel("Tiempo", color='white')
    # CAMBIO 2: Quitamos el label Y de ejecución
    ax1.set_ylabel("") 
    
    # Gráfico de cola de preparados (ax2)
    ax2.set_title("Cola de Procesos en Espera", color='white', pad=20)
    ax2.set_xlabel("Tiempo", color='white')
    ax2.set_ylabel("") 

    tiempo_maximo = max([p.get('final', 0) for p in procesos] + [tiempo_actual]) if procesos else tiempo_actual
    
    colores = generar_colores(len(procesos))
    
    # DIBUJAR EJECUCIÓN (Sin cambios significativos aquí, excepto quitar Y label)
    for i, proceso in enumerate(procesos):
        color = colores[i]; letra = chr(65 + proceso['pid'])
        if 'ejecuciones' in proceso:
            for inicio, duracion in proceso['ejecuciones']:
                if inicio <= tiempo_actual:
                    duracion_dibujo = min(duracion, tiempo_actual - inicio)
                    if duracion_dibujo > 0: # Evitar dibujar barras de tamaño 0
                        ax1.broken_barh([(inicio, duracion_dibujo)], (0, 0.8), facecolors=color, alpha=0.8)
                        ax1.text(inicio + duracion_dibujo/2, 0.4, letra, ha='center', va='center', color='white', fontweight='bold')
        elif 'inicio' in proceso and proceso['inicio'] <= tiempo_actual:
            duracion_dibujo = min(proceso['duracion'], tiempo_actual - proceso['inicio'])
            if duracion_dibujo > 0:
                ax1.broken_barh([(proceso['inicio'], duracion_dibujo)], (0, 0.8), facecolors=color, alpha=0.8)
                ax1.text(proceso['inicio'] + duracion_dibujo/2, 0.4, letra, ha='center', va='center', color='white', fontweight='bold')
                
    ax1.set_xlim(-0.5, tiempo_maximo + 1) # Ajuste leve para ver el 0
    ax1.set_ylim(-0.5, 1.3)
    # CAMBIO 2: Quitamos los ticks y labels Y
    ax1.set_yticks([])
    ax1.set_yticklabels([])
    ax1.set_xticks(range(0, tiempo_maximo + 2, 1))
    
    # DIBUJAR COLA DE ESPERA
    procesos_en_espera = obtener_procesos_en_espera_por_tiempo(procesos, tiempo_maximo)
    
    # Encontrar la máxima cantidad de procesos en espera en cualquier momento VISIBLE
    max_procesos_espera = 0
    for t in range(tiempo_actual + 1):
        max_procesos_espera = max(max_procesos_espera, len(procesos_en_espera.get(t, [])))
    max_procesos_espera = max(1, max_procesos_espera) # Mínimo 1 fila

    # CAMBIO 1: Iteramos desde t=0
    for t in range(tiempo_maximo + 1):
        if t <= tiempo_actual: # Solo mostrar hasta el tiempo actual
            procesos_esperando_info = procesos_en_espera.get(t, [])
            
            # Ordenar procesos por PID (A, B, C...) - Mantenemos esto
            procesos_esperando_info.sort(key=lambda item: item['pid'])
            
            # CAMBIO 3: Invertir el orden de dibujo vertical
            for posicion, info_proceso in enumerate(procesos_esperando_info):
                pid = info_proceso['pid']
                restante = info_proceso['restante']
                
                proceso_idx = next(i for i, p in enumerate(procesos) if p['pid'] == pid)
                color = colores[proceso_idx]
                letra = chr(65 + pid)
                
                # y_pos invertido: 0 es la fila de más arriba
                y_pos = max_procesos_espera - 1 - posicion 
                
                ax2.broken_barh([(t, 1)], (y_pos, 0.8), facecolors=color, alpha=0.6)
                
                # CAMBIO 4: Mostrar Letra + Restante
                texto_barra = f"{letra}{restante}"
                ax2.text(t + 0.5, y_pos + 0.4, texto_barra, ha='center', va='center', color='white', fontweight='bold', fontsize=10)
                
    ax2.set_xlim(-0.5, tiempo_maximo + 1) # Ajuste leve
    # Ajustamos ylim para que coincida con la altura calculada
    ax2.set_ylim(-0.5, max_procesos_espera - 0.5 + 0.8) # -0.5 a (altura_max - 1) + 0.8 + 0.2 margen
    
    # CAMBIO 2: Quitamos los labels del eje Y
    ax2.set_yticks([])
    ax2.set_xticks(range(0, tiempo_maximo + 2, 1))
    
    # Añadir línea de tiempo actual (Mantenemos original)
    for ax in [ax1, ax2]:
        ax.axvline(x=tiempo_actual, color='red', linestyle='--', alpha=0.7, linewidth=2)
        ax.text(tiempo_actual, ax.get_ylim()[1], f' T={tiempo_actual}', # Ajuste leve para no superponer
               color='red', ha='left', va='top', fontweight='bold') # Cambiado a 'left'
        
    plt.tight_layout()
    # Ajustar espaciado entre subplots si es necesario
    plt.subplots_adjust(hspace=0.3) 
    return fig

# La función mostrar_metricas no necesita cambios
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