def calcular_estadisticas(lista_tiempos):
    if lista_tiempos:
        mejor_tiempo = min(lista_tiempos)
        peor_tiempo = max(lista_tiempos)
        tiempo_promedio = sum(lista_tiempos) / len(lista_tiempos)
    else:
        mejor_tiempo = peor_tiempo = tiempo_promedio = 0

    return mejor_tiempo, peor_tiempo, tiempo_promedio