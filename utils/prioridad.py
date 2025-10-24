def calcular_prioridad(procesos):
    """
    Implementa planificación por prioridad (no preemptivo)
    """
    # Asegurar prioridades y llegadas
    for p in procesos:
        p.setdefault('prioridad', 0)
        p.setdefault('llegada', 0)
    
    tiempo_actual = 0
    procesos_restantes = procesos.copy()
    procesos_ejecutados = []
    
    while procesos_restantes:
        # Encontrar procesos disponibles
        disponibles = [p for p in procesos_restantes if p['llegada'] <= tiempo_actual]
        
        if disponibles:
            # Ordenar por prioridad (menor número = mayor prioridad)
            disponibles.sort(key=lambda p: p['prioridad'])
            proceso_actual = disponibles[0]
            
            proceso_actual['inicio'] = tiempo_actual
            proceso_actual['final'] = tiempo_actual + proceso_actual['duracion']
            proceso_actual['retorno'] = proceso_actual['final'] - proceso_actual['llegada']
            proceso_actual['espera'] = proceso_actual['inicio'] - proceso_actual['llegada']
            
            tiempo_actual = proceso_actual['final']
            procesos_restantes.remove(proceso_actual)
            procesos_ejecutados.append(proceso_actual)
        else:
            # Avanzar al siguiente tiempo de llegada
            siguiente_llegada = min(p['llegada'] for p in procesos_restantes)
            tiempo_actual = siguiente_llegada
    
    return procesos