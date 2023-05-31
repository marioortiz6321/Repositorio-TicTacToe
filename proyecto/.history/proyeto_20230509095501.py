from termcolor import colored
import math
import random

def realizar_movimiento_bot(tablero, jugador, tamaño):
    print("bot juega")
    valid_move = False
    while not valid_move:
        move = monte_carlo_tree_search(tablero, jugador, tamaño)
        capa = move[0]
        x = move[1]
        y = move[2]
        if tablero[capa][x][y] == " ":
            tablero[capa][x][y] = jugador
            valid_move = True

def monte_carlo_tree_search(tablero, jugador, tamaño):
    root = Node(state=(tablero, jugador))
    for _ in range(1000):
        leaf = root.select_leaf(tamaño)
        child = leaf.expand(tamaño)
        winner = child.simulate(tamaño)
        child.backpropagate(winner)
    return root.best_child().move

class Node:
    def __init__(self, state=None, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0

    def select_leaf(self, tamaño):
        current = self
        while current.children:
            current = current.best_child(c_param=1 / math.sqrt(2))
        return current

    def expand(self, tamaño):
        tablero, jugador = self.state
        if check_ganador(tablero, tamaño) is not None or check_empate(tablero, tamaño):
            return self
        next_jugador = 'X' if jugador == 'O' else 'O'
        for capa in range(tamaño):
            for fila in range(tamaño):
                for col in range(tamaño):
                    if tablero[capa][fila][col] == " ":
                        new_tablero = [layer.copy() for layer in tablero]
                        new_tablero[capa][fila][col] = jugador
                        new_state = (new_tablero, next_jugador)
                        new_move = (capa, fila, col)
                        child = Node(state=new_state, parent=self, move=new_move)
                        self.children.append(child)
        child = random.choice(self.children)
        return child

    def simulate(self, tamaño):
        tablero, jugador = self.state
        while True:
            ganador = check_ganador(tablero, tamaño)
            if ganador is not None:
                return ganador
            if check_empate(tablero, tamaño):
                return None
            capa = random.randint(0, tamaño - 1)
            position = random.randint(0, tamaño * tamaño - 1)
            x = position // tamaño
            y = position % tamaño
            if tablero[capa][x][y] == " ":
                tablero[capa][x][y] = jugador
                jugador = 'X' if jugador == 'O' else 'O'

    def backpropagate(self, winner):
        current = self
        while current.parent is not None:
            current.visits += 1
            if winner is not None and winner == current.state[1]:
                current.wins += 1
            current = current.parent

    def best_child(self, c_param=0.5):
        weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits) / child.visits))
            if child.visits > 0 and self.visits > 0 and (2 * math.log(self.visits) / child.visits) >= 0 else 0
            for child in self.children
        ]
        max_index = max(range(len(weights)), key=weights.__getitem__)
        return self.children[max_index]

def obtener_tablero_tamaño():
    while True:
        tamaño = input("Elige el tamaño de las capas (3, 4, 5 o 6): ")
        if tamaño in ["3", "4", "5", "6"]:
            return int(tamaño)
        else:
            print("Tamaño inválido. Por favor elige 3, 4, 5 o 6.")
def init_tablero(tamaño):
    tablero = []
    for _ in range(tamaño):
        capa = []
        for _ in range(tamaño):
            fila = [" "] * tamaño
            capa.append(fila)
        tablero.append(capa)
    return tablero
def mostrar_tablero(tablero, tamaño):
    for z in range(tamaño):
        print(f"capa {z + 1}")
        print("┌" + "───┬" * (tamaño - 1) + "───┐")
        for x in range(tamaño):
            for y in range(tamaño):
                if tablero[z][x][y] == "X":
                    print("│ " + colored(tablero[z][x][y], "red") + " ", end="")
                elif tablero[z][x][y] == "O":
                    print("│ " + colored(tablero[z][x][y], "blue") + " ", end="")
                else:
                    print("│   ", end="")
            print("│")
            if x != tamaño - 1:
                print("├" + "───┼" * (tamaño - 1) + "───┤")
        print("└" + "───┴" * (tamaño - 1) + "───┘")
        print()
