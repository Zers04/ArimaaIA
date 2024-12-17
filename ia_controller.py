from config import *
import game_controller
import copy

# Funcion para ejecutar la IA
def play(screen, current_player, moves, max_moves, winner, pieces):
    
    # Definir variables para alpha-beta
    depth = 3
    alpha = float('-inf')
    beta = float('inf')
    maximizing_player = True

    # Comprobar si ya hay un ganador
    if winner:
        return current_player, moves, max_moves, winner, pieces  # Devolver el estado actual de piezas
      
    # Si se alcanzó el máximo de movimientos, cambiar de turno
    if moves == max_moves:
        current_player, moves = game_controller.end_turn(current_player, moves, max_moves)
        return current_player, moves, max_moves, winner, pieces
    
    print("IA jugando")
    
    # Ejecutar alpha-beta para determinar el mejor movimiento
    _, new_board = alphabeta(depth, alpha, beta, maximizing_player, current_player, pieces, moves, max_moves)
    
    # Actualizar las piezas globales con el nuevo tablero
    pieces = new_board
    
    # Incrementar el número de movimientos
    moves += 1

    # Verificar si hay piezas eliminadas
    pieces = game_controller.eliminated_piece(pieces)

    # Verificar si hay un ganador
    winner = game_controller.win_condition(winner, pieces)
    
    return current_player, moves, max_moves, winner, pieces

# Poda alfa-beta
def alphabeta(depth, alpha, beta, maximizing_player, current_player, pieces, moves, max_moves):
    """
    Implementación del algoritmo Alpha-Beta Pruning teniendo en cuenta que cada jugador juega 4 movimientos.

    :param depth: La profundidad actual del árbol.
    :param alpha: El límite inferior de la ventana Alpha-Beta.
    :param beta: El límite superior de la ventana Alpha-Beta.
    :param maximizing_player: Booleano, True si el jugador actual es el jugador maximizador.
    :param current_player: El jugador actual.
    :param actual_pieces: Las piezas actuales.
    :param moves: El número de movimientos realizados.
    :return: El valor heurístico del nodo.
    """
   
    if depth == 0:
        # Usamos solo el valor heurístico (primer elemento de la tupla retornada por get_value)
        value, _ = get_value(current_player, pieces)
        return value, pieces

    best_board = None

    if maximizing_player:
        value = float('-inf')
        for board_info in create_boards(current_player, moves, pieces):
            board = board_info[2]  # Tercer elemento siempre es el nuevo tablero
            if moves < max_moves:
                new_value, _ = alphabeta(depth - 1, alpha, beta, True, current_player, board, moves + 1, max_moves)
            else:
                next_player = 'gold' if current_player == 'silver' else 'silver'
                new_value, _ = alphabeta(depth - 1, alpha, beta, False, next_player, board, 0, max_moves)
            
            if new_value > value:
                value = new_value
                best_board = board

            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_board
    else:
        value = float('inf')
        for board_info in create_boards(current_player, moves, pieces):
            board = board_info[2]  # Tercer elemento siempre es el nuevo tablero
            if moves < max_moves:
                new_value, _ = alphabeta(depth - 1, alpha, beta, False, current_player, board, moves + 1, max_moves)
            else:
                next_player = 'gold' if current_player == 'silver' else 'silver'
                new_value, _ = alphabeta(depth - 1, alpha, beta, True, next_player, board, 0, max_moves)
            
            if new_value < value:
                value = new_value
                best_board = board

            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_board
    
# Funcion para calcular todos los posibles movimientos de las piezas
def get_all_movements(current_player, pieces):
    """
    Función para calcular todos los posibles movimientos de las piezas.
    
    :return: Lista con los posibles movimientos con la forma (piece, move).
    """
    movements = []
    for piece in pieces:
        if piece["color"] == current_player:
            valid_moves = game_controller.get_valid_moves(piece, pieces)
            for move in valid_moves:
                movements.append((piece, move))
    return movements

