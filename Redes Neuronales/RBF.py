import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from sklearn.datasets import make_circles

# Generar datos artificiales (dos círculos concéntricos)
def generar_datos_circulos():
    X, y = make_circles(n_samples=300, factor=0.5, noise=0.05, random_state=42)
    return X, y

# Función Gaussiana para la activación de las neuronas ocultas
def funcion_gaussiana(x, c, sigma):
    return np.exp(-cdist(x, c, 'sqeuclidean') / (2 * sigma ** 2))

# Red RBF
class RBFNetwork:
    def __init__(self, num_centroides):
        self.num_centroides = num_centroides
        self.centroides = None
        self.sigma = None
        self.pesos = None

    def entrenar(self, X, y):
        # Paso 1: Encontrar centroides con K-Means
        kmeans = KMeans(n_clusters=self.num_centroides, random_state=42).fit(X)
        self.centroides = kmeans.cluster_centers_

        # Paso 2: Calcular sigma (media de las distancias entre los centroides)
        distancias = cdist(self.centroides, self.centroides, 'sqeuclidean')
        distancias[distancias == 0] = np.inf  # Evitar la diagonal (distancia a sí mismo)
        self.sigma = np.sqrt(np.mean(np.min(distancias, axis=1)))

        # Paso 3: Generar la matriz de activación
        G = funcion_gaussiana(X, self.centroides, self.sigma)

        # Verificar si G es singular y ajustarla
        if np.linalg.cond(G) > 1e10:  # Si la matriz está mal condicionada
            G += np.eye(G.shape[0]) * 1e-4  # Regularización

        # Paso 4: Calcular los pesos (pseudo-inversa)
        self.pesos = np.linalg.pinv(G).dot(y)

    def predecir(self, X):
        # Calcular la salida de la capa oculta
        G = funcion_gaussiana(X, self.centroides, self.sigma)

        # Calcular la salida final
        return np.round(G.dot(self.pesos))  # Redondear para clasificación binaria

# Visualización de resultados
def graficar_resultados(X, y, modelo):
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))
    
    Z = modelo.predecir(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    plt.contourf(xx, yy, Z, alpha=0.8, cmap=plt.cm.Paired)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors="k", cmap=plt.cm.Paired)
    plt.title("Clasificación de círculos concéntricos usando RBF")
    plt.show()

# Main
if __name__ == "__main__":
    # Generar datos artificiales
    X, y = generar_datos_circulos()

    # Crear y entrenar la red RBF
    rbf = RBFNetwork(num_centroides=10)  # Usar 10 centroides
    rbf.entrenar(X, y)

    # Realizar predicciones
    y_pred = rbf.predecir(X)
    print("Predicciones:", y_pred)
    print("Exactitud:", np.mean(y_pred == y))

    # Visualizar los resultados
    graficar_resultados(X, y, rbf)
