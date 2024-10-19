import socket
import pickle

# --- Configuración general ---
# Definición de los jugadores y casillas vacías
JUGADOR_X = "X"  # Jugador X
JUGADOR_O = "O"  # Jugador O
VACIO = ""       # Casilla vacía
TAMAÑO = 4       # Tamaño del tablero (4x4)

def inicializar_tablero():
    """
    Inicializa el tablero como una matriz de 4x4 llena de casillas vacías.
    :return: Una lista 2D representando el tablero vacío.
    """
    return [[VACIO for _ in range(TAMAÑO)] for _ in range(TAMAÑO)]

def tablero_lleno(tablero):
    """
    Verifica si el tablero está completamente lleno.
    :param tablero: El tablero actual.
    :return: True si el tablero está lleno, False en caso contrario.
    """
    return all(tablero[i][j] != VACIO for i in range(TAMAÑO) for j in range(TAMAÑO))

def verificar_ganador(tablero, jugador):
    """
    Verifica si un jugador ha ganado al conseguir una línea de 4 en el tablero.
    :param tablero: El tablero actual.
    :param jugador: El jugador actual ("X" o "O").
    :return: True si el jugador ha ganado, False en caso contrario.
    """
    # Verifica filas, columnas y diagonales
    for i in range(TAMAÑO):
        # Filas y columnas
        if all([tablero[i][j] == jugador for j in range(TAMAÑO)]) or \
           all([tablero[j][i] == jugador for j in range(TAMAÑO)]):
            return True
    # Diagonales
    if all([tablero[i][i] == jugador for i in range(TAMAÑO)]) or \
       all([tablero[i][TAMAÑO - 1 - i] == jugador for i in range(TAMAÑO)]):
        return True
    return False

def enviar_datos(socket, datos):
    """
    Serializa y envía datos a través del socket.
    :param socket: El socket a través del cual se envían los datos.
    :param datos: Los datos a enviar (pueden ser cualquier tipo de dato serializable).
    """
    datos_serializados = pickle.dumps(datos)  # Serializa los datos usando pickle
    socket.sendall(datos_serializados)  # Envía los datos serializados

def recibir_datos(socket):
    """
    Recibe y deserializa datos a través del socket.
    :param socket: El socket desde el cual se reciben los datos.
    :return: Los datos deserializados.
    """
    datos_serializados = socket.recv(1024)  # Recibe datos del socket (máximo 1024 bytes)
    return pickle.loads(datos_serializados)  # Deserializa los datos usando pickle

def juego_servidor():
    """
    Función principal del servidor que maneja la conexión, el flujo del juego y
    la reinicialización de partidas según la elección de los jugadores.
    """
    # Configuración del servidor: creación de socket y escucha en localhost en el puerto 12345
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 12345))
    servidor.listen(2)  # Escucha hasta 2 conexiones (jugadores)

    print("Esperando a los jugadores...")
    conexion_jugador1, _ = servidor.accept()  # Conecta al primer jugador
    print("Jugador 1 (X) conectado.")
    conexion_jugador2, _ = servidor.accept()  # Conecta al segundo jugador
    print("Jugador 2 (O) conectado.")

    while True:
        # Inicializar el tablero para una nueva partida
        tablero = inicializar_tablero()
        turno = JUGADOR_X  # Comienza el jugador "X"

        # Enviar información inicial a ambos jugadores (quién es X y quién es O)
        enviar_datos(conexion_jugador1, JUGADOR_X)
        enviar_datos(conexion_jugador2, JUGADOR_O)

        juego_activo = True  # Controla si la partida está activa

        # Bucle principal del juego
        while juego_activo:
            # Enviar el tablero actual y el turno a ambos jugadores
            enviar_datos(conexion_jugador1, (tablero, turno))
            enviar_datos(conexion_jugador2, (tablero, turno))

            # Recibe el movimiento del jugador en turno
            if turno == JUGADOR_X:
                print("Esperando movimiento del Jugador X...")
                movimiento = recibir_datos(conexion_jugador1)
            else:
                print("Esperando movimiento del Jugador O...")
                movimiento = recibir_datos(conexion_jugador2)

            # Actualizar el tablero con el movimiento recibido
            fila, col = movimiento
            tablero[fila][col] = turno

            # Verificar si el jugador actual ha ganado
            if verificar_ganador(tablero, turno):
                enviar_datos(conexion_jugador1, f"{turno} ha ganado!")
                enviar_datos(conexion_jugador2, f"{turno} ha ganado!")
                juego_activo = False  # Termina el juego si hay un ganador
                break

            # Verificar si el tablero está lleno (empate)
            if tablero_lleno(tablero):
                enviar_datos(conexion_jugador1, "Empate")
                enviar_datos(conexion_jugador2, "Empate")
                juego_activo = False  # Termina el juego si hay empate
                break

            # Cambiar turno: alterna entre jugador X y O
            turno = JUGADOR_O if turno == JUGADOR_X else JUGADOR_X

        # Preguntar si los jugadores desean jugar nuevamente
        enviar_datos(conexion_jugador1, "¿Quieres jugar de nuevo? (s/n)")
        enviar_datos(conexion_jugador2, "¿Quieres jugar de nuevo? (s/n)")
        respuesta_jugador1 = recibir_datos(conexion_jugador1)  # Respuesta de Jugador 1
        respuesta_jugador2 = recibir_datos(conexion_jugador2)  # Respuesta de Jugador 2

        # Si alguno de los jugadores dice que no, finalizar el juego
        if respuesta_jugador1.lower() != 's' or respuesta_jugador2.lower() != 's':
            enviar_datos(conexion_jugador1, "Gracias por jugar!")
            enviar_datos(conexion_jugador2, "Gracias por jugar!")
            break

    # Cierra el servidor cuando el ciclo termina
    servidor.close()

# Iniciar el servidor
if __name__ == "__main__":
    juego_servidor()
