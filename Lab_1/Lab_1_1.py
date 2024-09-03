import numpy as np

# Definimos la función objetivo
def funcion_objetivo(x, y):
    return (1.5 - x + x * y)**2 + (2.25 - x + x * y**2)**2 + (2.625 - x + x * y**3)**2

# Parámetros de la búsqueda aleatoria
iteraciones = 10000
rango_min = -4.5
rango_max = 4.5

# Inicialización
mejor_valor = float('inf')
mejores_variables = None

# Búsqueda aleatoria
for i in range(iteraciones):
    # Generar valores aleatorios para x y y
    x = np.random.uniform(rango_min, rango_max)
    y = np.random.uniform(rango_min, rango_max)
    valor = funcion_objetivo(x, y)
    
    # Actualizar si encontramos un valor mejor
    if valor < mejor_valor:
        mejor_valor = valor
        mejores_variables = (x, y)

print(f"Mejor valor encontrado: {mejor_valor}")
print(f"Valores de x y y: {mejores_variables}")
