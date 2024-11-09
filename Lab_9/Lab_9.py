import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, KFold, LeaveOneOut
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.datasets import load_iris, load_wine, load_digits
from scipy.spatial import distance

# Configuración de pandas para mostrar todas las columnas y ajustar el ancho de la salida
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Clasificador Euclidiano basado en el centroide
class ClasificadorEuclidiano:
    """
    Clasificador basado en la distancia al centroide. Calcula el centroide de cada clase y asigna la
    clase del centroide más cercano a cada instancia de prueba.
    """
    def entrenar(self, X_entrenamiento, y_entrenamiento):
        """
        Calcula el centroide para cada clase en el conjunto de entrenamiento.
        
        Parámetros:
        - X_entrenamiento: Matriz de características para entrenamiento.
        - y_entrenamiento: Vector de etiquetas de clase para entrenamiento.
        """
        self.centroides = {}
        clases = np.unique(y_entrenamiento)
        for clase in clases:
            # Calcula el centroide como el promedio de los puntos de cada clase
            self.centroides[clase] = X_entrenamiento[y_entrenamiento == clase].mean(axis=0)

    def predecir(self, X_prueba):
        """
        Predice las clases para las instancias de prueba basándose en la distancia al centroide más cercano.
        
        Parámetro:
        - X_prueba: Matriz de características para las instancias de prueba.
        
        Retorna:
        - Array con las etiquetas de clase predichas.
        """
        y_predicho = []
        for x in X_prueba:
            # Calcula la distancia al centroide de cada clase
            distancias = {clase: distance.euclidean(x, centroide) for clase, centroide in self.centroides.items()}
            # Encuentra la clase del centroide más cercano
            clase_min = min(distancias, key=distancias.get)
            y_predicho.append(clase_min)
        return np.array(y_predicho)

# Clasificador 1NN
class Clasificador1NN:
    """
    Clasificador 1-Nearest Neighbor (1NN). Similar al clasificador Euclidiano,
    asigna la clase del vecino más cercano basándose en la distancia Euclidiana.
    """
    def entrenar(self, X_entrenamiento, y_entrenamiento):
        """
        Guarda el conjunto de entrenamiento.
        
        Parámetros:
        - X_entrenamiento: Matriz de características para entrenamiento.
        - y_entrenamiento: Vector de etiquetas de clase para entrenamiento.
        """
        self.X_entrenamiento = X_entrenamiento
        self.y_entrenamiento = y_entrenamiento

    def predecir(self, X_prueba):
        """
        Predice las clases para las instancias de prueba usando el vecino más cercano.
        
        Parámetro:
        - X_prueba: Matriz de características para las instancias de prueba.
        
        Retorna:
        - Array con las etiquetas de clase predichas.
        """
        y_predicho = []
        for x in X_prueba:
            # Calcula la distancia Euclidiana a todas las instancias de entrenamiento
            distancias = [distance.euclidean(x, x_entreno) for x_entreno in self.X_entrenamiento]
            # Encuentra el índice de la instancia más cercana
            indice_min = np.argmin(distancias)
            # Asigna la clase de la instancia más cercana
            y_predicho.append(self.y_entrenamiento[indice_min])
        return np.array(y_predicho)