# Funcion para calcular todos los posibles movimientos de empujar o tirar
def get_all_push_pulls(current_player, moves, pieces):
    """
    Función para calcular todos los posibles movimientos de empujar o tirar.
    
    :return: Lista con los posibles movimientos de empujar o tirar con la forma (piece, piece_attacked, move).
    """
    push_pulls = []
    valid_push_pulls_pieces = []
    valid_push_pulls_pos = []

    # Si moves es menor a 2, no se pueden realizar movimientos de empujar o tirar
    if moves > 2:
        return push_pulls
    
    for piece in pieces:
        if piece["color"] == current_player:
            # Obtener ubicacion de piezas validas para empujar o tirar
            valid_push_pulls_target = game_controller.get_valid_push_pull_pieces(piece, moves, pieces)

            if valid_push_pulls_target:
                # Obtener las piezas en las posiciones validas
            
                for push_pull_target in valid_push_pulls_target:
                    
                    piece_attacked = game_controller.get_piece_from_square(push_pull_target, pieces)
                    
                    if piece_attacked:
                        valid_push_pulls_pieces.append(piece_attacked)
                        
           
            if valid_push_pulls_pieces:
                # Obtener posibles movimientos de empujar o tirar
                # para cada pieza en valid_push_pulls_pieces, traerla completa
                for piece_attacked in valid_push_pulls_pieces:
                    if piece_attacked:
                        valid_push_pulls_pos = game_controller.get_valid_push_pull(piece, piece_attacked, pieces)

            if valid_push_pulls_pos:
                for push_pull in valid_push_pulls_pos:
                    push_pulls.append((piece, piece_attacked, push_pull))

        valid_push_pulls_target = []
        valid_push_pulls_pieces = []
        valid_push_pulls_pos = []


    return push_pulls

# Funcion para crear los tableros de los posibles movimientos
def create_boards(current_player, moves, pieces):
    """
    Función para crear los tableros de los posibles movimientos.
    
    :param current_player: El jugador actual.
    :param moves: El número de movimientos realizados.
    :param pieces: Lista original de piezas.
    :return: Lista de tableros con la forma (piece, move, board).
    """
    boards = []
    
    # Obtener movimientos estándar
    movements = get_all_movements(current_player, pieces)
    
    for piece, move in movements:
        # Crear una copia profunda de pieces PARA CADA iteración
        pieces_copy = [p.copy() for p in pieces]  # Nueva copia en cada iteración

        # Aplicar el movimiento en la copia
        new_board = game_controller.move_piece(piece, move, pieces_copy)

        # Agregar el nuevo estado del tablero a la lista
        boards.append((piece, move, new_board))

    if moves > 2:
        return boards
    
    else:
        # Obtener movimientos de push/pull
        push_pulls = get_all_push_pulls(current_player, moves, pieces)
        for piece, piece_attacked, move in push_pulls:
            # Crear una copia profunda de pieces PARA CADA iteración
            pieces_copy = [p.copy() for p in pieces]  # Nueva copia en cada iteración

            # Aplicar el movimiento push/pull en la copia
            new_board = game_controller.move_piece_push_pull(piece, piece_attacked, move, pieces_copy)

            # Agregar el nuevo estado del tablero a la lista
            boards.append((piece, move, new_board, piece_attacked))

    return boards

# Funcion para obtener el valor heuristico de un tablero
def get_value(current_player, pieces):
    """
    Función para calcular el valor heurístico de un tablero.
    
    :param current_player: El jugador actual.
    :param pieces: Las piezas actuales.
    :return: El valor heurístico del tablero.
    """
    if current_player == 'gold':
        enemy_player = 'silver'
    else:
        enemy_player = 'gold'
    
    value = 0

    value += pieces_value(current_player, pieces) - pieces_value(enemy_player, pieces)

    value += goal_distance(current_player, pieces) - goal_distance(enemy_player, pieces)

    value += near_trap(current_player, pieces) - near_trap(enemy_player, pieces)

    value += in_trap(current_player, pieces) - in_trap(enemy_player, pieces)

    value += freeze_piece(current_player, pieces) - freeze_piece(enemy_player, pieces)

    value += piece_together(current_player, pieces) - piece_together(enemy_player, pieces)

    # retornar el valor heurístico junto con el movimiento

    data_to_return = (value, pieces)

    return data_to_return

############################################################################################################

# Funciones para obtener valores de la heuristica
def pieces_value(current_player, pieces):
    """
    Función para calcular el valor total de las piezas de un jugador.

    :param current_player: El jugador actual.
    :return: El valor total de las piezas del jugador.
    """
    
    value = 0
    if pieces:
        for piece in pieces:
            if piece["color"] == current_player:
                value += piece["value"]

    return value

