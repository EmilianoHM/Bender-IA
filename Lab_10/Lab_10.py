# Importación de librerías necesarias para el procesamiento y modelado de datos
from sklearn.datasets import load_iris, load_wine, load_digits
from sklearn.model_selection import train_test_split, cross_val_predict, LeaveOneOut
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd

# Configuración de pandas para mostrar todas las columnas y ajustar el ancho de la salida
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

# Función para mostrar la matriz de confusión con etiquetas de clase y la precisión
def mostrar_matriz_confusion(matriz, etiquetas_clase, metodo, clasificador, dataset, precision):
    """
    Muestra la matriz de confusión con etiquetas de clase y la precisión obtenida.

    Args:
        matriz (array): Matriz de confusión generada por el modelo.
        etiquetas_clase (list): Lista de nombres de las clases en el dataset.
        metodo (str): Nombre del método de validación utilizado (e.g., Hold-Out, Validación Cruzada).
        clasificador (str): Nombre del clasificador (e.g., Naive Bayes, KNN).
        dataset (str): Nombre del dataset en el que se realizó la evaluación.
        precision (float): Precisión obtenida por el modelo en la evaluación.
    """
    # Convertir la matriz de confusión a un DataFrame de pandas para etiquetar filas y columnas
    df_matriz = pd.DataFrame(matriz, index=etiquetas_clase, columns=etiquetas_clase)
    # Imprimir información relevante sobre la matriz de confusión y la precisión del modelo
    print(f'\nMatriz de Confusión - {clasificador} ({metodo}) en {dataset}')
    print(f'Precisión: {precision:.2f}')
    print(df_matriz)

# Función para cargar los datasets Iris, Wine y Digits
def cargar_datasets():
    """
    Carga los datasets Iris, Wine y Digits desde sklearn.

    Returns:
        dict: Un diccionario que contiene los datasets con sus nombres como claves.
    """
    iris = load_iris()
    wine = load_wine()
    digits = load_digits()
    return {"Iris": iris, "Wine": wine, "Digits": digits}

# Implementación del clasificador Naive Bayes
def clasificador_naive_bayes(datos_entrenamiento, etiquetas_entrenamiento):
    """
    Entrena un clasificador Naive Bayes en los datos de entrenamiento.

    Args:
        datos_entrenamiento (array): Matriz de características para el entrenamiento.
        etiquetas_entrenamiento (array): Etiquetas de clase correspondientes a los datos de entrenamiento.

    Returns:
        GaussianNB: Modelo de Naive Bayes entrenado.
    """
    modelo = GaussianNB()
    modelo.fit(datos_entrenamiento, etiquetas_entrenamiento)
    return modelo

# Implementación del clasificador K-Nearest Neighbors (KNN)
def clasificador_knn(datos_entrenamiento, etiquetas_entrenamiento, k=3):
    """
    Entrena un clasificador KNN con un valor de K especificado en los datos de entrenamiento.

    Args:
        datos_entrenamiento (array): Matriz de características para el entrenamiento.
        etiquetas_entrenamiento (array): Etiquetas de clase correspondientes a los datos de entrenamiento.
        k (int): Número de vecinos a considerar en el modelo KNN.

    Returns:
        KNeighborsClassifier: Modelo KNN entrenado.
    """
    modelo = KNeighborsClassifier(n_neighbors=k)
    modelo.fit(datos_entrenamiento, etiquetas_entrenamiento)
    return modelo

# Evaluación del modelo con Hold-Out (división 70% entrenamiento, 30% prueba)
def evaluacion_hold_out(modelo, datos, etiquetas, etiquetas_clase, clasificador, dataset):
    """
    Evalúa el modelo utilizando el método Hold-Out (70% entrenamiento, 30% prueba).

    Args:
        modelo: Clasificador entrenado que se va a evaluar.
        datos (array): Matriz de características del dataset completo.
        etiquetas (array): Etiquetas de clase correspondientes al dataset completo.
        etiquetas_clase (list): Lista de nombres de las clases en el dataset.
        clasificador (str): Nombre del clasificador.
        dataset (str): Nombre del dataset en el que se realiza la evaluación.
    """
    # División de los datos en entrenamiento y prueba
    datos_entrenamiento, datos_prueba, etiquetas_entrenamiento, etiquetas_prueba = train_test_split(
        datos, etiquetas, test_size=0.3, random_state=42)
    # Entrenamiento y predicción
    modelo.fit(datos_entrenamiento, etiquetas_entrenamiento)
    predicciones = modelo.predict(datos_prueba)
    # Cálculo de precisión y matriz de confusión
    precision = accuracy_score(etiquetas_prueba, predicciones)
    matriz_confusion = confusion_matrix(etiquetas_prueba, predicciones)
    # Mostrar resultados
    mostrar_matriz_confusion(matriz_confusion, etiquetas_clase, 'Hold-Out', clasificador, dataset, precision)

