from config import *
import draw
import copy

# Manejar el clic del jugador
def handle_click(screen, mouse_pos, selected_piece, piece_attacked, current_player, moves, max_moves, winner, old_pieces):
    """
    Maneja el clic del jugador.
    """
    # Si ya hay un ganador, no hacer nada
    if winner:
        return selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves , winner, pieces
    
    # Si ya se alcanzó el máximo de movimientos por turno, no hacer nada
    if moves >= max_moves:
        current_player, moves = end_turn(current_player, moves, max_moves)
        
        return selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner, pieces
    
    square = get_square_from_pos(mouse_pos)

    # si no hay pieza seleccionada
    if not selected_piece:
        
        
        new_selected_piece = get_piece_from_square(square)
        # Seleccionar una pieza válida del jugador actual
        if new_selected_piece and new_selected_piece['color'] == current_player:
            selected_piece = new_selected_piece
            #return selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner, pieces
        else:
            print("Selecciona una pieza válida.")
            #return selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner, pieces

    elif selected_piece:
        
        if not piece_attacked:
            new_piece_attacked = get_piece_from_square(square)

            # Si ya hay una pieza seleccionada y se hace clic sobre una aliada o la misma pieza
            if new_piece_attacked and new_piece_attacked['color'] == current_player:
                selected_piece = new_piece_attacked
            
            # Si ya hay una pieza seleccionada y se hace clic sobre una enemiga
            elif new_piece_attacked and new_piece_attacked['color'] != current_player:

                piece_attacked = new_piece_attacked

            # Si se hace clic en una casilla vacía para mover la pieza seleccionada
            elif is_valid_move(selected_piece, square):
                old_pieces = copy.deepcopy(get_pieces())
                move_piece(selected_piece, square)
                eliminated_piece()
                moves += 1
                selected_piece = None
            
        elif piece_attacked:

            # Si hace clic sobre una aliada o la misma pieza
            option = get_piece_from_square(square)
            if option and option['color'] == current_player:
                selected_piece = option
                piece_attacked = None

            # Si se hace clic en una casilla vacía para empujar o tirar la pieza enemiga
            elif is_valid_push_pull(selected_piece, piece_attacked, square):
                old_pieces = copy.deepcopy(get_pieces())
                move_piece_push_pull(selected_piece, piece_attacked, square)
                eliminated_piece()
                moves += 2
                selected_piece = None
                piece_attacked = None

    current_player, moves = end_turn(current_player, moves, max_moves)
    winner = win_condition(winner)
    return selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner, old_pieces
    
# Seleccionar una coordenada de tablero según la posición del mouse
def get_square_from_pos(pos):
    """
    Convierte una posición de píxel a coordenadas de tablero.
    """
    x, y = pos
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    square = (row, col)

    return square

# Seleccionar una pieza según la posición
def get_piece_from_square(square):
    """
    Encuentra si hay una pieza en la posición dada.
    """
    for piece in pieces:
        if piece['position'] == square:
            return piece
    return None

# Seleccionar movimientos válidos
def get_valid_moves(piece):
    """
    Retorna los movimientos válidos de una pieza
    """
    valid_moves = []
    
    for row in range(ROWS):
        for col in range(COLS):
            target_pos = (row, col)
            if is_valid_move(piece, target_pos):
                valid_moves.append(target_pos)
    return valid_moves  

# Seleccionar si un movimiento es válido
def is_valid_move(piece, target_pos):
    """
    Verifica si el movimiento es válido.
    Considera las reglas de movimiento de Arimaa y el límite de movimientos.
    """
    
    current_row, current_col = piece['position']
    target_row, target_col = target_pos

    # No se puede mover a una casilla fuera del tablero
    if target_row < 0 or target_row >= ROWS or target_col < 0 or target_col >= COLS:
        return False
    
    # No se puede mover en diagonal
    if target_row != current_row and target_col != current_col:
        return False
    # No se puede mover a la misma casilla
    if target_pos == piece['position']:
        return False
    
    # Conejos no pueden retroceder
    if piece['type'] == 'rabbit':
        if piece['color'] == 'gold' and target_row > current_row:
            return False
        if piece['color'] == 'silver' and target_row < current_row:
            return False
        
    # No se puede mover más de 1 casilla en cualquier dirección
    if abs(target_row - current_row) > 1 or abs(target_col - current_col) > 1:
        return False
    
    # No se puede mover a una casilla ocupada por una pieza del mismo color
    for p in pieces:
        if p['position'] == target_pos and p['color'] == piece['color']:
            return False
        
    # No se puede mover a una casilla ocupada por una pieza de mayor igual valor
    for p in pieces:
        if p['position'] == target_pos and p['value'] >= piece['value']:
            return False

    # No se puede mover si en la posición actual tiene alrededor una pieza de otro color con valor mayor y no tiene cerca una pieza del mismo color 
    for p in pieces:
        adjacent_positions = [
            (current_row - 1, current_col),
            (current_row + 1, current_col),
            (current_row, current_col - 1),
            (current_row, current_col + 1)
        ]
        if p['position'] in adjacent_positions and p['color'] != piece['color'] and p['value'] > piece['value']:
            same_color_pieces = [p for p in pieces if p['position'] in adjacent_positions and p['color'] == piece['color']]
            if not same_color_pieces:
                return False
            
    # No se puede mover a una casilla trampa si no tiene piezas del mismo color alrededor de la trampa que no sea la misma pieza
    for trap_pos in TRAP_POSITIONS:
        if target_pos == trap_pos:
            trap_row, trap_col = trap_pos
            adjacent_positions = [
                (trap_row - 1, trap_col),
                (trap_row + 1, trap_col),
                (trap_row, trap_col - 1),
                (trap_row, trap_col + 1)
            ]
            adjacent_pieces = [p for p in pieces if p['position'] in adjacent_positions]
            same_color_pieces = [p for p in adjacent_pieces if p['color'] == piece['color']]
            if len(same_color_pieces) <= 1:
                return False

    # Se puede mover a una casilla donde este una pieza de otro color con valor menor y esta tenga donde moverse los conejos pueden retroceder
    for p in pieces:
        if p['position'] == target_pos and p['color'] != piece['color'] and p['value'] < piece['value']:
            if get_valid_moves(p):
                return True
            else:
                return False
            
    return True

