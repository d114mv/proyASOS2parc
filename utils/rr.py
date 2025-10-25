def calcular_rr(procesos, quantum=2, cambio_contexto=0):
    """
    Implementa el algoritmo Round Robin
    """
    for p in procesos:
        p.setdefault('llegada', 0)
    
    tiempo_actual = 0
    cola = []
    tiempo_restante = {p['pid']: p['duracion'] for p in procesos}
    ejecuciones = {p['pid']: [] for p in procesos}
    procesos_terminados = set()
    
    while len(procesos_terminados) < len(procesos):
        for p in procesos:
            pid = p['pid']
            if (pid not in procesos_terminados and 
                p['llegada'] <= tiempo_actual and 
                tiempo_restante[pid] > 0 and
                p not in cola):
                cola.append(p)
        
        if cola:
            proceso_actual = cola.pop(0)
            pid = proceso_actual['pid']
            
            tiempo_a_ejecutar = min(quantum, tiempo_restante[pid])
            
            ejecuciones[pid].append((tiempo_actual, tiempo_a_ejecutar))
            
            tiempo_restante[pid] -= tiempo_a_ejecutar
            tiempo_actual += tiempo_a_ejecutar
            
            for p_nuevo in procesos:
                pid_nuevo = p_nuevo['pid']
                if (pid_nuevo not in procesos_terminados and 
                    p_nuevo['llegada'] <= tiempo_actual and 
                    tiempo_restante[pid_nuevo] > 0 and
                    p_nuevo not in cola and
                    p_nuevo != proceso_actual):
                    cola.append(p_nuevo)
            
            if tiempo_restante[pid] > 0:
                cola.append(proceso_actual)
            else:
                procesos_terminados.add(pid)
                proceso_actual['final'] = tiempo_actual
            
            if cambio_contexto > 0:
                tiempo_actual += cambio_contexto
        else:
            tiempo_actual += 1
    
    for p in procesos:
        p['ejecuciones'] = ejecuciones[p['pid']]
        
        if ejecuciones[p['pid']]:
            p['inicio'] = ejecuciones[p['pid']][0][0]
            ultima_ejecucion = ejecuciones[p['pid']][-1]
            p['final'] = ultima_ejecucion[0] + ultima_ejecucion[1]
        else:
            p['inicio'] = p['llegada']
            p['final'] = p['llegada'] + p['duracion']
        
        p['retorno'] = p['final'] - p['llegada']
        p['espera'] = p['retorno'] - p['duracion']
        p['quantum'] = quantum
    
    return procesos