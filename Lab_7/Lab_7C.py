import socket
import pickle
import tkinter as tk
from tkinter import messagebox
import threading

# --- Configuración general ---
# Definición de los jugadores y casillas vacías
JUGADOR_X = "X"  # Jugador X
JUGADOR_O = "O"  # Jugador O
VACIO = ""       # Casilla vacía
TAMAÑO = 4       # Tamaño del tablero (4x4)

def recibir_datos(socket):
    """
    Recibe y deserializa datos a través del socket.
    :param socket: El socket desde el cual se reciben los datos.
    :return: Los datos deserializados.
    """
    datos_serializados = socket.recv(1024)  # Recibe datos del socket (máximo 1024 bytes)
    return pickle.loads(datos_serializados)  # Deserializa los datos usando pickle

def enviar_datos(socket, datos):
    """
    Serializa y envía datos a través del socket.
    :param socket: El socket a través del cual se envían los datos.
    :param datos: Los datos a enviar (pueden ser cualquier tipo de dato serializable).
    """
    datos_serializados = pickle.dumps(datos)  # Serializa los datos usando pickle
    socket.sendall(datos_serializados)  # Envía los datos serializados

# --- Interfaz gráfica con Tkinter ---
class ClienteGato4x4:
    """
    Clase que representa el cliente del juego de Gato (4x4) usando Tkinter para la interfaz gráfica.
    """
    def __init__(self, root, cliente, jugador):
        """
        Inicializa el cliente con la ventana Tkinter, el socket del cliente y el jugador asignado.
        :param root: La ventana principal de Tkinter.
        :param cliente: El socket de conexión con el servidor.
        :param jugador: El jugador asignado ("X" o "O").
        """
        self.root = root
        self.root.title(f"Gato 4x4 - Jugador {jugador}")
        self.cliente = cliente
        self.jugador = jugador
        self.turno_actual = JUGADOR_X  # El turno comienza con "X"
        self.mi_turno = False  # Controla si es el turno del jugador
        self.tablero = [[VACIO for _ in range(TAMAÑO)] for _ in range(TAMAÑO)]  # Inicializa el tablero vacío
        self.botones = [[None for _ in range(TAMAÑO)] for _ in range(TAMAÑO)]  # Botones de la interfaz
        self.crear_tablero()  # Crea la interfaz del tablero
        
        # Iniciar un hilo para manejar la recepción de datos sin bloquear la interfaz gráfica
        self.hilo_escucha = threading.Thread(target=self.recibir_actualizacion, daemon=True)
        self.hilo_escucha.start()

    def crear_tablero(self):
        """
        Crea la interfaz gráfica del tablero de Gato con botones para cada casilla.
        """
        frame = tk.Frame(self.root)
        frame.pack()  # Empaqueta el frame en la ventana principal
        for i in range(TAMAÑO):
            for j in range(TAMAÑO):
                # Cada botón representa una casilla en el tablero
                boton = tk.Button(frame, text="", width=5, height=2, font=('Helvetica', 24),
                                  command=lambda i=i, j=j: self.click_boton(i, j))
                boton.grid(row=i, column=j)
                self.botones[i][j] = boton

    def click_boton(self, i, j):
        """
        Maneja el evento de clic en un botón del tablero.
        :param i: Fila del botón clicado.
        :param j: Columna del botón clicado.
        """
        # Solo permite al jugador hacer clic si es su turno y la casilla está vacía
        if self.tablero[i][j] == VACIO and self.mi_turno:
            self.tablero[i][j] = self.jugador  # Actualiza el tablero con el símbolo del jugador
            self.botones[i][j]['text'] = self.jugador  # Actualiza el texto del botón
            enviar_datos(self.cliente, (i, j))  # Envía el movimiento al servidor
            self.mi_turno = False  # Desactiva el turno hasta la próxima actualización

    def recibir_actualizacion(self):
        """
        Hilo que recibe continuamente actualizaciones del estado del tablero y el turno desde el servidor.
        """
        while True:
            mensaje = recibir_datos(self.cliente)  # Recibe los datos del servidor
            if isinstance(mensaje, str):
                # Si el mensaje es una cadena, significa que es el resultado del juego
                if mensaje.startswith("¿Quieres jugar de nuevo?"):
                    self.preguntar_reiniciar()
                else:
                    messagebox.showinfo("Resultado", mensaje)
                    self.reiniciar_juego()  # Reinicia el tablero si termina el juego
            else:
                # El mensaje es el estado del tablero y el turno actual
                self.tablero, turno = mensaje
                self.mi_turno = (turno == self.jugador)  # Activa el turno si corresponde al jugador
                self.actualizar_tablero()  # Actualiza visualmente el tablero

    def actualizar_tablero(self):
        """
        Actualiza el tablero en la interfaz gráfica según el estado actual.
        """
        for i in range(TAMAÑO):
            for j in range(TAMAÑO):
                self.botones[i][j]['text'] = self.tablero[i][j]  # Actualiza el texto del botón según el tablero

    def reiniciar_juego(self):
        """
        Reinicia el estado del tablero y la interfaz para una nueva partida.
        """
        self.tablero = [[VACIO for _ in range(TAMAÑO)] for _ in range(TAMAÑO)]  # Resetea el tablero
        for i in range(TAMAÑO):
            for j in range(TAMAÑO):
                self.botones[i][j]['text'] = ""  # Limpia los botones

    def preguntar_reiniciar(self):
        """
        Pregunta al jugador si desea jugar nuevamente y envía su respuesta al servidor.
        """
        respuesta = messagebox.askyesno("Nuevo Juego", "¿Quieres jugar de nuevo?")  # Pregunta al jugador
        if respuesta:
            enviar_datos(self.cliente, 's')  # Si acepta, envía 's' al servidor
            self.reiniciar_juego()  # Reinicia el tablero
        else:
            enviar_datos(self.cliente, 'n')  # Si no acepta, envía 'n' al servidor y cierra la ventana
            self.root.quit()

# --- Ejecución del Cliente ---
if __name__ == "__main__":
    # Conectar al servidor en localhost:12345
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(('localhost', 12345))

    # Iniciar la interfaz Tkinter y el juego
    root = tk.Tk()
    jugador = recibir_datos(cliente)  # Recibe si el jugador es "X" o "O" desde el servidor
    juego = ClienteGato4x4(root, cliente, jugador)
    root.mainloop()  # Inicia el ciclo de eventos de Tkinter
    cliente.close()  # Cierra la conexión cuando termina el juego