# Mover una pieza           
def move_piece(piece, pos):
    """
    Mueve la pieza a la nueva posición.
    """
    
    #reemplazar la posición de la pieza
    piece['position'] = pos

    # Actualizar la lista de piezas
    pieces.remove(piece)
    pieces.append(piece)

# Seleccionar piezas válidas para empujar o tirar
def get_valid_push_pull_pieces(selected_piece, moves):
    """
    Retorna las casillas donde hay piezas que se pueden empujar o tirar.
    """
    valid_push_pull = []
    for row in range(ROWS):
        for col in range(COLS):
            target_pos = (row, col)
            if is_valid_push_pull_pieces(selected_piece, target_pos, moves):
                valid_push_pull.append(target_pos)
    return valid_push_pull

# Seleccionar si una pieza es válida para empujar o tirar
def is_valid_push_pull_pieces(selected_piece, target_pos, moves):
    """
    Verifica si existe una pieza que se puede empujar o tirar.
    """
    
    current_row, current_col = selected_piece['position']

    enemy_piece= get_piece_from_square(target_pos)
    
    # Si no hay pieza en la posición no se puede empujar o tirar
    if enemy_piece:
        target_row, target_col = enemy_piece['position']
        
        # No se puede empujar o tirar si tengo menos de 2 movimientos
        if moves > 2:
            return False
        
        # Si la pieza está en diagonal no es valida para empujar
        if target_row != current_row and target_col != current_col:
            return False
        
        # Si la pieza está a mas de una casilla de distancia en las 4 direcciones no es valida para empujar
        if abs(target_row - current_row) > 1 or abs(target_col - current_col) > 1:
            return False
        
        # No se puede empujar o tirar a una casilla ocupada por una pieza del mismo color
        if selected_piece['color'] == enemy_piece['color']:
            return False
        
        # No se puede empujar o tirar a una casilla ocupada por una pieza de mayor igual valor
        if enemy_piece['value'] >= selected_piece['value']:
            return False
         
        # No se puede empujar o tirar si tengo una pieza enemiga alrededor mio con valor mayor
        for p in pieces:
            adjacent_positions = [
                (current_row - 1, current_col),
                (current_row + 1, current_col),
                (current_row, current_col - 1),
                (current_row, current_col + 1)
            ]
            if p['position'] in adjacent_positions and p['color'] != selected_piece['color'] and p['value'] > selected_piece['value']:
                return False
          
        # No se puede empujar o tirar si no tengo espacio para moverme o si la pieza enemiga no tiene espacio para moverse
        adjacent_positions = get_valid_push_pull(selected_piece, enemy_piece)
        if not adjacent_positions:
            return False
        
        return True
    else:
        return False

# Seleccionar casillas válidas para empujar o tirar
def get_valid_push_pull(selected_piece, enemy_piece):
    """
    Retorna las casillas donde se puede empujar o tirar una pieza.
    """
    valid_push_pull = []
    
    for row in range(ROWS):
        for col in range(COLS):
            target_pos = (row, col)
            if is_valid_push_pull(selected_piece, enemy_piece, target_pos):
                valid_push_pull.append(target_pos)
    return valid_push_pull

# Seleccionar si un empuje o tirón es válido
def is_valid_push_pull(selected_piece,enemy_piece, target_pos):
    """
    Verifica si se puede empujar o tirar una pieza.
    """
    
    current_row, current_col = selected_piece['position']

    enemy_row, enemy_col = enemy_piece['position']

    target_row, target_col = target_pos
    
    # Si la posición está en diagonal no es valida para empujar
    if target_row != current_row and target_col != current_col and target_row != enemy_row and target_col != enemy_col:
        return False

    # si la posición está a mas de una casilla de distancia mio no es valida para empujar
    if abs(target_row - current_row) > 1 or abs(target_col - current_col) > 1:
        if abs(target_row - enemy_row) > 1 or abs(target_col - enemy_col) > 1:
            return False
        
    if abs(target_row - enemy_row) > 1 or abs(target_col - enemy_col) > 1:
        if abs(target_row - current_row) > 1 or abs(target_col - current_col) > 1:
            return False
    

    # No se puede empujar o tirar a una casilla ocupada 
    for p in pieces:
        if p['position'] == target_pos:
            return False
    
    return True

