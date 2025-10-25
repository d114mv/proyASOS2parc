def calcular_sjf(procesos):
    """
    Implementa el algoritmo Shortest Job First (no preemptivo)
    """
    for p in procesos:
        p.setdefault('llegada', 0)
    
    tiempo_actual = 0
    procesos_restantes = procesos.copy()
    procesos_ejecutados = []
    
    while procesos_restantes:
        disponibles = [p for p in procesos_restantes if p['llegada'] <= tiempo_actual]
        
        if disponibles:
            disponibles.sort(key=lambda p: p['duracion'])
            proceso_actual = disponibles[0]
            
            proceso_actual['inicio'] = tiempo_actual
            proceso_actual['final'] = tiempo_actual + proceso_actual['duracion']
            proceso_actual['retorno'] = proceso_actual['final'] - proceso_actual['llegada']
            proceso_actual['espera'] = proceso_actual['inicio'] - proceso_actual['llegada']
            
            tiempo_actual = proceso_actual['final']
            procesos_restantes.remove(proceso_actual)
            procesos_ejecutados.append(proceso_actual)
        else:
            siguiente_llegada = min(p['llegada'] for p in procesos_restantes)
            tiempo_actual = siguiente_llegada
    
    return procesos