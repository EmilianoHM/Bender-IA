"""
7.4 Aplicaciones Representativas del Cuckoo Search
Ejemplo: Optimización de un problema de clustering

Explicación: Este ejemplo utiliza Cuckoo Search para encontrar los mejores centroides de clustering, optimizando la puntuación Silhouette.
"""

from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score
import numpy as np

# Generar datos de ejemplo
data, _ = make_blobs(n_samples=100, centers=3, cluster_std=1.0, random_state=42)

def fitness_clustering(nidos, data):
    """Calcula la puntuación Silhouette como fitness."""
    scores = []
    for nido in nidos:
        etiquetas = np.argmin(np.linalg.norm(data[:, None] - nido[None, :], axis=2), axis=1)
        scores.append(silhouette_score(data, etiquetas))
    return scores

# Ejecución del algoritmo de clustering con Cuckoo Search
n_nidos = 10
dim = 3  # Tres centroides
rango = (data.min(axis=0), data.max(axis=0))

nidos = np.random.uniform(rango[0], rango[1], (n_nidos, dim, data.shape[1]))
fitness = fitness_clustering(nidos, data)
mejor_solucion = nidos[np.argmax(fitness)]

print("Mejores centroides:", mejor_solucion)