# Mover una pieza empujando o tirando
def move_piece_push_pull(selected_piece, enemy_piece, pos):
    """
    Mueve la pieza a la nueva posición.
    """
    if is_valid_push_pull(selected_piece, enemy_piece, pos):
        #si la nueva posición arriba, abajo, derecha o izquierda de la pieza enemiga
        if abs(enemy_piece['position'][0] - pos[0]) == 1 and abs(enemy_piece['position'][1] - pos[1]) == 0 or abs(enemy_piece['position'][0] - pos[0]) == 0 and abs(enemy_piece['position'][1] - pos[1]) == 1:
        
            #reemplazar la posición de la aliada
            selected_piece['position'] = enemy_piece['position']

            #reemplazar la posición de la pieza enemiga
            enemy_piece['position'] = pos
            
        #si la nueva posición arriba, abajo, derecha o izquierda de la pieza aliada
        elif abs(selected_piece['position'][0] - pos[0]) == 1 and abs(selected_piece['position'][1] - pos[1]) == 0 or abs(selected_piece['position'][0] - pos[0]) == 0 and abs(selected_piece['position'][1] - pos[1]) == 1:
    
                #reemplazar la posición de la pieza enemiga
                enemy_piece['position'] = selected_piece['position']

                #reemplazar la posición de la aliada
                selected_piece['position'] = pos
    else:
        print("No puedes mover la pieza enemiga a esa casilla.")
        return None

    # Actualizar la lista de piezas
    pieces.remove(enemy_piece)
    pieces.append(enemy_piece)

    # Actualizar la lista de piezas
    pieces.remove(selected_piece)
    pieces.append(selected_piece)
    
    return pieces

# Verificar si una pieza ha sido eliminada
def eliminated_piece():
    """
    Verifica si una pieza ha sido eliminada.
    """
    for piece in pieces:
        # Si la pieza está en una casilla trampa y no tiene piezas del mismo color alrededor
        if piece['position'] in TRAP_POSITIONS:
            trap_row, trap_col = piece['position']
            adjacent_positions = [
                (trap_row - 1, trap_col),
                (trap_row + 1, trap_col),
                (trap_row, trap_col - 1),
                (trap_row, trap_col + 1)
            ]
            same_color_pieces = [p for p in pieces if p['position'] in adjacent_positions and p['color'] == piece['color']]
            if not same_color_pieces:
                pieces.remove(piece)

# Cambiar de turno
def change_turn(current_player, moves, old_pieces):
    """
    Cambia el turno de los jugadores.
    """
    # Si no se han realizado al menos 1 movimiento, no se puede cambiar de turno
    if moves == 0:
        print("Debes realizar al menos un movimiento.")
        return current_player, moves
    
    # Si todas las piezas siguen en el mismo lugar, no se puede cambiar de turno
    if pieces == old_pieces:
        print("Las piezas no pueden quedar igual que al inicio.")
        return current_player, moves
    
    # Cambiar de turno
    if current_player == 'gold':
        current_player = 'silver'
        moves = 0
    else:
        current_player = 'gold'
        moves = 0

    return current_player, moves

def end_turn(current_player, moves, max_moves):
    """
    Termina el turno del jugador actual.
    """
    if moves == max_moves:

        if current_player == 'gold':
            current_player = 'silver'
            moves = 0
        else:
            current_player = 'gold'
            moves = 0

    return current_player, moves

# Obtneer las piezas actuales
def get_pieces():
    """
    Retorna las piezas iniciales.
    """
    return pieces

# Obtener el ganador
def win_condition(winner):
    """
    Verifica si hay un ganador.
    """
    # Si un conejo llega al lado opuesto del tablero, el jugador gana
    for piece in pieces:
        if piece['type'] == 'rabbit':
            if piece['position'][0] == 7 and piece['color'] == 'silver':
                winner = piece['color']
            if piece['position'][0] == 0 and piece['color'] == 'gold':
                winner = piece['color']

    # Si un jugador no tiene conejos, pierde
    gold_rabbits = [piece for piece in pieces if piece['type'] == 'rabbit' and piece['color'] == 'gold']
    silver_rabbits = [piece for piece in pieces if piece['type'] == 'rabbit' and piece['color'] == 'silver']

    if not gold_rabbits:
        winner = 'silver'
    if not silver_rabbits:
        winner = 'gold'

    # Si un jugador no tiene movimientos válidos en ninguna de sus piezas, pierde
    valid_moves_gold = []
    valid_moves_silver = []
    for piece in pieces:
        if piece['color'] == 'gold':
            valid_moves_gold += get_valid_moves(piece)
        if piece['color'] == 'silver':
            valid_moves_silver += get_valid_moves(piece)

    if not valid_moves_gold:
        winner = 'silver'
    if not valid_moves_silver:
        winner = 'gold'

    return winner