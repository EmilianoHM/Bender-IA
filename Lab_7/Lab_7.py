import tkinter as tk
import math

# Constantes del juego
JUGADOR = 'X'  # Símbolo del jugador humano
IA = 'O'       # Símbolo de la IA (Inteligencia Artificial)
VACIO = '.'    # Símbolo que representa una casilla vacía en el tablero

# Profundidad máxima permitida para el algoritmo Minimax
PROFUNDIDAD_MAX = 4  # Se ha reducido para acelerar el tiempo de respuesta

# ------------------- Clase Principal del Juego ------------------- #

class JuegoGato4x4:
    """Clase principal que implementa la interfaz gráfica y la lógica del juego del gato 4x4."""

    def __init__(self, root):
        """Inicializa el tablero, los botones, el modo de juego y la interfaz gráfica."""
        self.root = root
        self.root.title("Gato 4x4")

        # Crear el tablero 4x4 vacío
        self.tablero = crear_tablero()  # Inicializa el tablero con posiciones vacías
        self.botones = [[None for _ in range(4)] for _ in range(4)]  # Matriz para los botones
        self.turno_humano = True  # El jugador humano comienza el juego

        # Crear la cuadrícula de botones que representan el tablero en la GUI
        self.crear_cuadricula()

        # Etiqueta para mostrar mensajes sobre el estado del juego (quién tiene el turno o si alguien ganó)
        self.mensaje = tk.Label(self.root, text="Turno del Jugador X", font=("Helvetica", 16))
        self.mensaje.grid(row=4, column=0, columnspan=4)

        # Variable que indica el modo de juego actual
        self.modo_juego = "Humano vs Humano"  # Modo de juego predeterminado

        # Crear el menú para seleccionar los modos de juego
        self.crear_menu()

    def crear_cuadricula(self):
        """Crea una cuadrícula de botones que representan el tablero en la interfaz gráfica."""
        for i in range(4):
            for j in range(4):
                # Cada botón representa una celda en el tablero y se coloca en la cuadrícula
                boton = tk.Button(self.root, text="", font=("Helvetica", 20), width=5, height=2,
                                  command=lambda i=i, j=j: self.click_boton(i, j))  # Al hacer clic, llama a click_boton
                boton.grid(row=i, column=j)
                self.botones[i][j] = boton  # Guarda el botón en la matriz

    def click_boton(self, i, j):
        """
        Maneja el evento de click en los botones del tablero. El jugador humano marca una casilla
        y luego se alterna el turno entre los jugadores X y O o la IA si es necesario.
        """
        if self.tablero[i][j] == VACIO:  # Solo se permite marcar casillas vacías
            if self.modo_juego == "Humano vs Humano":
                # Alterna entre los dos jugadores en el modo "Humano vs Humano"
                if self.turno_humano:  # Si es el turno del jugador humano X
                    self.tablero[i][j] = JUGADOR  # Marca la casilla con 'X'
                    self.botones[i][j].config(text=JUGADOR)  # Actualiza la visualización
                    self.turno_humano = False  # Cambia el turno a O
                    self.mensaje.config(text="Turno del Jugador O")  # Actualiza el mensaje
                else:  # Si es el turno del jugador O
                    self.tablero[i][j] = IA  # Marca la casilla con 'O'
                    self.botones[i][j].config(text=IA)  # Actualiza la visualización
                    self.turno_humano = True  # Cambia el turno a X
                    self.mensaje.config(text="Turno del Jugador X")
            elif self.modo_juego == "Humano vs IA":
                # El humano juega como X y la IA como O
                if self.turno_humano:  # Turno del humano
                    self.tablero[i][j] = JUGADOR
                    self.botones[i][j].config(text=JUGADOR)
                    self.turno_humano = False
                    self.mensaje.config(text="Turno de la IA")
                    self.root.after(500, self.turno_ia)  # Retraso de 0.5s para simular respuesta de la IA

        # Después del movimiento, verifica si hay un ganador o empate
        if hay_ganador(self.tablero, JUGADOR):
            self.mensaje.config(text="¡Jugador X ha ganado!")
            self.deshabilitar_botones()  # Bloquea el tablero
        elif hay_ganador(self.tablero, IA):
            self.mensaje.config(text="¡Jugador O ha ganado!" if self.modo_juego == "Humano vs Humano" else "¡La IA ha ganado!")
            self.deshabilitar_botones()
        elif es_tablero_lleno(self.tablero):
            self.mensaje.config(text="¡Es un empate!")
            self.deshabilitar_botones()

    def turno_ia(self):
        """
        Realiza el turno de la IA utilizando el algoritmo Minimax con poda Alfa-Beta.
        La IA selecciona el mejor movimiento disponible.
        """
        if self.modo_juego == "Humano vs IA" and not self.turno_humano:
            fila, columna = mejor_movimiento(self.tablero, PROFUNDIDAD_MAX)  # IA elige su movimiento
            self.tablero[fila][columna] = IA
            self.botones[fila][columna].config(text=IA)
            self.turno_humano = True  # Después del turno, vuelve a ser turno del humano
            self.mensaje.config(text="Turno del Jugador")

        # Después del movimiento, verifica si hay un ganador o empate
        if hay_ganador(self.tablero, IA):
            self.mensaje.config(text="¡La IA ha ganado!")
            self.deshabilitar_botones()
        elif es_tablero_lleno(self.tablero):
            self.mensaje.config(text="¡Es un empate!")
            self.deshabilitar_botones()

    def deshabilitar_botones(self):
        """Deshabilita todos los botones del tablero al finalizar el juego."""
        for fila in self.botones:
            for boton in fila:
                boton.config(state=tk.DISABLED)  # Deshabilita cada botón

    def reiniciar_juego(self):
        """Reinicia el tablero y habilita los botones para empezar un nuevo juego."""
        self.tablero = crear_tablero()  # Resetea el tablero
        for i in range(4):
            for j in range(4):
                self.botones[i][j].config(text="", state=tk.NORMAL)  # Resetea cada botón
        self.mensaje.config(text="Turno del Jugador X")  # El jugador X empieza de nuevo
        self.turno_humano = True

    def crear_menu(self):
        """Crea un menú que permite al usuario seleccionar el modo de juego y reiniciar el juego."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        opciones_menu = tk.Menu(menubar, tearoff=0)  # Menú desplegable
        menubar.add_cascade(label="Opciones", menu=opciones_menu)

        # Modos de juego
        opciones_menu.add_command(label="Humano vs Humano", command=self.modo_humano_vs_humano)
        opciones_menu.add_command(label="Humano vs IA", command=self.modo_humano_vs_ia)
        opciones_menu.add_command(label="IA vs IA", command=self.modo_ia_vs_ia)
        opciones_menu.add_separator()
        # Opciones para reiniciar el juego o salir
        opciones_menu.add_command(label="Reiniciar Juego", command=self.reiniciar_juego)
        opciones_menu.add_command(label="Salir", command=self.root.quit)

    def modo_humano_vs_humano(self):
        """Configura el modo de juego Humano vs Humano."""
        self.modo_juego = "Humano vs Humano"
        self.reiniciar_juego()

    def modo_humano_vs_ia(self):
        """Configura el modo de juego Humano vs IA."""
        self.modo_juego = "Humano vs IA"
        self.reiniciar_juego()

    def modo_ia_vs_ia(self):
        """Configura el modo de juego IA vs IA."""
        self.modo_juego = "IA vs IA"
        self.reiniciar_juego()
        self.mensaje.config(text="Turno de la IA X")
        self.root.after(500, self.turno_ia_vs_ia)  # Inicia el juego entre dos IAs

    def turno_ia_vs_ia(self):
        """Realiza los turnos alternativos entre dos IAs jugando entre sí."""
        if not hay_ganador(self.tablero, JUGADOR) and not hay_ganador(self.tablero, IA) and not es_tablero_lleno(self.tablero):
            fila, columna = mejor_movimiento(self.tablero, PROFUNDIDAD_MAX)
            jugador_actual = JUGADOR if self.turno_humano else IA  # Alterna el turno entre las dos IAs
            self.tablero[fila][columna] = jugador_actual
            self.botones[fila][columna].config(text=jugador_actual)
            self.turno_humano = not self.turno_humano

            # Verificar el estado del juego después del turno de la IA
            if hay_ganador(self.tablero, jugador_actual):
                self.mensaje.config(text=f"¡La IA {jugador_actual} ha ganado!")
                self.deshabilitar_botones()
            elif es_tablero_lleno(self.tablero):
                self.mensaje.config(text="¡Es un empate!")
                self.deshabilitar_botones()
            else:
                siguiente_jugador = "IA X" if self.turno_humano else "IA O"
                self.mensaje.config(text=f"Turno de la {siguiente_jugador}")
                self.root.after(500, self.turno_ia_vs_ia)  # Continua el ciclo

# ------------------- Funciones de Lógica del Juego ------------------- #

def crear_tablero():
    """Crea un tablero vacío de 4x4, representado por una lista de listas."""
    return [[VACIO for _ in range(4)] for _ in range(4)]  # Inicializa un tablero vacío

def hay_ganador(tablero, jugador):
    """
    Verifica si un jugador ha ganado el juego al conseguir 4 en línea.
    Revisa filas, columnas y diagonales.
    """
    for fila in tablero:
        if fila.count(jugador) == 4:  # Si una fila tiene las 4 posiciones ocupadas por el mismo jugador
            return True
    for col in range(4):
        if [fila[col] for fila in tablero].count(jugador) == 4:  # Si una columna tiene las 4 posiciones ocupadas
            return True
    # Revisar diagonales
    if [tablero[i][i] for i in range(4)].count(jugador) == 4:  # Diagonal principal
        return True
    if [tablero[i][3 - i] for i in range(4)].count(jugador) == 4:  # Diagonal secundaria
        return True
    return False  # Si no se cumple ninguna condición, no hay ganador

def es_tablero_lleno(tablero):
    """Verifica si el tablero está lleno (empate)."""
    return all(VACIO not in fila for fila in tablero)  # Si no hay casillas vacías, el tablero está lleno

# Función de evaluación heurística para la IA
def evaluar_tablero(tablero):
    """
    Evalúa el tablero asignando un puntaje heurístico.
    La IA obtiene puntajes más altos si está cerca de formar 4 en línea.
    """
    puntaje = 0

    # Asignar puntajes según cuántas casillas tiene cada jugador en filas, columnas y diagonales
    for fila in tablero:
        puntaje += evaluar_linea(fila)

    for col in range(4):
        puntaje += evaluar_linea([fila[col] for fila in tablero])

    puntaje += evaluar_linea([tablero[i][i] for i in range(4)])  # Diagonal principal
    puntaje += evaluar_linea([tablero[i][3 - i] for i in range(4)])  # Diagonal secundaria

    return puntaje

def evaluar_linea(linea):
    """
    Evalúa una línea de 4 casillas (fila, columna o diagonal).
    La IA obtiene más puntaje por líneas que tiene casi completas.
    """
    puntaje = 0
    if linea.count(IA) == 3 and linea.count(VACIO) == 1:
        puntaje += 100  # 3 en línea para la IA
    elif linea.count(JUGADOR) == 3 and linea.count(VACIO) == 1:
        puntaje -= 100  # 3 en línea para el jugador (la IA debe bloquear)
    return puntaje

# Minimax con poda Alfa-Beta
def minimax(tablero, profundidad, es_max, alpha, beta):
    """
    Implementa el algoritmo Minimax con poda Alfa-Beta, limitado por una profundidad máxima.
    """
    if hay_ganador(tablero, IA):
        return 1000  # La IA ha ganado
    if hay_ganador(tablero, JUGADOR):
        return -1000  # El jugador ha ganado
    if es_tablero_lleno(tablero) or profundidad == 0:
        return evaluar_tablero(tablero)  # Evalúa el tablero si se alcanza la profundidad máxima o no hay más movimientos

    if es_max:  # Maximiza el puntaje de la IA
        max_eval = -math.inf
        for i in range(4):
            for j in range(4):
                if tablero[i][j] == VACIO:
                    tablero[i][j] = IA
                    eval = minimax(tablero, profundidad - 1, False, alpha, beta)  # Llama recursivamente a minimax
                    tablero[i][j] = VACIO
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Poda Alfa-Beta
        return max_eval
    else:  # Minimiza el puntaje del jugador
        min_eval = math.inf
        for i in range(4):
            for j in range(4):
                if tablero[i][j] == VACIO:
                    tablero[i][j] = JUGADOR
                    eval = minimax(tablero, profundidad - 1, True, alpha, beta)
                    tablero[i][j] = VACIO
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Encuentra el mejor movimiento para la IA
def mejor_movimiento(tablero, profundidad):
    """Encuentra el mejor movimiento posible para la IA usando Minimax con Poda Alfa-Beta."""
    mejor_valor = -math.inf
    mejor_mov = (-1, -1)  # Coordenadas iniciales del mejor movimiento
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == VACIO:
                tablero[i][j] = IA
                mov_valor = minimax(tablero, profundidad, False, -math.inf, math.inf)
                tablero[i][j] = VACIO
                if mov_valor > mejor_valor:  # Actualiza el mejor movimiento
                    mejor_valor = mov_valor
                    mejor_mov = (i, j)
    return mejor_mov

# ------------------- EJECUCIÓN DEL PROGRAMA ------------------- #

if __name__ == "__main__":
    root = tk.Tk()  # Crear la ventana principal
    juego = JuegoGato4x4(root)  # Crear el objeto de juego
    root.mainloop()  # Iniciar el loop de la ventana
