import matplotlib.pyplot as plt
import numpy as np

# --- 1. Generador de Colores ---
def generar_colores_nuevos(n):
    """Genera una lista de n colores distintos usando el mapa de color HSV."""
    if n == 0:
        return []
    cmap = plt.get_cmap('hsv')
    return [cmap(i) for i in np.linspace(0, 0.9, n)]

# --- 2. Funciones de Dibujo para SRT ---

def dibujar_tabla_st(ax_tabla, procesos):
    """Dibuja la tabla de métricas en el 'ax' proporcionado."""
    ax_tabla.clear()
    ax_tabla.axis('off')

    if not procesos:
        return

    # Columnas para SRT
    columnas = ["N", "Llegada", "Duración", "Retorno", "Espera"]
    filas = [[chr(65 + p['pid']), p['llegada'], p['duracion'], p['retorno'], p['espera']] for p in procesos]
    
    retorno_total = sum(p['retorno'] for p in procesos)
    espera_total = sum(p['espera'] for p in procesos)

    tabla = ax_tabla.table(
        cellText=filas,
        colLabels=columnas,
        loc='center',
        cellLoc='center',
        colColours=["#495057"] * len(columnas)
    )
    tabla.scale(1.0, 1.5)
    tabla.set_fontsize(11)

    for key, cell in tabla.get_celld().items():
        cell.set_edgecolor('#6c757d')
        cell.set_linewidth(0.6)
        if key[0] == 0:
            cell.set_text_props(weight='bold', color='#dee2e6')

    n = len(procesos)
    if n > 0:
        prom_retorno = round(retorno_total / n, 2)
        prom_espera = round(espera_total / n, 2)
        ax_tabla.text(
            0.5, -0.15,
            f"Promedio Retorno: {prom_retorno}     Promedio Espera: {prom_espera}",
            transform=ax_tabla.transAxes,
            ha='center', va='top',
            fontsize=11, color="#adb5bd", style='italic'
        )

