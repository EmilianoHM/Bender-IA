import tkinter as tk
import random

class JuegoGato:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Gato 4x4")
        self.crear_widgets()
        self.iniciar_juego()

    def crear_widgets(self):
        self.tablero_frame = tk.Frame(self.root)
        self.tablero_frame.grid(row=0, column=0, columnspan=4)

        self.botones = [[None for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                boton = tk.Button(self.tablero_frame, text=" ", font=("Arial", 20), width=5, height=2,
                                  command=lambda i=i, j=j: self.movimiento_jugador(i, j))
                boton.grid(row=i, column=j)
                self.botones[i][j] = boton

        self.reset_button = tk.Button(self.root, text="Reiniciar", font=("Arial", 15), command=self.reiniciar_juego)
        self.reset_button.grid(row=1, column=0, columnspan=4)

    def iniciar_juego(self):
        self.turno_jugador = True
        self.tablero = [[" " for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.botones[i][j].config(text=" ", state="normal")

    def movimiento_jugador(self, fila, columna):
        if self.tablero[fila][columna] == " ":
            self.tablero[fila][columna] = "X"
            self.botones[fila][columna].config(text="X")
            if self.verificar_ganador("X"):
                self.finalizar_juego("¡Ganaste!")
            elif self.tablero_lleno():
                self.finalizar_juego("¡Es un empate!")
            else:
                self.turno_jugador = False
                self.movimiento_computadora()

    def movimiento_computadora(self):
        while True:
            fila = random.randint(0, 3)
            columna = random.randint(0, 3)
            if self.tablero[fila][columna] == " ":
                self.tablero[fila][columna] = "O"
                self.botones[fila][columna].config(text="O")
                break
        if self.verificar_ganador("O"):
            self.finalizar_juego("¡La computadora ganó!")
        elif self.tablero_lleno():
            self.finalizar_juego("¡Es un empate!")
        self.turno_jugador = True

    def verificar_ganador(self, jugador):
        # Verificar filas y columnas
        for i in range(4):
            if all(self.tablero[i][j] == jugador for j in range(4)) or \
               all(self.tablero[j][i] == jugador for j in range(4)):
                return True
        # Verificar diagonales
        if all(self.tablero[i][i] == jugador for i in range(4)) or \
           all(self.tablero[i][3 - i] == jugador for i in range(4)):
            return True
        return False

    def tablero_lleno(self):
        return all(self.tablero[i][j] != " " for i in range(4) for j in range(4))

    def finalizar_juego(self, mensaje):
        for i in range(4):
            for j in range(4):
                self.botones[i][j].config(state="disabled")
        resultado = tk.Label(self.root, text=mensaje, font=("Arial", 20))
        resultado.grid(row=2, column=0, columnspan=4)

    def reiniciar_juego(self):
        # Limpiar el mensaje final si existe
        for widget in self.root.grid_slaves(row=2):
            widget.destroy()
        # Reiniciar el juego
        self.iniciar_juego()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoGato(root)
    root.mainloop()
