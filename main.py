import tkinter as tk
from tkinter import messagebox

class Reversi:
    def __init__(self):
        #inicias un tablero 8*8 con puro 0
        self.tablero = [[0 for _ in range(8)] for _ in range(8)] 
        #inicia el negro (-1)
        self.turno = -1  
        #piezas iniciales
        self.iniciar_juego()

    def iniciar_juego(self):
        # Coloca las piezas iniciales en el tablero
        self.tablero[3][3] = self.tablero[4][4] = 1  # Piezas blancas
        self.tablero[3][4] = self.tablero[4][3] = -1  # Piezas negras

    def jugada_valida(self, x, y):
        #checa si (x,y) vacia. sino, no jala la jugada
        if self.tablero[x][y] != 0:
            return False

        # Posibles direcciones  
        direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                       (0, 1), (1, -1), (1, 0), (1, 1)]
        valido = False
        
        #Recorres todas las direcciones pa ver si en alguna se puede
        for dx, dy in direcciones:
            if self._puede_voltear(x, y, dx, dy): #al menos una que sí
                valido = True
        return valido

    def _puede_voltear(self, x, y, dx, dy):
        # Verificar si se pueden voltear piezas en una dirección
        i, j = x + dx, y + dy #calculas la primera casilla en direccion 
        piezas_entre = 0 #cuenta piezas contrarias entre jugada y popia
        
        #Mientras estas adentro y encuentras piezas contrarias 
        while 0 <= i < 8 and 0 <= j < 8 and self.tablero[i][j] == -self.turno:
            piezas_entre += 1 # aumentas el contador 
            i += dx #Mueves 
            j += dy

        #Si hay piezas contrarias y terminamos en propia, se vale voltear
        if piezas_entre > 0 and 0 <= i < 8 and 0 <= j < 8 and self.tablero[i][j] == self.turno:
            return True
        return False # sino pues no 

    def realizar_jugada(self, x, y):
        #checas si se vale
        if self.jugada_valida(x, y):
            self.tablero[x][y] = self.turno #oloca la pieza del jugador en pose (x,y)
            self.voltear_piezas(x, y) #le volteas 
            self.turno = -self.turno  # Cambias turno
            return True #jugada hecha 
        return False #juega bien

    def voltear_piezas(self, x, y):
        #Posibles direcciones 
        direcciones = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                       (0, 1), (1, -1), (1, 0), (1, 1)]
        
        #recorremos direcciones 
        for dx, dy in direcciones:
            if self._puede_voltear(x, y, dx, dy): # si hay piezas pa voltear por ese rumbo
                self._voltear_en_direccion(x, y, dx, dy) #ps volteas

    def _voltear_en_direccion(self, x, y, dx, dy):
        # Voltear piezas en una dirección
        i, j = x + dx, y + dy
        
        #Mientras sigas encontrando piezas del otor
        while self.tablero[i][j] == -self.turno: 
            self.tablero[i][j] = self.turno # voltear la pieza al color del mero mero
            i += dx #le sigues moviendo
            j += dy

    def obtener_jugadas_validas(self):
        #hace una lista con todas jugadas validas 
        jugadas = []
        #recorres el tablero
        for x in range(8):
            for y in range(8):
                if self.jugada_valida(x, y): # si (x,y) es valido
                    jugadas.append((x, y)) # le agregas a la lusta
        return jugadas # le regresa la lisra de validas 

    def is_game_over(self):
        if len(self.obtener_jugadas_validas()) == 0: return True
        return False

    def game_result(self):
        white_score = sum(fila.count(1) for fila in self.juego.tablero)
        black_score = sum(fila.count(-1) for fila in self.juego.tablero)
        if black_score > white_score: return -1
        elif black_score < white_score: return 1
        else: return 0

