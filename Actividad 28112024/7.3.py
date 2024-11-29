"""
7.3 Variantes Seleccionadas del Cuckoo Search
Ejemplo: Modified Cuckoo Search (MCS)

Diferencia clave: El MCS ajusta dinámicamente el tamaño del paso y realiza un intercambio de información entre los mejores nidos.
"""

import numpy as np

def funcion_objetivo(x):
    """Función objetivo: Rastrigin"""
    return 10 * len(x) + sum([(xi ** 2 - 10 * np.cos(2 * np.pi * xi)) for xi in x])

def levy_flight(lam):
    """Genera un paso de vuelo Lévy."""
    u = np.random.normal(0, 1) * (1 / np.abs(np.random.normal(0, 1)) ** (1 / lam))
    return u

def modified_cuckoo_search(n_nidos=15, max_iter=100, dim=5, rango=(-5, 5), Pa=0.25):
    """Algoritmo Cuckoo Search modificado."""
    nidos = np.random.uniform(rango[0], rango[1], (n_nidos, dim))
    fitness = np.array([funcion_objetivo(nido) for nido in nidos])
    mejor_solucion = nidos[np.argmin(fitness)]
    mejor_valor = min(fitness)

    for gen in range(max_iter):
        paso = 1 / np.sqrt(gen + 1)  # Disminuir el tamaño del paso
        nuevo_nido = mejor_solucion + paso * levy_flight(1.5) * np.random.uniform(rango[0], rango[1], dim)
        nuevo_fitness = funcion_objetivo(nuevo_nido)

        if nuevo_fitness < mejor_valor:
            mejor_solucion = nuevo_nido
            mejor_valor = nuevo_fitness

        # Intercambio entre las mejores soluciones
        top_nidos = nidos[np.argsort(fitness)[:3]]
        for i in range(len(top_nidos)):
            vecino = top_nidos[np.random.randint(len(top_nidos))]
            nidos[i] = (top_nidos[i] + vecino) / 2 + paso * levy_flight(1.5)

        fitness = np.array([funcion_objetivo(nido) for nido in nidos])

    return mejor_solucion, mejor_valor

# Ejecución del algoritmo
mejor_solucion, mejor_valor = modified_cuckoo_search()
print("Mejor solución modificada:", mejor_solucion)
print("Mejor valor modificado:", mejor_valor)
