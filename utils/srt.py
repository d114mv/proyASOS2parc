def calcular_srt(procesos):
    """
    Toma una lista de procesos (dict) con 'duracion' y 'llegada'
    y devuelve una nueva lista con todos los tiempos calculados usando SRT.
    """
    
    # Asignamos un PID a cada proceso
    procesos_con_pid = [dict(p, pid=i) for i, p in enumerate(procesos)]
    procesos_con_pid.sort(key=lambda p: p['llegada'])
    
    # Inicialización de variables para SRT
    tiempo_actual = 0
    ejecuciones = {p['pid']: [] for p in procesos_con_pid}
    restante = {p['pid']: p['duracion'] for p in procesos_con_pid}
    completados = 0
    total_procesos = len(procesos_con_pid)
    
    esperando = {}
    en_preparado = set()
    
    # Simulación SRT
    while completados < total_procesos:
        # Agregar procesos que han llegado
        for p in procesos_con_pid:
            pid = p['pid']
            if p['llegada'] <= tiempo_actual and restante[pid] > 0:
                if pid not in en_preparado:
                    esperando[pid] = tiempo_actual
                    en_preparado.add(pid)
        
        # Procesos disponibles
        disponibles = [p for p in procesos_con_pid 
                      if p['llegada'] <= tiempo_actual and restante[p['pid']] > 0]
        
        if disponibles:
            # Ordenar por tiempo restante (SRT)
            disponibles.sort(key=lambda p: (restante[p['pid']], esperando.get(p['pid'], float('inf'))))
            actual = disponibles[0]
            pid_actual = actual['pid']
            
            # Registrar ejecución
            if (ejecuciones[pid_actual] and 
                ejecuciones[pid_actual][-1][0] + ejecuciones[pid_actual][-1][1] == tiempo_actual):
                # Extender ejecución existente
                ejecuciones[pid_actual][-1] = (ejecuciones[pid_actual][-1][0], 
                                             ejecuciones[pid_actual][-1][1] + 1)
            else:
                # Nueva ejecución
                ejecuciones[pid_actual].append((tiempo_actual, 1))
            
            restante[pid_actual] -= 1
            
            if restante[pid_actual] == 0:
                completados += 1
                actual['final'] = tiempo_actual + 1
                en_preparado.discard(pid_actual)
        
        tiempo_actual += 1
    
    # Calcular métricas finales
    procesos_calculados = []
    for p in procesos_con_pid:
        pid = p['pid']
        p['ejecuciones'] = ejecuciones[pid]
        if ejecuciones[pid]:
            p['inicio'] = ejecuciones[pid][0][0]
            p['final'] = ejecuciones[pid][-1][0] + ejecuciones[pid][-1][1]
            p['retorno'] = p['final'] - p['llegada']
            p['espera'] = p['retorno'] - p['duracion']
        else:
            p['inicio'] = p['llegada']
            p['final'] = p['llegada']
            p['retorno'] = 0
            p['espera'] = 0
        
        procesos_calculados.append(p)
    
    # Ordenar por PID para consistencia
    procesos_calculados.sort(key=lambda p: p['pid'])
    return procesos_calculados