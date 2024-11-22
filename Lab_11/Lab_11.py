import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_wine, load_breast_cancer  # Datasets predefinidos en sklearn
from sklearn.model_selection import train_test_split, KFold, LeaveOneOut  # Métodos de validación
from sklearn.metrics import accuracy_score, confusion_matrix  # Métricas de desempeño
from sklearn.neural_network import MLPClassifier  # Perceptrón Multicapa
from sklearn.svm import SVC  # Clasificador basado en SVM con kernel RBF
from sklearn.preprocessing import StandardScaler  # Escalador para normalizar los datos
from sklearn.utils.multiclass import unique_labels  # Para obtener etiquetas únicas de un conjunto de datos

# Función para cargar los datasets
def cargar_datasets():
    """
    Carga y devuelve tres datasets predefinidos de sklearn:
    - Iris: Clasificación de flores (3 clases).
    - Wine: Clasificación de tipos de vino (3 clases).
    - Breast Cancer: Clasificación binaria de células tumorales (malignas/benignas).
    
    Cada entrada contiene:
    - Las características (X) y las etiquetas (y) del dataset.
    - Los nombres de las clases correspondientes.
    """
    datasets = {
        "Iris": (load_iris(return_X_y=True), load_iris().target_names),
        "Wine": (load_wine(return_X_y=True), load_wine().target_names),
        "Breast Cancer": (load_breast_cancer(return_X_y=True), load_breast_cancer().target_names),
    }
    return datasets

# Clasificador RBF (simulado usando SVM con kernel RBF)
def clasificador_rbf():
    """
    Devuelve un clasificador basado en SVM con kernel RBF.
    El kernel RBF permite manejar problemas no lineales.
    """
    return SVC(kernel='rbf', gamma='scale', probability=True)

# Función para imprimir la matriz de confusión con nombres y mostrarla completa
def imprimir_matriz_confusion(matriz_confusion, etiquetas):
    """
    Imprime la matriz de confusión con etiquetas legibles para cada clase.
    - matriz_confusion: La matriz de confusión a imprimir.
    - etiquetas: Los nombres de las clases para las filas y columnas.
    """
    # Ajustar opciones de pandas para evitar truncar la salida
    with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
        df_matriz = pd.DataFrame(
            matriz_confusion,
            index=[f"Verdadero {etiqueta}" for etiqueta in etiquetas],  # Nombres para las filas
            columns=[f"Predicho {etiqueta}" for etiqueta in etiquetas]  # Nombres para las columnas
        )
        print("\nMatriz de Confusión:")
        print(df_matriz)

# Función para realizar validaciones
def realizar_validaciones(X, y, modelo, metodo_validacion, etiquetas):
    """
    Aplica un método de validación sobre un clasificador y calcula su precisión y matriz de confusión.
    - X: Características del dataset.
    - y: Etiquetas del dataset.
    - modelo: Clasificador a validar.
    - metodo_validacion: Método de validación ("Hold-Out", "10-Fold", "Leave-One-Out").
    - etiquetas: Nombres de las clases en el dataset.
    """
    print(f"\nValidación: {metodo_validacion}")

    if metodo_validacion == "Hold-Out":
        # Dividir el dataset en 70% entrenamiento y 30% prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        modelo.fit(X_train, y_train)  # Entrenar el modelo con los datos de entrenamiento
        y_pred = modelo.predict(X_test)  # Hacer predicciones con los datos de prueba
        accuracy = accuracy_score(y_test, y_pred)  # Calcular la precisión
        # Calcular la matriz de confusión
        matriz_confusion = confusion_matrix(y_test, y_pred, labels=range(len(etiquetas))).astype(int)
        imprimir_matriz_confusion(matriz_confusion, etiquetas)  # Imprimir la matriz de confusión
        return accuracy

    elif metodo_validacion == "10-Fold":
        # Crear particiones en 10 partes para validación cruzada
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        accuracies = []  # Lista para almacenar las precisiones en cada iteración
        conf_matrices = np.zeros((len(etiquetas), len(etiquetas)), dtype=int)  # Matriz acumulada de confusión
        for train_idx, test_idx in kf.split(X):
            # Dividir los datos en conjuntos de entrenamiento y prueba
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            modelo.fit(X_train, y_train)  # Entrenar el modelo
            y_pred = modelo.predict(X_test)  # Predecir
            accuracies.append(accuracy_score(y_test, y_pred))  # Guardar la precisión
            conf_matrices += confusion_matrix(y_test, y_pred, labels=range(len(etiquetas))).astype(int)
        imprimir_matriz_confusion(conf_matrices, etiquetas)  # Imprimir la matriz acumulada
        return np.mean(accuracies)  # Promedio de las precisiones

    elif metodo_validacion == "Leave-One-Out":
        # Validación cruzada Leave-One-Out (entrena con todas las muestras menos una)
        loo = LeaveOneOut()
        accuracies = []  # Lista para almacenar las precisiones
        conf_matrices = np.zeros((len(etiquetas), len(etiquetas)), dtype=int)  # Matriz acumulada de confusión
        for train_idx, test_idx in loo.split(X):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            modelo.fit(X_train, y_train)  # Entrenar
            y_pred = modelo.predict(X_test)  # Predecir
            accuracies.append(accuracy_score(y_test, y_pred))  # Guardar precisión
            conf_matrices += confusion_matrix(y_test, y_pred, labels=range(len(etiquetas))).astype(int)
        imprimir_matriz_confusion(conf_matrices, etiquetas)  # Imprimir la matriz acumulada
        return np.mean(accuracies)  # Promedio de las precisiones

# Main
datasets = cargar_datasets()  # Cargar los datasets

for nombre_dataset, ((X, y), etiquetas) in datasets.items():
    print(f"\nDataset: {nombre_dataset}")
    # Escalar los datos para normalizar las características
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Modelos a probar
    modelos = {
        "Perceptrón Multicapa": MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42),
        "Red Neuronal RBF": clasificador_rbf()
    }

    for nombre_modelo, modelo in modelos.items():
        print(f"\nClasificador: {nombre_modelo}")
        for metodo in ["Hold-Out", "10-Fold", "Leave-One-Out"]:
            accuracy = realizar_validaciones(X, y, modelo, metodo, etiquetas)  # Realizar validación
            print(f"Accuracy: {accuracy:.4f}")  # Imprimir la precisión
