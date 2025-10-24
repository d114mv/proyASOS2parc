def calcular_fcfs(procesos):
    """
    Implementa el algoritmo First Come First Served
    """
    # Ordenar por tiempo de llegada
    procesos.sort(key=lambda p: p['llegada'])
    
    tiempo_actual = 0
    for proceso in procesos:
        # Esperar si el proceso llega después del tiempo actual
        if tiempo_actual < proceso['llegada']:
            tiempo_actual = proceso['llegada']
        
        proceso['inicio'] = tiempo_actual
        proceso['final'] = tiempo_actual + proceso['duracion']
        proceso['retorno'] = proceso['final'] - proceso['llegada']
        proceso['espera'] = proceso['inicio'] - proceso['llegada']
        
        tiempo_actual = proceso['final']
    
    return procesos