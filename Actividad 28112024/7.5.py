"""
7.5 Algoritmo de Optimización del Cuco (COA)
Ejemplo: Simulación básica del COA

Explicación: Este algoritmo extiende Cuckoo Search al considerar el Radio de Deposición de Huevos (ELR) y la migración hacia mejores hábitats.
"""

import numpy as np

def funcion_objetivo(x):
    """Función objetivo: Rastrigin"""
    return 10 * len(x) + sum([(xi ** 2 - 10 * np.cos(2 * np.pi * xi)) for xi in x])


def cuckoo_optimization_algorithm(n_cuckoos=10, max_iter=50, dim=5, rango=(-5, 5)):
    """Implementación básica del algoritmo de Optimización del Cuco."""
    habitats = np.random.uniform(rango[0], rango[1], (n_cuckoos, dim))
    eggs = np.random.randint(5, 20, n_cuckoos)  # Huevos por hábitat
    elr = (rango[1] - rango[0]) * (eggs / max(eggs))  # Radio de deposición

    for _ in range(max_iter):
        for i, habitat in enumerate(habitats):
            # Generar huevos dentro del rango ELR
            huevos = habitat + np.random.uniform(-elr[i], elr[i], (eggs[i], dim))
            fitness_huevos = [funcion_objetivo(huevo) for huevo in huevos]
            mejor_huevo = huevos[np.argmin(fitness_huevos)]

            # Migración si el huevo es mejor que el hábitat actual
            if funcion_objetivo(mejor_huevo) < funcion_objetivo(habitat):
                habitats[i] = mejor_huevo

    mejor_habitat = habitats[np.argmin([funcion_objetivo(habitat) for habitat in habitats])]
    return mejor_habitat

# Ejecución del COA
mejor_habitat = cuckoo_optimization_algorithm()
print("Mejor hábitat:", mejor_habitat)
