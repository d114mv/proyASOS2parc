def validar_procesos(procesos):
    """Valida que la lista de procesos sea correcta"""
    if not procesos:
        return False, "No hay procesos definidos"
    
    for i, proceso in enumerate(procesos):
        if 'duracion' not in proceso or proceso['duracion'] <= 0:
            return False, f"Proceso {i}: Duración inválida"
        if 'llegada' not in proceso:
            proceso['llegada'] = 0
        if 'pid' not in proceso:
            proceso['pid'] = i
    
    return True, "Procesos válidos"

def calcular_tiempo_total(procesos):
    """Calcula el tiempo total de simulación"""
    if not procesos:
        return 0
    return max(p.get('final', 0) for p in procesos)

def formatear_tiempo(tiempo):
    """Formatea el tiempo para mostrar"""
    return f"{tiempo} ticks"