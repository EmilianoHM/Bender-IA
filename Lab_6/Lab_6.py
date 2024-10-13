import numpy as np
import random
import math

# Función de Himmelblau
def funcion_himmelblau(x, y):
    """
    Calcula el valor de la función de Himmelblau dada una pareja de coordenadas (x, y).
    
    Parámetros:
    x (float): Coordenada x.
    y (float): Coordenada y.
    
    Retorna:
    float: El valor de la función de Himmelblau en el punto (x, y).
    """
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

# Algoritmo de Recocido Simulado
def recocido_simulado(limites, max_iteraciones, temp_inicial, alfa):
    """
    Implementa el algoritmo de recocido simulado para minimizar la función de Himmelblau.
    
    Parámetros:
    limites (list): Lista con dos valores [min, max] que definen los límites del rango de búsqueda para x e y.
    max_iteraciones (int): Número máximo de iteraciones que realizará el algoritmo.
    temp_inicial (float): Temperatura inicial del recocido simulado, que afecta la probabilidad de aceptar soluciones peores.
    alfa (float): Factor de enfriamiento que determina cómo se reduce la temperatura en cada iteración.
    
    Retorna:
    tuple: Una tupla que contiene las mejores coordenadas encontradas (mejor_x, mejor_y) 
           y el costo mínimo asociado (mejor_costo).
    """
    
    # Generar un punto inicial aleatorio dentro de los límites establecidos
    x = random.uniform(limites[0], limites[1])
    y = random.uniform(limites[0], limites[1])
    
    # Evaluar la función objetivo en el punto inicial (costo inicial)
    costo_actual = funcion_himmelblau(x, y)
    
    # Almacenar el mejor punto encontrado hasta ahora
    mejor_x, mejor_y = x, y
    mejor_costo = costo_actual
    
    # Establecer la temperatura inicial
    temperatura = temp_inicial
    
    # Bucle principal del algoritmo
    for i in range(max_iteraciones):
        # Generar un nuevo punto vecino aleatorio agregando un pequeño valor a las coordenadas actuales
        x_nuevo = x + random.uniform(-0.01, 0.01)
        y_nuevo = y + random.uniform(-0.01, 0.01)
        
        # Asegurarse de que el nuevo punto esté dentro de los límites definidos
        x_nuevo = max(min(x_nuevo, limites[1]), limites[0])
        y_nuevo = max(min(y_nuevo, limites[1]), limites[0])
        
        # Evaluar la función objetivo en el nuevo punto
        nuevo_costo = funcion_himmelblau(x_nuevo, y_nuevo)
        
        # Calcular el cambio en la función objetivo (diferencia de costos entre el punto actual y el nuevo)
        delta_costo = nuevo_costo - costo_actual
        
        # Condiciones para aceptar el nuevo punto:
        # Si el nuevo costo es menor, se acepta automáticamente.
        # Si es mayor, se acepta con una probabilidad dependiente de la temperatura.
        if delta_costo < 0 or random.random() < math.exp(-delta_costo / temperatura):
            # Actualizar las coordenadas actuales y el costo si se acepta el nuevo punto
            x, y = x_nuevo, y_nuevo
            costo_actual = nuevo_costo
        
        # Actualizar la mejor solución encontrada
        if costo_actual < mejor_costo:
            mejor_x, mejor_y = x, y
            mejor_costo = costo_actual
        
        # Enfriar la temperatura multiplicándola por el factor alfa
        temperatura *= alfa
    
    # Imprimir los parámetros utilizados
    print(f"Parámetros del recocido simulado:\n - Temperatura inicial: {temp_inicial}\n - Factor de enfriamiento: {alfa}\n - Iteraciones máximas: {max_iteraciones}")
    
    # Devolver las mejores coordenadas encontradas y el costo asociado
    return mejor_x, mejor_y, mejor_costo

# Parámetros ajustados para el recocido simulado
limites = [-5, 5]  # Límites de búsqueda
max_iteraciones = 50000  # Mayor número de iteraciones para exploración
temp_inicial = 10000  # Alta temperatura inicial
alfa = 0.9995  # Enfriamiento lento

# Ejecutar el algoritmo de recocido simulado
mejor_x, mejor_y, mejor_costo = recocido_simulado(limites, max_iteraciones, temp_inicial, alfa)

print(f"Los valores mínimos encontrados son: x = {mejor_x}, y = {mejor_y}")
print(f"El valor mínimo de la función es: {mejor_costo}")