def dibujar_ejecucion_srt_st(ax_ejecucion, procesos, colores, tiempo_actual, tiempo_total):
    """Dibuja el gráfico de Gantt de ejecución SRT hasta el tiempo_actual."""
    ax_ejecucion.clear()
    
    # Definimos un tamaño de ventana
    ventana_tamaño = 30
    ventana_inicio = max(0, min(tiempo_actual - ventana_tamaño // 2, tiempo_total - ventana_tamaño))
    if tiempo_total < ventana_tamaño:
        ventana_inicio = 0
        ventana_tamaño = max(10, tiempo_total)

    ax_ejecucion.set_xlim(ventana_inicio, ventana_inicio + ventana_tamaño)
    ax_ejecucion.set_ylim(0, 1)
    
    ticks = np.arange(int(ventana_inicio), int(ventana_inicio + ventana_tamaño) + 1)
    ax_ejecucion.set_xticks(ticks + 0.5)
    ax_ejecucion.set_xticklabels(ticks)
    ax_ejecucion.tick_params(axis='x', colors='white')
    ax_ejecucion.set_yticks([])
    ax_ejecucion.set_title("⚡ Ejecución SRT", color='white', fontsize=12, fontweight='bold')

    # Rejilla
    for i in ticks:
        ax_ejecucion.axvline(i, color='white', linewidth=0.5, linestyle=':')

    # Dibujar ejecuciones hasta el tiempo actual
    for t in range(tiempo_actual):
        encontrado = False
        for p in procesos:
            pid = p['pid']
            letra = chr(65 + pid)
            color = colores[pid % len(colores)]
            
            # Para SRT, revisamos cada segmento de ejecución
            for inicio, duracion in p.get('ejecuciones', []):
                if inicio <= t < inicio + duracion:
                    # Calcular tiempo restante en ese momento
                    tiempo_ejecutado_hasta_t = sum(
                        min(duracion_seg, max(0, t - inicio_seg + 1)) 
                        for inicio_seg, duracion_seg in p.get('ejecuciones', [])
                        if inicio_seg <= t
                    )
                    restante = p['duracion'] - tiempo_ejecutado_hasta_t
                    
                    ax_ejecucion.broken_barh([(t, 1)], (0, 1), facecolors=color)
                    texto = f"{letra}{restante}" if restante > 0 else letra
                    ax_ejecucion.text(t + 0.5, 0.5, texto, ha='center', va='center', 
                                    color='black', fontweight='bold', fontsize=9)
                    encontrado = True
                    break
            if encontrado:
                break
        
        if not encontrado and t >= 0:
            ax_ejecucion.broken_barh([(t, 1)], (0, 1), facecolors='#292b3e')
            ax_ejecucion.text(t + 0.5, 0.5, "⌀", ha='center', va='center', color='white')

def dibujar_preparado_srt_st(ax_preparado, procesos, colores, tiempo_actual, tiempo_total):
    """Dibuja la cola de preparados para SRT."""
    ax_preparado.clear()
    n_procesos = len(procesos)

    ventana_tamaño = 30
    ventana_inicio = max(0, min(tiempo_actual - ventana_tamaño // 2, tiempo_total - ventana_tamaño))
    if tiempo_total < ventana_tamaño:
        ventana_inicio = 0
        ventana_tamaño = max(10, tiempo_total)

    ax_preparado.set_xlim(ventana_inicio, ventana_inicio + ventana_tamaño)
    ax_preparado.set_ylim(0, max(1, n_procesos))

    ticks = np.arange(int(ventana_inicio), int(ventana_inicio + ventana_tamaño) + 1)
    ax_preparado.set_xticks(ticks + 0.5)
    ax_preparado.set_xticklabels(ticks)
    ax_preparado.tick_params(axis='x', colors='white')
    ax_preparado.set_yticks([])
    ax_preparado.set_title("📋 Cola de Preparados SRT", color='white', fontsize=12, fontweight='bold')

    for i in ticks:
        ax_preparado.axvline(i, color='white', linewidth=0.5, linestyle=':')
    for i in range(n_procesos + 1):
        ax_preparado.axhline(i, color='white', linewidth=0.5)

    # Lógica específica para SRT
    for t in range(tiempo_actual):
        en_preparado = []
        
        for p in procesos:
            # Calcular tiempo ejecutado hasta t
            tiempo_ejecutado = sum(
                min(duracion, max(0, t - inicio + 1)) 
                for inicio, duracion in p.get('ejecuciones', [])
                if inicio <= t
            )
            restante = p['duracion'] - tiempo_ejecutado
            
            # Está en preparado si: llegó, no ha terminado y no está ejecutándose en t
            esta_ejecutando = any(
                inicio <= t < inicio + duracion 
                for inicio, duracion in p.get('ejecuciones', [])
            )
            
            if (p['llegada'] <= t and restante > 0 and not esta_ejecutando):
                en_preparado.append((p, restante, p['llegada']))

        if not en_preparado:
            en_preparado = [(-1, 0, 0)]

        # Ordenar por tiempo restante (SRT)
        en_preparado.sort(key=lambda x: (x[1], x[2]))

        for fila, (proc, restante, _) in enumerate(en_preparado):
            y_pos = n_procesos - fila - 1
            if proc == -1:
                ax_preparado.broken_barh([(t, 1)], (y_pos, 1), facecolors='#292b3e')
                ax_preparado.text(t + 0.5, y_pos + 0.5, "⌀", ha='center', va='center', color='white')
            else:
                pid = proc['pid']
                letra = chr(65 + pid)
                color = colores[pid % len(colores)]
                ax_preparado.broken_barh([(t, 1)], (y_pos, 1), facecolors=color)
                ax_preparado.text(t + 0.5, y_pos + 0.5, f"{letra}{restante}", 
                                ha='center', va='center', color='black', fontweight='bold')

# --- 3. Función Maestra de Dibujo para SRT ---

def generar_visualizacion_srt(procesos_calculados, tiempo_actual):
    """
    Crea la figura completa de Matplotlib para SRT en un tiempo_actual dado.
    """
    if not procesos_calculados:
        fig = plt.figure(figsize=(13, 6))
        fig.patch.set_facecolor('#1e1f2f')
        return fig

    # 1. Crear Figura y Ejes
    fig = plt.figure(figsize=(13, 6))
    fig.patch.set_facecolor('#1e1f2f')

    # Definir los ejes
    ax_tabla = plt.axes([0.1, 0.58, 0.8, 0.3])
    ax_ejecucion = plt.axes([0.1, 0.35, 0.8, 0.12])
    ax_preparado = plt.axes([0.1, 0.15, 0.8, 0.12])
    
    # Colores de fondo
    for ax in [ax_tabla, ax_ejecucion, ax_preparado]:
        ax.set_facecolor('#292b3e')
    
    # 2. Obtener Datos y Colores
    tiempo_total = max(p['final'] for p in procesos_calculados) if procesos_calculados else 0
    colores = generar_colores_nuevos(len(procesos_calculados))

    # 3. Llamar a las funciones de dibujo específicas para SRT
    dibujar_tabla_st(ax_tabla, procesos_calculados)
    dibujar_ejecucion_srt_st(ax_ejecucion, procesos_calculados, colores, tiempo_actual, tiempo_total)
    dibujar_preparado_srt_st(ax_preparado, procesos_calculados, colores, tiempo_actual, tiempo_total)

    fig.subplots_adjust(top=0.9, bottom=0.05, hspace=0.8)
    
    return fig