# Evaluación del modelo con Validación Cruzada de 10 particiones (10-Fold)
def evaluacion_validacion_cruzada(modelo, datos, etiquetas, etiquetas_clase, clasificador, dataset):
    """
    Evalúa el modelo utilizando validación cruzada de 10 particiones (10-Fold).

    Args:
        modelo: Clasificador entrenado que se va a evaluar.
        datos (array): Matriz de características del dataset completo.
        etiquetas (array): Etiquetas de clase correspondientes al dataset completo.
        etiquetas_clase (list): Lista de nombres de las clases en el dataset.
        clasificador (str): Nombre del clasificador.
        dataset (str): Nombre del dataset en el que se realiza la evaluación.
    """
    # Predicción utilizando validación cruzada de 10 particiones
    predicciones = cross_val_predict(modelo, datos, etiquetas, cv=10)
    # Cálculo de precisión y matriz de confusión
    precision = accuracy_score(etiquetas, predicciones)
    matriz_confusion = confusion_matrix(etiquetas, predicciones)
    # Mostrar resultados
    mostrar_matriz_confusion(matriz_confusion, etiquetas_clase, 'Validación Cruzada', clasificador, dataset, precision)

# Evaluación del modelo con Leave-One-Out
def evaluacion_leave_one_out(modelo, datos, etiquetas, etiquetas_clase, clasificador, dataset):
    """
    Evalúa el modelo utilizando el método Leave-One-Out.

    Args:
        modelo: Clasificador entrenado que se va a evaluar.
        datos (array): Matriz de características del dataset completo.
        etiquetas (array): Etiquetas de clase correspondientes al dataset completo.
        etiquetas_clase (list): Lista de nombres de las clases en el dataset.
        clasificador (str): Nombre del clasificador.
        dataset (str): Nombre del dataset en el que se realiza la evaluación.
    """
    # Configuración del método Leave-One-Out
    loo = LeaveOneOut()
    predicciones = []
    etiquetas_reales = []

    # Iteración para cada muestra en el dataset (entrenamiento y prueba uno a uno)
    for tren_index, prueba_index in loo.split(datos):
        datos_entrenamiento, datos_prueba = datos[tren_index], datos[prueba_index]
        etiquetas_entrenamiento, etiquetas_prueba = etiquetas[tren_index], etiquetas[prueba_index]
        # Entrenamiento y predicción para cada instancia
        modelo.fit(datos_entrenamiento, etiquetas_entrenamiento)
        prediccion = modelo.predict(datos_prueba)
        predicciones.append(prediccion[0])
        etiquetas_reales.append(etiquetas_prueba[0])

    # Cálculo de precisión y matriz de confusión
    precision = accuracy_score(etiquetas_reales, predicciones)
    matriz_confusion = confusion_matrix(etiquetas_reales, predicciones)
    # Mostrar resultados
    mostrar_matriz_confusion(matriz_confusion, etiquetas_clase, 'Leave-One-Out', clasificador, dataset, precision)

# Función principal para ejecutar los experimentos de clasificación
def ejecutar_experimentos():
    """
    Ejecuta experimentos de clasificación utilizando Naive Bayes y KNN en tres datasets,
    evaluando el rendimiento con diferentes métodos de validación.
    """
    # Cargar los datasets
    datasets = cargar_datasets()
    # Definir los valores de K para el clasificador KNN
    valores_k = [3, 5, 7]

    # Iterar sobre cada dataset
    for nombre_dataset, dataset in datasets.items():
        datos, etiquetas = dataset.data, dataset.target
        etiquetas_clase = dataset.target_names

        print(f"\nResultados para el dataset: {nombre_dataset}")

        # Clasificador Naive Bayes
        modelo_naive_bayes = clasificador_naive_bayes(datos, etiquetas)
        print("\nClasificador: Naive Bayes")
        
        # Evaluación del clasificador Naive Bayes con cada método de validación
        evaluacion_hold_out(modelo_naive_bayes, datos, etiquetas, etiquetas_clase, 'Naive Bayes', nombre_dataset)
        evaluacion_validacion_cruzada(modelo_naive_bayes, datos, etiquetas, etiquetas_clase, 'Naive Bayes', nombre_dataset)
        evaluacion_leave_one_out(modelo_naive_bayes, datos, etiquetas, etiquetas_clase, 'Naive Bayes', nombre_dataset)

        # Clasificador KNN
        for k in valores_k:
            modelo_knn = clasificador_knn(datos, etiquetas, k=k)
            print(f"\nClasificador: KNN con K={k}")
            
            # Evaluación del clasificador KNN con cada método de validación
            evaluacion_hold_out(modelo_knn, datos, etiquetas, etiquetas_clase, f'KNN (K={k})', nombre_dataset)
            evaluacion_validacion_cruzada(modelo_knn, datos, etiquetas, etiquetas_clase, f'KNN (K={k})', nombre_dataset)
            evaluacion_leave_one_out(modelo_knn, datos, etiquetas, etiquetas_clase, f'KNN (K={k})', nombre_dataset)

# Ejecución de los experimentos
ejecutar_experimentos()