def realizar_movimiento(tablero, jugador, tamaño):
    valid_move = False
    while not valid_move:
        capa = int(input(f"jugador {jugador}, eliga una capa (1-{tamaño}): ")) - 1
        position = int(input(f"jugador {jugador}, eliga una posicion (1-{tamaño * tamaño}): ")) - 1
        x = position // tamaño
        y = position % tamaño
        if tablero[capa][x][y] == " ":
            tablero[capa][x][y] = jugador
            valid_move = True
        else:
            print("Esa poscicion ya esta ocupada. Porfavor eliga otra.")
def check_ganador(tablero, tamaño):
    # check filas
    for capa in range(tamaño):
        for fila in range(tamaño):
            if all(tablero[capa][fila][col] == tablero[capa][fila][0] for col in range(tamaño)) and tablero[capa][fila][
                0] != " ":
                return tablero[capa][fila][0]
    # check columnas
    for capa in range(tamaño):
        for col in range(tamaño):
            if all(tablero[capa][fila][col] == tablero[capa][0][col] for fila in range(tamaño)) and tablero[capa][0][
                col] != " ":
                return tablero[capa][0][col]
    # check diagonales
    for capa in range(tamaño):
        if all(tablero[capa][i][i] == tablero[capa][0][0] for i in range(tamaño)) and tablero[capa][0][0] != " ":
            return tablero[capa][0][0]
        if all(tablero[capa][i][tamaño - i - 1] == tablero[capa][0][tamaño - 1] for i in range(tamaño)) and \
                tablero[capa][0][tamaño - 1] != " ":
            return tablero[capa][0][tamaño - 1]
    # check profundidad
    for fila in range(tamaño):
        for col in range(tamaño):
            if all(tablero[capa][fila][col] == tablero[0][fila][col] for capa in range(tamaño)) and tablero[0][fila][
                col] != " ":
                return tablero[0][fila][col]
    # check diagonales por profundidad
    for i in range(tamaño):
        if all(tablero[j][i][i] == tablero[0][i][i] for j in range(tamaño)) and tablero[0][i][i] != " ":
            return tablero[0][i][i]
        if all(tablero[j][i][tamaño - i - 1] == tablero[0][i][tamaño - i - 1] for j in range(tamaño)) and tablero[0][i][
            tamaño - i - 1] != " ":
            return tablero[0][i][tamaño - i - 1]
        if all(tablero[i][i][i] == tablero[0][0][0] for i in range(tamaño)) and tablero[0][0][0] != " ":
            return tablero[0][0][0]
        if all(tablero[i][i][tamaño - i - 1] == tablero[0][0][tamaño - 1] for i in range(tamaño)) and tablero[0][0][
            tamaño - 1] != " ":
            return tablero[0][0][tamaño - 1]

    # no ganador
    return None
def check_empate(tablero, tamaño):
    for capa in range(tamaño):
        for fila in range(tamaño):
            for col in range(tamaño):
                if tablero[capa][fila][col] == " ":
                    return False
    return True


def check_empate(tablero, tamaño):
    for capa in range(tamaño):
        for fila in range(tamaño):
            for col in range(tamaño):
                if tablero[capa][fila][col] == " ":
                    return False
    return True


def main():
    tamaño = obtener_tablero_tamaño()
    tablero = init_tablero(tamaño)
    jugador = 'X'
    juego_terminado = False
    while not juego_terminado:
        mostrar_tablero(tablero, tamaño)
        if jugador == 'O':
            realizar_movimiento(tablero, jugador, tamaño)
        else:
            realizar_movimiento_bot(tablero, jugador, tamaño)
        ganador = check_ganador(tablero, tamaño)
        if ganador is not None:
            mostrar_tablero(tablero, tamaño)
            print(f"Jugador {ganador} gana!")
            juego_terminado = True
        elif check_empate(tablero, tamaño):
            mostrar_tablero(tablero, tamaño)
            print("El juego termina en empate.")
            juego_terminado = True
        if jugador == 'X':
            jugador = 'O'
        else:
            jugador = 'X'
if __name__ == "__main__":
    main()