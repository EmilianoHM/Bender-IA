import time
import heapq

# Función heurística para el algoritmo A* (distancia de Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_estrella(laberinto, inicio, final):
    filas, columnas = len(laberinto), len(laberinto[0])
    conjunto_abierto = []
    heapq.heappush(conjunto_abierto, (0 + heuristica(inicio, final), 0, inicio))
    proveniente_de = {}
    puntaje_g = {inicio: 0}
    
    while conjunto_abierto:
        _, costo_actual, actual = heapq.heappop(conjunto_abierto)
        
        if actual == final:
            # Reconstrucción del camino
            camino = []
            while actual in proveniente_de:
                camino.append(actual)
                actual = proveniente_de[actual]
            camino.append(inicio)
            return camino[::-1], costo_actual
        
        # Exploración de vecinos (arriba, abajo, izquierda, derecha)
        vecinos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dr, dc in vecinos:
            vecino = (actual[0] + dr, actual[1] + dc)
            
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas and laberinto[vecino[0]][vecino[1]] == 0:
                puntaje_g_tentativo = puntaje_g[actual] + 1
                
                if vecino not in puntaje_g or puntaje_g_tentativo < puntaje_g[vecino]:
                    puntaje_g[vecino] = puntaje_g_tentativo
                    puntaje_f = puntaje_g_tentativo + heuristica(vecino, final)
                    heapq.heappush(conjunto_abierto, (puntaje_f, puntaje_g_tentativo, vecino))
                    proveniente_de[vecino] = actual
                    
    return None, float('inf')  # Devuelve None si no se encuentra un camino

# Definición del laberinto proporcionado
laberinto = [
    [1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1]
]
inicio = (0, 1)  # Coordenadas de inicio (fila, columna)
final = (3, 4)   # Coordenadas de salida (fila, columna)

# Medición del tiempo de ejecución para el laberinto proporcionado
tiempo_inicio = time.perf_counter()
camino, costo = a_estrella(laberinto, inicio, final)
tiempo_ejecucion = time.perf_counter() - tiempo_inicio

print("Resultados para el laberinto proporcionado:")
print("Camino encontrado:", camino)
print("Costo del camino:", costo)
print(f"Tiempo de ejecución: {tiempo_ejecucion:.10f} segundos")

# Definición de un laberinto más complejo y de mayor tamaño
laberinto_complejo = [
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1]
]
inicio_complejo = (0, 1)  # Coordenadas de inicio (fila, columna)
final_complejo = (9, 8)   # Coordenadas de salida (fila, columna)

# Medición del tiempo de ejecución para el laberinto más complejo
tiempo_inicio_complejo = time.perf_counter()
camino_complejo, costo_complejo = a_estrella(laberinto_complejo, inicio_complejo, final_complejo)
tiempo_ejecucion_complejo = time.perf_counter() - tiempo_inicio_complejo

print("\nResultados para el laberinto más complejo:")
print("Camino encontrado:", camino_complejo)
print("Costo del camino:", costo_complejo)
print(f"Tiempo de ejecución: {tiempo_ejecucion_complejo:.10f} segundos")
