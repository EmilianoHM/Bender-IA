"""
7.2 Fundamentos del Algoritmo Cuckoo Search (CS)
Ejemplo: Implementación básica del Cuckoo Search

Explicación:
Inicialización: Genera una población inicial de nidos dentro del rango especificado.
Vuelo Lévy: Utiliza el vuelo Lévy para explorar nuevas soluciones.
Reemplazo: Los nidos de baja calidad son reemplazados por nuevos aleatorios.
Criterio de parada: El algoritmo itera hasta alcanzar el número máximo de iteraciones.
"""

import numpy as np

def funcion_objetivo(x):
    """Función objetivo: Rastrigin"""
    return 10 * len(x) + sum([(xi ** 2 - 10 * np.cos(2 * np.pi * xi)) for xi in x])

def levy_flight(lam):
    """Genera un paso de vuelo Lévy."""
    u = np.random.normal(0, 1) * (1 / np.abs(np.random.normal(0, 1)) ** (1 / lam))
    return u

def cuckoo_search(n_nidos=15, max_iter=100, dim=5, rango=(-5, 5), Pa=0.25):
    """Implementación básica del algoritmo Cuckoo Search."""
    # Inicializar los nidos aleatoriamente
    nidos = np.random.uniform(rango[0], rango[1], (n_nidos, dim))
    fitness = np.array([funcion_objetivo(nido) for nido in nidos])
    
    mejor_solucion = nidos[np.argmin(fitness)]
    mejor_valor = min(fitness)

    for _ in range(max_iter):
        # Generar un nuevo nido mediante vuelo Lévy
        nuevo_nido = mejor_solucion + levy_flight(1.5) * np.random.uniform(rango[0], rango[1], dim)
        nuevo_fitness = funcion_objetivo(nuevo_nido)
        
        # Reemplazar si el nuevo nido es mejor
        if nuevo_fitness < mejor_valor:
            mejor_solucion = nuevo_nido
            mejor_valor = nuevo_fitness

        # Reemplazar una fracción Pa de los peores nidos
        for i in range(int(n_nidos * Pa)):
            nidos[np.random.randint(n_nidos)] = np.random.uniform(rango[0], rango[1], dim)

        # Actualizar fitness
        fitness = np.array([funcion_objetivo(nido) for nido in nidos])

    return mejor_solucion, mejor_valor

# Ejecución del algoritmo
mejor_solucion, mejor_valor = cuckoo_search()
print("Mejor solución:", mejor_solucion)
print("Mejor valor:", mejor_valor)
