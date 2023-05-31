from termcolor import colored
import os

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


def score_line(line):
    score = 0
    if line.count('O') == 3 and line.count(' ') == 1:
        score += 100
    elif line.count('O') == 2 and line.count(' ') == 2:
        score += 10
    if line.count('X') == 3 and line.count(' ') == 1:
        score -= 100
    return score

def score(tablero, tamaño):
    score = 0
    # check filas
    for capa in range(tamaño):
        for fila in range(tamaño):
            score += score_line(tablero[capa][fila])
    # check columnas
    for capa in range(tamaño):
        for col in range(tamaño):
            column = [tablero[capa][fila][col] for fila in range(tamaño)]
            score += score_line(column)
    # check diagonales
    for capa in range(tamaño):
        diagonal1 = [tablero[capa][i][i] for i in range(tamaño)]
        diagonal2 = [tablero[capa][i][tamaño - i - 1] for i in range(tamaño)]
        score += score_line(diagonal1)
        score += score_line(diagonal2)
    # check profundidad
    for fila in range(tamaño):
        for col in range(tamaño):
            depth = [tablero[capa][fila][col] for capa in range(tamaño)]
            score += score_line(depth)
    # check diagonales por profundidad
    diagonal1 = [tablero[i][i][i] for i in range(tamaño)]
    diagonal2 = [tablero[i][i][tamaño - i - 1] for i in range(tamaño)]
    diagonal3 = [tablero[i][tamaño - i - 1][i] for i in range(tamaño)]
    diagonal4 = [tablero[i][tamaño - i - 1][tamaño - i - 1] for i in range(tamaño)]
    score += score_line(diagonal1)
    score += score_line(diagonal2)
    score += score_line(diagonal3)
    score += score_line(diagonal4)
    
    ganador = check_ganador(tablero, tamaño)
    if ganador == 'X':
        return float('-inf')
    elif ganador == 'O':
        return float('inf')
    
    return score


def minimax(tablero, tamaño, depth, alpha, beta, is_maximizing, transposition_table):
    state = tuple(tuple(tuple(tablero[capa][fila]) for fila in range(tamaño)) for capa in range(tamaño))
    if state in transposition_table:
        return transposition_table[state]
    if depth == 0 or check_ganador(tablero, tamaño) is not None:
        eval_score = score(tablero, tamaño)
        transposition_table[state] = eval_score
        return eval_score
    if is_maximizing:
        max_eval = float('-inf')
        for capa in range(tamaño):
            for fila in range(tamaño):
                for col in range(tamaño):
                    if tablero[capa][fila][col] == " ":
                        tablero[capa][fila][col] = 'O'
                        eval_score = minimax(tablero, tamaño, depth - 1, alpha, beta, False, transposition_table)
                        tablero[capa][fila][col] = " "
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        if beta <= alpha:
                            break
        transposition_table[state] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for capa in range(tamaño):
            for fila in range(tamaño):
                for col in range(tamaño):
                    if tablero[capa][fila][col] == " ":
                        tablero[capa][fila][col] = 'X'
                        eval_score = minimax(tablero, tamaño, depth - 1, alpha, beta, True, transposition_table)
                        tablero[capa][fila][col] = " "
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        if beta <= alpha:
                            break
        transposition_table[state] = min_eval
        return min_eval


def iterative_deepening(tablero, tamaño, max_depth):
    best_move = None
    transposition_table = {}
    for depth in range(1, max_depth + 1):
        best_score = float('-inf')
        for capa in range(tamaño):
            for fila in range(tamaño):
                for col in range(tamaño):
                    if tablero[capa][fila][col] == " ":
                        tablero[capa][fila][col] = 'O'
                        score = minimax(tablero, tamaño, depth - 1, float('-inf'), float('inf'), False,
                                        transposition_table)
                        tablero[capa][fila][col] = " "
                        if score > best_score:
                            best_score = score
                            best_move = (capa, fila,col)
    return best_move

def realizar_movimiento_bot(tablero,jugador,tamaño):
    print("bot juega")
    valid_move=False
    while not valid_move:
        capa,x,y=iterative_deepening(tablero,tamaño,tamaño**2)
        if tablero[capa][x][y]==" ":
            tablero[capa][x][y]=jugador
            valid_move=True



def main():
    tamaño = obtener_tablero_tamaño()
    tablero = init_tablero(tamaño)
    jugador = 'X'
    juego_terminado = False
    while not juego_terminado:
        os.system('cls')
        mostrar_tablero(tablero, tamaño)
        if jugador == 'O':
            realizar_movimiento(tablero, jugador, tamaño)
        else:
            realizar_movimiento_bot(tablero, jugador, tamaño)
        ganador = check_ganador(tablero, tamaño)
        if ganador is not None:
            os.system('cls')
            mostrar_tablero(tablero, tamaño)
            print(f"Jugador {ganador} gana!")
            juego_terminado = True
        elif check_empate(tablero, tamaño):
            limpiar_pantalla()
            mostrar_tablero(tablero, tamaño)
            print("El juego termina en empate.")
            juego_terminado = True
        if jugador == 'X':
            jugador = 'O'
        else:
            jugador = 'X'


if __name__ == "__main__":
    main()