### Parte 1. Biblioteca. ###

# Clase para la Pila (Stack)
class Pila:
    def __init__(self):
        self.elementos = []
    
    # Push
    def apilar(self, objeto):
        self.elementos.append(objeto)
    
    # Pop
    def desapilar(self):
        if not self.esta_vacia():
            return self.elementos.pop()
        else:
            return None
    
    # Otras
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

# Clase para la Lista
class Lista:
    def __init__(self):
        self.elementos = []
    
    def insertar(self, objeto):
        self.elementos.append(objeto)
    
    def buscar(self, objeto):
        return objeto in self.elementos
    

### Parte 2a. 4-puzzle. ###

def bfs_4_puzzle(start, objetivo):
    # Usamos la Cola implementada
    cola = Cola()
    cola.insertar((start, []))  # (estado actual, lista de movimientos)
    
    # Usamos la Lista genérica para los visitados
    visitados = Lista()
    visitados.insertar(start)
    
    while not cola.esta_vacia():
        estado_actual, movimientos = cola.quitar()
        
        # Si hemos alcanzado el objetivo
        if estado_actual == objetivo:
            return movimientos
        
        # Generar todos los posibles estados adyacentes (intercambiar elementos adyacentes)
        for i in range(len(estado_actual) - 1):
            nuevo_estado = estado_actual[:]
            # Intercambiar elementos adyacentes
            nuevo_estado[i], nuevo_estado[i + 1] = nuevo_estado[i + 1], nuevo_estado[i]
            
            if not visitados.buscar(nuevo_estado):
                visitados.insertar(nuevo_estado)
                cola.insertar((nuevo_estado, movimientos + [nuevo_estado]))  # Agregar el nuevo estado y el camino
    
    return None  # Si no hay solución

# Estado inicial del 4-puzzle
estado_inicial = [4, 3, 2, 1]
estado_objetivo = [1, 2, 3, 4]

camino = bfs_4_puzzle(estado_inicial, estado_objetivo)

print("\n4-puzzle:")

if camino:
    print("Se encontró una solución:")
    print(estado_inicial)
    for paso in camino:
        print(paso)
else:
    print("No se encontró una solución.")


### Parte 2b. Laberinto. ###

def bfs_laberinto(maze, start, end):
    filas = len(maze)
    columnas = len(maze[0])
    
    # Movimientos posibles: arriba, abajo, izquierda, derecha
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Usamos la Cola implementada
    cola = Cola()
    cola.insertar((start, [start]))  # (posición actual, camino recorrido)
    
    # Usamos la Lista genérica para los visitados
    visitados = Lista()
    visitados.insertar(start)
    
    while not cola.esta_vacia():
        (posicion_actual, camino) = cola.quitar()
        fila, columna = posicion_actual
        
        # Si llegamos al final
        if posicion_actual == end:
            return camino
        
        # Explorar los vecinos
        for movimiento in movimientos:
            nueva_fila, nueva_columna = fila + movimiento[0], columna + movimiento[1]
            
            if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas and maze[nueva_fila][nueva_columna] == 0:
                nueva_posicion = (nueva_fila, nueva_columna)
                if not visitados.buscar(nueva_posicion):
                    visitados.insertar(nueva_posicion)
                    cola.insertar((nueva_posicion, camino + [nueva_posicion]))
    
    return None  # No se encontró un camino

# Laberinto de ejemplo
maze = [
    [1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]

start = (0, 1)
end = (3, 4)

camino = bfs_laberinto(maze, start, end)

print("\n\nLaberinto:")

if camino:
    print("Camino encontrado:\n", camino, "\n")
else:
    print("No se encontró un camino.\n")
