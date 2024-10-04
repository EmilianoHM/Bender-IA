import numpy as np

# Definir la función de Himmelblau
def funcion_himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

# Método 1: Usar una librería (scipy)
def metodo_libreria():
    from scipy.optimize import minimize
    # Definir la función para optimizar
    def himmelblau_opt(xy):
        x, y = xy
        return funcion_himmelblau(x, y)
    
    # Establecer el valor inicial y los límites
    valor_inicial = np.array([0, 0])
    limites = [(-5, 5), (-5, 5)]
    
    # Ejecutar el algoritmo de minimización
    resultado = minimize(himmelblau_opt, valor_inicial, bounds=limites)
    
    # Mostrar resultados
    print(f"\nMétodo con librería:")
    print(f"El mínimo está en x = {resultado.x[0]}, y = {resultado.x[1]}, con un valor de {resultado.fun}\n")


# Método 2: Fuerza Bruta
def metodo_fuerza_bruta():
    # Definir los rangos de búsqueda y los pasos
    rango_x = np.linspace(-5, 5, 1000)
    rango_y = np.linspace(-5, 5, 1000)

    # Variables para almacenar el valor mínimo
    valor_minimo = float('inf')
    minimo_x, minimo_y = 0, 0

    # Búsqueda exhaustiva en el espacio definido
    for x in rango_x:
        for y in rango_y:
            valor_actual = funcion_himmelblau(x, y)
            if valor_actual < valor_minimo:
                valor_minimo = valor_actual
                minimo_x = x
                minimo_y = y

    # Mostrar resultados
    print(f"\nMétodo de fuerza bruta:")
    print(f"El mínimo está en x = {minimo_x}, y = {minimo_y}, con un valor de {valor_minimo}\n")


# Método 3: Descenso por gradiente
def metodo_gradiente():
    # Definir el gradiente (derivadas parciales de la función)
    def gradiente_himmelblau(x, y):
        df_dx = 4 * (x**2 + y - 11) * x + 2 * (x + y**2 - 7)
        df_dy = 2 * (x**2 + y - 11) + 4 * (x + y**2 - 7) * y
        return np.array([df_dx, df_dy])

    # Parámetros iniciales
    x_actual, y_actual = 0, 0   # Punto de inicio
    tasa_aprendizaje = 0.001    # Tamaño del paso
    tolerancia = 1e-16          # Criterio de convergencia
    max_iteraciones = 1500      # Máximo número de iteraciones

    # Algoritmo de descenso por gradiente
    for i in range(max_iteraciones):
        gradiente = gradiente_himmelblau(x_actual, y_actual)
        nuevo_x = x_actual - tasa_aprendizaje * gradiente[0]
        nuevo_y = y_actual - tasa_aprendizaje * gradiente[1]
        
        # Verificar convergencia
        if np.linalg.norm([nuevo_x - x_actual, nuevo_y - y_actual]) < tolerancia:
            print(f"\nConvergencia alcanzada en iteración {i}")
            break
        
        x_actual, y_actual = nuevo_x, nuevo_y

    # Mostrar resultados
    valor_minimo = funcion_himmelblau(x_actual, y_actual)
    print(f"Método de descenso por gradiente:")
    print(f"El mínimo está en x = {x_actual}, y = {y_actual}, con un valor de {valor_minimo}\n")


# Menú para seleccionar el método
def menu():
    while True:  # Bucle para repetir el menú hasta que el usuario elija salir
        print("\nSelecciona el método para encontrar el mínimo de la función de Himmelblau:")
        print("1. Usar librería (scipy)")
        print("2. Fuerza bruta")
        print("3. Descenso por gradiente")
        print("4. Salir")
        eleccion = input("Introduce el número del método que deseas usar: ")

        if eleccion == '1':
            metodo_libreria()
        elif eleccion == '2':
            metodo_fuerza_bruta()
        elif eleccion == '3':
            metodo_gradiente()
        elif eleccion == '4':
            print("\nSaliendo del programa. ¡Hasta luego!")
            break  # Salir del bucle y finalizar el programa
        else:
            print("Opción no válida. Por favor, selecciona 1, 2, 3 o 4.")

# Ejecutar el menú
menu()
