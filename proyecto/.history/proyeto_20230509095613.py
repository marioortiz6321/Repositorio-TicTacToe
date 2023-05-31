from termcolor import colored
import random


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


def realizar_movimiento_bot(tablero, jugador, tamaño):
    print("bot juega")
    valid_move = False
    while not valid_move:
        capa = random.randint(0, tamaño - 1)
        position = random.randint(0, tamaño * tamaño - 1)
        x = position // tamaño
        y = position % tamaño
        if tablero[capa][x][y] == " ":
            tablero[capa][x][y] = jugador
            valid_move = True


def check_empate(tablero, tamaño):
    for capa in range(tamaño):
        for fila in range(tamaño):
            for col in range(tamaño):
                if tablero[capa][fila][col] == " ":
                    return False
    return True


def realizar_movimiento_bot(tablero, jugador, tamaño):
    print("bot juega")
    valid_move = False
    while not valid_move:
        capa = random.randint(0, tamaño - 1)
        position = random.randint(0, tamaño * tamaño - 1)
        x = position // tamaño
        y = position % tamaño
        if tablero[capa][x][y] == " ":
            tablero[capa][x][y] = jugador
            valid_move = True


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