# Funcion para obtner valor según distacia de los conejos a la meta
def goal_distance(current_player, pieces):
    """
    Función para calcular un valor según la distancia de los conejos a la meta.
    
    si el conejo está a 6 casillas de la meta su valor es 1, si esta a 5 su valor es 3, si esta a 4 su valor es 5, si esta a 3 su valor es 7, si esta a 2 su valor es 9, si esta a 1 su valor es 11
    :param current_player: El jugador actual.
    :return: El valor total de las piezas del jugador.
    """
    value = 0
    if pieces:
        for piece in pieces:
            if piece["type"] == "rabbit":
                if piece["color"] == current_player:
                    if piece["color"] == "silver":
                        if 6 - piece["position"][0] == 0:
                            value += 100
                        if 6 - piece["position"][0] == 1:   
                            value += 15
                        elif 6 - piece["position"][0] == 2:
                            value += 10
                        elif 6 - piece["position"][0] == 3:
                            value += 7
                        elif 6 - piece["position"][0] == 4:
                            value += 5
                        elif 6 - piece["position"][0] == 5:
                            value += 3
                        elif 6 - piece["position"][0] == 6:
                            value += 1
                    else:
                        if piece["position"][0] == 0:
                            value += 100
                        if piece["position"][0] == 1:
                            value += 15
                        elif piece["position"][0] == 2:
                            value += 10
                        elif piece["position"][0] == 3:
                            value += 7
                        elif piece["position"][0] == 4:
                            value += 5
                        elif piece["position"][0] == 5:
                            value += 3
                        elif piece["position"][0] == 6:
                            value += 1
            
    return value

# Funciones para obtener valores de la heuristica
def near_trap(current_player, pieces):
    """
    Función para calcular las piezas que están alrededor de las trampas.
    
    si hay una pieza alrededor el valor es 1, si hay dos el valor es 2, si hay tres el valor es 3

    :param current_player: El jugador actual.
    :return: El valor total de las piezas del jugador.
    """
    value = 0
    if pieces:
        for piece in pieces:
            if piece["color"] == current_player:
                if (piece["position"][0] + 1, piece["position"][1]) in TRAP_POSITIONS:
                    value += 1
                if (piece["position"][0] - 1, piece["position"][1]) in TRAP_POSITIONS:
                    value += 1
                if (piece["position"][0], piece["position"][1] + 1) in TRAP_POSITIONS:
                    value += 1
                if (piece["position"][0], piece["position"][1] - 1) in TRAP_POSITIONS:
                    value += 1
    return value

# Funciones para obtener valores de la heuristica    
def in_trap(current_player, pieces):
    """
    Función para calcular las piezas que están en las trampas.
    
    si hay una pieza enemiga en la trampa el valor es 1, si hay dos el valor es 2, si hay tres el valor es 3

    :param current_player: El jugador actual.
    :return: El valor total de las piezas del jugador.
    """
    value = 0
    if pieces:
        for piece in pieces:
            if piece["color"] != current_player and piece["type"] == "rabbit":
                if piece["position"] in TRAP_POSITIONS:
                    value += 11
            elif piece["color"] != current_player:
                if piece["position"] in TRAP_POSITIONS:
                    value += 7
    return value

# Funciones para obtener valores de la heuristica
def freeze_piece(current_player, pieces):
    """
    Función para calcular las piezas que están congeladas.
    
    si hay una pieza enemiga congelada el valor es 1, si hay dos el valor es 2, si hay tres el valor es 3

    :param current_player: El jugador actual.
    :return: El valor total de las piezas del jugador.
    """
    value = 0
    if pieces:
        for piece in pieces:
            if piece["color"] != current_player:
                if is_frozen(piece, pieces):
                    value += 5
    return value

# Funciones para obtener valores de la heuristica
def is_frozen(piece, pieces):
    """
    Función para calcular si una pieza está congelada.
    
    :param piece: La pieza a evaluar.
    :return: True si la pieza está congelada, False de lo contrario.
    """
    if pieces:
        for piece1 in pieces:
            if piece1["color"] != piece["color"] and piece1["value"] > piece["value"]:
                # Si la pieza 1 está alrededor de la pieza 2
                if (abs(piece1["position"][0] - piece["position"][0]) == 1 and piece1["position"][1] == piece["position"][1]) or (abs(piece1["position"][1] - piece["position"][1]) == 1 and piece1["position"][0] == piece["position"][0]):
                    return True
    return False

# Funciones para obtener valores de la heuristica
def piece_together(current_player, pieces):
    """
    Función para calcular las piezas que están juntas.
    
    si hay dos piezas aliadas el valor es 1

    :param current_player: El jugador actual.
    :return: El valor total de las piezas del jugador.
    """
    value = 0
    if pieces:
        for piece in pieces:
            if piece["color"] == current_player:
                if is_together(piece, pieces):
                    value += 1

    return value

# Funciones para obtener valores de la heuristica
def is_together(piece, pieces):
    """
    Función para calcular si una pieza está junta a otra aliada.
    
    :param piece: La pieza a evaluar.
    :return: True si la pieza está junta a otra aliada, False de lo contrario.
    """
    if pieces:
        for piece1 in pieces:
            if piece1["color"] == piece["color"] and piece1 != piece:
                if (abs(piece1["position"][0] - piece["position"][0]) == 1 and piece1["position"][1] == piece["position"][1]) or (abs(piece1["position"][1] - piece["position"][1]) == 1 and piece1["position"][0] == piece["position"][0]):
                    return True
    return False