# Función para evaluar el modelo
def evaluar_modelo(modelo, X, y, tipo_validacion="holdout"):
    """
    Evalúa el rendimiento del modelo usando diferentes métodos de validación.
    
    Parámetros:
    - modelo: Clasificador a evaluar.
    - X: Matriz de características.
    - y: Vector de etiquetas de clase.
    - tipo_validacion: Método de validación ("holdout", "kfold" o "leaveoneout").
    
    Retorna:
    - Precisión media y matriz de confusión acumulada.
    """
    if tipo_validacion == "holdout":
        # Divide el conjunto en 70% entrenamiento y 30% prueba
        X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(X, y, test_size=0.3, random_state=42)
        modelo.entrenar(X_entrenamiento, y_entrenamiento)
        y_predicho = modelo.predecir(X_prueba)
        precision = accuracy_score(y_prueba, y_predicho)
        matriz_confusion = confusion_matrix(y_prueba, y_predicho)
        return precision, matriz_confusion

    elif tipo_validacion == "kfold":
        # 10-Fold Cross-Validation
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        precisiones = []
        matrices_confusion = []
        for indice_entrenamiento, indice_prueba in kf.split(X):
            X_entrenamiento, X_prueba = X[indice_entrenamiento], X[indice_prueba]
            y_entrenamiento, y_prueba = y[indice_entrenamiento], y[indice_prueba]
            modelo.entrenar(X_entrenamiento, y_entrenamiento)
            y_predicho = modelo.predecir(X_prueba)
            precisiones.append(accuracy_score(y_prueba, y_predicho))
            matrices_confusion.append(confusion_matrix(y_prueba, y_predicho))
        return np.mean(precisiones), sum(matrices_confusion)

    elif tipo_validacion == "leaveoneout":
        # Leave-One-Out Cross-Validation
        loo = LeaveOneOut()
        precisiones = []
        matrices_confusion = []
        for indice_entrenamiento, indice_prueba in loo.split(X):
            X_entrenamiento, X_prueba = X[indice_entrenamiento], X[indice_prueba]
            y_entrenamiento, y_prueba = y[indice_entrenamiento], y[indice_prueba]
            modelo.entrenar(X_entrenamiento, y_entrenamiento)
            y_predicho = modelo.predecir(X_prueba)
            precisiones.append(accuracy_score(y_prueba, y_predicho))
            matrices_confusion.append(confusion_matrix(y_prueba, y_predicho, labels=np.unique(y)))
        return np.mean(precisiones), sum(matrices_confusion)

# Función para mostrar la matriz de confusión con títulos
def mostrar_matriz_confusion(matriz, etiquetas_clases):
    """
    Convierte la matriz de confusión en un DataFrame con etiquetas de clase para filas y columnas.
    
    Parámetros:
    - matriz: Matriz de confusión (array).
    - etiquetas_clases: Lista de nombres de clase para las filas y columnas.
    
    Retorna:
    - DataFrame con la matriz de confusión etiquetada.
    """
    matriz_df = pd.DataFrame(matriz, index=[f"Real {etiqueta}" for etiqueta in etiquetas_clases],
                             columns=[f"Predicción {etiqueta}" for etiqueta in etiquetas_clases])
    return matriz_df

# Cargar datasets de sklearn
# Carga el conjunto de datos Iris y obtiene las etiquetas
iris = load_iris()
X_iris, y_iris = iris.data, iris.target
etiquetas_iris = iris.target_names

# Carga el conjunto de datos Wine y obtiene las etiquetas
wine = load_wine()
X_wine, y_wine = wine.data, wine.target
etiquetas_wine = wine.target_names

# Carga el conjunto de datos Digits y define las etiquetas del 0 al 9
digits = load_digits()
X_digits, y_digits = digits.data, digits.target
etiquetas_digits = [str(i) for i in range(10)]

# Probar el clasificador Euclidiano con diferentes métodos de validación
clasificador_euclidiano = ClasificadorEuclidiano()
print("Resultados del Clasificador Euclidiano")
for metodo in ["holdout", "kfold", "leaveoneout"]:
    for nombre, X, y, etiquetas in [("Iris", X_iris, y_iris, etiquetas_iris),
                                    ("Wine", X_wine, y_wine, etiquetas_wine),
                                    ("Digits", X_digits, y_digits, etiquetas_digits)]:
        precision, matriz_confusion = evaluar_modelo(clasificador_euclidiano, X, y, metodo)
        print(f"\nDataset: {nombre}")
        print(f"Método de Validación: {metodo}")
        print(f"Precisión: {precision:.4f}")
        print("Matriz de Confusión:")
        print(mostrar_matriz_confusion(matriz_confusion, etiquetas))

# Probar el clasificador 1NN con diferentes métodos de validación
clasificador_1nn = Clasificador1NN()
print("\nResultados del Clasificador 1NN")
for metodo in ["holdout", "kfold", "leaveoneout"]:
    for nombre, X, y, etiquetas in [("Iris", X_iris, y_iris, etiquetas_iris),
                                    ("Wine", X_wine, y_wine, etiquetas_wine),
                                    ("Digits", X_digits, y_digits, etiquetas_digits)]:
        precision, matriz_confusion = evaluar_modelo(clasificador_1nn, X, y, metodo)
        print(f"\nDataset: {nombre}")
        print(f"Método de Validación: {metodo}")
        print(f"Precisión: {precision:.4f}")
        print("Matriz de Confusión:")
        print(mostrar_matriz_confusion(matriz_confusion, etiquetas))