class InterfazReversi:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Reversi")
        self.raiz.configure(bg="lightgray")
        
        self.inicializar_juego()

    def inicializar_juego(self):
        self.juego = Reversi()
        self.cursor_pos = [0, 0]  # Posición inicial del cursor para el teclado
        self.crear_interfaz()
        self.actualizar_tablero()

    def crear_interfaz(self):
        # Información de Turno
        self.info_turno = tk.Label(self.raiz, text="Turno: ⚪ Blanco", font=("Arial", 14), bg="lightgray")
        self.info_turno.grid(row=0, column=0, columnspan=8, pady=10)
        
        # Marcador
        self.marcador = tk.Label(self.raiz, text="⚪: 0 | ⚫: 0", font=("Arial", 12), bg="lightgray")
        self.marcador.grid(row=1, column=0, columnspan=8)
        
        # Botón de Reinicio
        self.boton_reiniciar = tk.Button(self.raiz, text="Reiniciar Juego", command=self.reiniciar_juego, bg="blue", fg="white", font=("Arial", 12))
        self.boton_reiniciar.grid(row=2, column=0, columnspan=8, pady=5)
        
        # Tablero
        self.botones = [[None for _ in range(8)] for _ in range(8)]
        for x in range(8):
            for y in range(8):
                boton = tk.Button(self.raiz, width=4, height=2, bg="darkgreen", state="normal")
                boton.grid(row=x+3, column=y, padx=1, pady=1)  # Espaciado entre botones
                self.botones[x][y] = boton
                boton.config(command=lambda x=x, y=y: self.realizar_jugada_mouse(x, y))
        
        # Vincular controles de teclado
        self.raiz.bind("<Up>", self.mover_cursor)
        self.raiz.bind("<Down>", self.mover_cursor)
        self.raiz.bind("<Left>", self.mover_cursor)
        self.raiz.bind("<Right>", self.mover_cursor)
        self.raiz.bind("<Return>", self.realizar_jugada_teclado)
        
    def reiniciar_juego(self):
        #Reinicia el juego.
        self.inicializar_juego()

    def mover_cursor(self, event):
        #Mueve el cursor en el tablero con las teclas de flecha
        if event.keysym == "Up":
            self.cursor_pos[0] = (self.cursor_pos[0] - 1) % 8
        elif event.keysym == "Down":
            self.cursor_pos[0] = (self.cursor_pos[0] + 1) % 8
        elif event.keysym == "Left":
            self.cursor_pos[1] = (self.cursor_pos[1] - 1) % 8
        elif event.keysym == "Right":
            self.cursor_pos[1] = (self.cursor_pos[1] + 1) % 8
        self.actualizar_tablero()

    def realizar_jugada_teclado(self, event):
        #Realiza la jugada en la posición actual del cursor
        x, y = self.cursor_pos
        self.realizar_jugada(x, y)
        
    def realizar_jugada_mouse(self, x, y):
        # Ahora solo se realiza la jugada en la posición (x, y) que el mouse selecciona
        if self.juego.realizar_jugada(x, y):
            self.actualizar_tablero()
            if not self.juego.obtener_jugadas_validas():
                self.juego.turno = -self.juego.turno
                if not self.juego.obtener_jugadas_validas():
                    self.finalizar_juego()
        else:
            messagebox.showwarning("Jugada inválida", "No puedes realizar esa jugada.")


    def realizar_jugada(self, x, y):
        if self.juego.realizar_jugada(x, y):
            self.actualizar_tablero()
            if not self.juego.obtener_jugadas_validas():
                self.juego.turno = -self.juego.turno
                if not self.juego.obtener_jugadas_validas():
                    self.finalizar_juego()
        else:
            messagebox.showwarning("Jugada inválida", "No puedes realizar esa jugada.")

    def actualizar_tablero(self):
        #Actualiza el tablero visualmente, incluyendo indicadores de jugadas válidas y marcador.
        puntaje_blanco = sum(fila.count(1) for fila in self.juego.tablero)
        puntaje_negro = sum(fila.count(-1) for fila in self.juego.tablero)
        
        # Actualizar marcador
        self.marcador.config(text=f"⚪: {puntaje_blanco} | ⚫: {puntaje_negro}")
        
        # Actualizar turno
        turno = "⚪ Blanco" if self.juego.turno == 1 else "⚫ Negro"
        self.info_turno.config(text=f"Turno: {turno}")
        
        # Actualizar tablero y jugadas válidas
        jugadas_validas = self.juego.obtener_jugadas_validas()
        for x in range(8):
            for y in range(8):
                valor = self.juego.tablero[x][y]
                if valor == 1:
                    self.botones[x][y].config(text="⚪", state="disabled", bg="white")
                elif valor == -1:
                    self.botones[x][y].config(text="⚫", state="disabled", bg="black")
                else:
                    self.botones[x][y].config(text="", state="normal", bg="palevioletred")
                if (x, y) in jugadas_validas:
                    self.botones[x][y].config(bg="mediumpurple")  # Resaltar jugadas válidas
        
        # Resaltar posición del cursor
        cx, cy = self.cursor_pos
        self.botones[cx][cy].config(bg="mediumvioletred")

    def finalizar_juego(self):
        puntaje_blanco = sum(fila.count(1) for fila in self.juego.tablero)
        puntaje_negro = sum(fila.count(-1) for fila in self.juego.tablero)
        ganador = "Blanco" if puntaje_blanco > puntaje_negro else "Negro"
        if puntaje_blanco == puntaje_negro:
            ganador = "Empate"
        messagebox.showinfo("Juego terminado", f"Ganador: {ganador}\nBlanco: {puntaje_blanco} | Negro: {puntaje_negro}")
        self.raiz.destroy()

if __name__ == "__main__":
    raiz = tk.Tk()
    interfaz = InterfazReversi(raiz)
    raiz.mainloop()
