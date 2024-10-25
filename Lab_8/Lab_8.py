import pandas as pd  # Importamos la librería pandas, que nos permite trabajar con dataframes y manipular datos.

# Definimos los nombres de las columnas para el dataset Iris.
column_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'class']

# Leemos el archivo CSV 'bezdekIris.data' y almacenamos los datos en un dataframe llamado 'iris_df'.
# El archivo se lee con 'read_csv' y se le asignan nombres a las columnas usando el argumento 'names'.
iris_df = pd.read_csv('bezdekIris.data', names=column_names)

# Mostramos las primeras 5 filas del dataframe para verificar que los datos se han cargado correctamente.
print(iris_df.head())
