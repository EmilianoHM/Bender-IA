### Parte 1. Biblioteca. ###

# Clase para la Pila (Stack)
class Pila:
    def __init__(self):
        self.elementos = []
    
    def apilar(self, objeto):
        self.elementos.append(objeto)
    
    def desapilar(self):
        if not self.esta_vacia():
            return self.elementos.pop()
        else:
            return None
    
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    def cima(self):
        if not self.esta_vacia():
            return self.elementos[-1]
        else:
            return None

# Clase para la Cola (Queue)
class Cola:
    def __init__(self):
        self.elementos = []
    
    def insertar(self, objeto):
        self.elementos.append(objeto)
    
    def quitar(self):
        if not self.esta_vacia():
            return self.elementos.pop(0)
        else:
            return None
    
    def esta_vacia(self):
        return len(self.elementos) == 0
    
    def recorrer(self):
        for elemento in self.elementos:
            print(elemento)
    
    def buscar(self, objeto):
        return objeto in self.elementos

# Clase para la Lista Genérica
class Lista:
    def __init__(self):
        self.elementos = []
    
    def insertar(self, objeto):
        self.elementos.append(objeto)
    
    def buscar(self, objeto):
        return objeto in self.elementos


### Parte 2a. 4-puzzle. ###

# Función que genera nuevos estados intercambiando pares de elementos adyacentes
def generar_nuevos_estados(estado_actual):
    nuevos_estados = []
    for i in range(len(estado_actual) - 1):
        # Intercambiar elementos adyacentes
        nuevo_estado = estado_actual[:]
        nuevo_estado[i], nuevo_estado[i + 1] = nuevo_estado[i + 1], nuevo_estado[i]
        nuevos_estados.append(nuevo_estado)
    return nuevos_estados

# Implementación de DFS para el 4-puzzle en una línea utilizando la clase Lista
def dfs_4puzzle_linea(estado_inicial, estado_objetivo):
    pila = Pila()  # Usamos la pila implementada anteriormente
    pila.apilar([estado_inicial])
    visitado = Lista()  # Usamos la clase Lista para almacenar los visitados

    while not pila.esta_vacia():
        camino = pila.desapilar()
        estado_actual = camino[-1]

        # Verificamos si hemos llegado al estado objetivo
        if estado_actual == estado_objetivo:
            return camino

        estado_tupla = tuple(estado_actual)  # Convertimos el estado en tupla para buscarla en la lista de visitados

        if not visitado.buscar(estado_tupla):  # Usamos la función buscar de la clase Lista
            visitado.insertar(estado_tupla)  # Insertamos el estado actual en la lista de visitados

            # Generamos los nuevos estados y los agregamos a la pila
            for nuevo_estado in generar_nuevos_estados(estado_actual):
                nuevo_camino = camino[:]
                nuevo_camino.append(nuevo_estado)
                pila.apilar(nuevo_camino)

    return None  # Si no hay solución

# Estado inicial y objetivo del 4-puzzle en una línea
estado_inicial = [4, 2, 1, 3]
estado_objetivo = [1, 2, 3, 4]

# Resolvemos el 4-puzzle en una línea
solucion = dfs_4puzzle_linea(estado_inicial, estado_objetivo)

print("\n4-puzzle:")

if solucion:
    print("\nSolución encontrada:")
    for paso in solucion:
        print(paso)
else:
    print("\nNo se encontró solución.")


### Parte 2b. Laberinto. ###

# Movimientos posibles: Arriba, Abajo, Izquierda, Derecha
movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Representados como (fila, columna)

# Función para verificar si una posición está dentro de los límites del laberinto
def es_posicion_valida(laberinto, posicion):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    fila, columna = posicion
    return 0 <= fila < filas and 0 <= columna < columnas and laberinto[fila][columna] == 0

# Función para generar nuevos estados a partir de la posición actual
def generar_nuevos_estados(laberinto, posicion_actual):
    nuevos_estados = []
    fila_actual, columna_actual = posicion_actual

    for movimiento in movimientos:
        nueva_fila = fila_actual + movimiento[0]
        nueva_columna = columna_actual + movimiento[1]
        nueva_posicion = (nueva_fila, nueva_columna)
        
        if es_posicion_valida(laberinto, nueva_posicion):
            nuevos_estados.append(nueva_posicion)
    
    return nuevos_estados

# Implementación de DFS para resolver el laberinto utilizando la clase Lista
def dfs_laberinto(laberinto, inicio, objetivo):
    pila = Pila()  # Usamos la pila implementada anteriormente
    pila.apilar([inicio])
    visitado = Lista()  # Usamos la clase Lista para almacenar los visitados

    while not pila.esta_vacia():
        camino = pila.desapilar()
        posicion_actual = camino[-1]

        # Verificamos si hemos llegado al objetivo
        if posicion_actual == objetivo:
            return camino

        # Verificamos si ya hemos visitado la posición actual
        if not visitado.buscar(posicion_actual):  # Usamos la función buscar de la clase Lista
            visitado.insertar(posicion_actual)  # Insertamos la posición actual en la lista de visitados

            # Generamos los nuevos estados y los agregamos a la pila
            for nueva_posicion in generar_nuevos_estados(laberinto, posicion_actual):
                nuevo_camino = list(camino)
                nuevo_camino.append(nueva_posicion)
                pila.apilar(nuevo_camino)

    return None  # Si no hay solución

# Representación del laberinto
laberinto = [
    [1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]

# Posición de inicio y salida
inicio = (0, 1)
objetivo = (3, 4)

# Resolvemos el laberinto con DFS
solucion = dfs_laberinto(laberinto, inicio, objetivo)

print("\n\nLaberinto:")

if solucion:
    print("\nSolución encontrada:")
    for paso in solucion:
        print(paso)
else:
    print("\nNo se encontró solución.")
