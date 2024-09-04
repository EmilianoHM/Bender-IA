import tkinter as tk
import random

class JuegoGato:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Gato 4x4")
        self.jugador_simbolo = "X"
        self.computadora_simbolo = "O"
        self.jugador_ganadas = 0
        self.computadora_ganadas = 0
        self.primer_movimiento_jugador = True
        self.crear_widgets()
        self.iniciar_juego()

    def crear_widgets(self):
        self.tablero_frame = tk.Frame(self.root)
        self.tablero_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)  # Espacio añadido con padx y pady

        self.botones = [[None for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                boton = tk.Button(self.tablero_frame, text=" ", font=("Arial", 20), width=5, height=2,
                                  command=lambda i=i, j=j: self.movimiento_jugador(i, j))
                boton.grid(row=i, column=j)
                self.botones[i][j] = boton

        self.reset_button = tk.Button(self.root, text="Reiniciar", font=("Arial", 15), command=self.reiniciar_juego)
        self.reset_button.grid(row=1, column=0, columnspan=4, pady=10)  # Espacio vertical con pady

        self.cambiar_simbolo_button = tk.Button(self.root, text="Cambiar Símbolo", font=("Arial", 15), command=self.cambiar_simbolo)
        self.cambiar_simbolo_button.grid(row=2, column=0, columnspan=4, pady=10)  # Espacio vertical con pady

        self.resultado_label = tk.Label(self.root, text="", font=("Arial", 20))
        self.resultado_label.grid(row=3, column=0, columnspan=4, pady=10)  # Espacio vertical con pady

        self.contador_label = tk.Label(self.root, text="Jugador: 0  |  Computadora: 0", font=("Arial", 15))
        self.contador_label.grid(row=4, column=0, columnspan=4, pady=10)  # Espacio vertical con pady

    def iniciar_juego(self):
        self.tablero = [[" " for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.botones[i][j].config(text=" ", state="normal")
        self.resultado_label.config(text="")
        if not self.primer_movimiento_jugador:
            self.movimiento_computadora()
        self.primer_movimiento_jugador = not self.primer_movimiento_jugador

    def movimiento_jugador(self, fila, columna):
        if self.tablero[fila][columna] == " ":
            self.tablero[fila][columna] = self.jugador_simbolo
            self.botones[fila][columna].config(text=self.jugador_simbolo)
            if self.verificar_ganador(self.jugador_simbolo):
                self.jugador_ganadas += 1
                self.actualizar_contador()
                self.finalizar_juego("¡Ganaste!")
            elif self.tablero_lleno():
                self.finalizar_juego("¡Es un empate!")
            else:
                self.movimiento_computadora()

    def movimiento_computadora(self):
        while True:
            fila = random.randint(0, 3)
            columna = random.randint(0, 3)
            if self.tablero[fila][columna] == " ":
                self.tablero[fila][columna] = self.computadora_simbolo
                self.botones[fila][columna].config(text=self.computadora_simbolo)
                break
        if self.verificar_ganador(self.computadora_simbolo):
            self.computadora_ganadas += 1
            self.actualizar_contador()
            self.finalizar_juego("¡La computadora ganó!")
        elif self.tablero_lleno():
            self.finalizar_juego("¡Es un empate!")

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
        self.resultado_label.config(text=mensaje)

    def reiniciar_juego(self):
        self.iniciar_juego()

    def actualizar_contador(self):
        self.contador_label.config(text=f"Jugador: {self.jugador_ganadas}  |  Computadora: {self.computadora_ganadas}")

    def cambiar_simbolo(self):
        if self.jugador_simbolo == "X":
            self.jugador_simbolo = "O"
            self.computadora_simbolo = "X"
        else:
            self.jugador_simbolo = "X"
            self.computadora_simbolo = "O"
        self.reiniciar_juego()

if __name__ == "__main__":
    root = tk.Tk()
    juego = JuegoGato(root)
    root.mainloop()
