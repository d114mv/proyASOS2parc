def calcular_srt(procesos):
    """
    Implementa el algoritmo Shortest Remaining Time (preemptivo)
    """
    for p in procesos:
        p.setdefault('llegada', 0)
    
    procesos.sort(key=lambda p: p['llegada'])
    
    tiempo_actual = 0
    ejecuciones = {p['pid']: [] for p in procesos}
    restante = {p['pid']: p['duracion'] for p in procesos}
    completados = 0
    total_procesos = len(procesos)
    
    while completados < total_procesos:
        disponibles = [p for p in procesos if p['llegada'] <= tiempo_actual and restante[p['pid']] > 0]
        
        if disponibles:
            disponibles.sort(key=lambda p: restante[p['pid']])
            actual = disponibles[0]
            pid = actual['pid']
            
            if not ejecuciones[pid] or ejecuciones[pid][-1][0] + ejecuciones[pid][-1][1] < tiempo_actual:
                ejecuciones[pid].append((tiempo_actual, 1))
            else:
                ejecuciones[pid][-1] = (ejecuciones[pid][-1][0], ejecuciones[pid][-1][1] + 1)
                
            restante[pid] -= 1
            tiempo_actual += 1
            
            if restante[pid] == 0:
                completados += 1
                actual['final'] = tiempo_actual
        else:
            procesos_pendientes = [p for p in procesos if p['llegada'] > tiempo_actual and restante[p['pid']] > 0]
            if procesos_pendientes:
                siguiente_llegada = min(p['llegada'] for p in procesos_pendientes)
                tiempo_actual = siguiente_llegada
            else:
                tiempo_actual += 1
    
    for p in procesos:
        p['ejecuciones'] = ejecuciones[p['pid']]
        if ejecuciones[p['pid']]:
            p['inicio'] = ejecuciones[p['pid']][0][0]
            p['final'] = ejecuciones[p['pid']][-1][0] + ejecuciones[p['pid']][-1][1]
            p['retorno'] = p['final'] - p['llegada']
            p['espera'] = p['retorno'] - p['duracion']
        else:
            p['inicio'] = p['llegada']
            p['final'] = p['llegada'] + p['duracion']
            p['retorno'] = p['duracion']
            p['espera'] = 0
        
        p.setdefault('prioridad', 0)
    
    return procesos