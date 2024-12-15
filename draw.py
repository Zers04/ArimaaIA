import pygame
from config import *
import game_controller 

# Dibujar el tablero
def draw_board(screen):
    for row in range(ROWS):
        for col in range(COLS):
            # Alternar colores según la posición
            color = light_brown if (row + col) % 2 == 0 else dark_brown
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            
            # Dibujar casilla
            pygame.draw.rect(screen, color, rect)
            
            # Dibujar reborde negro
            pygame.draw.rect(screen, (0, 0, 0), rect, width=2)

            # Dibujar trampas en negro si la posición coincide
            if (row, col) in TRAP_POSITIONS:
                trap_rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, TRAP_COLOR, trap_rect)

# Dibujar las piezas
def draw_pieces(screen):
    """
    Dibuja las piezas en la pantalla
    """
    for piece in pieces:
        row, col = piece["position"]
        image = pygame.image.load(piece["image_path"])
        image = pygame.transform.scale(image, (80, 80))
        x = col * SQUARE_SIZE + (SQUARE_SIZE - 80) // 2
        y = row * SQUARE_SIZE + (SQUARE_SIZE - 80) // 2
        screen.blit(image, (x, y))

#Dibuja los movimientos validos
def draw_valid_moves_board(screen, selected_piece, piece_attacked, current_player, moves, max_moves):

    if piece_attacked:
        draw_push_pull_posibility(screen, selected_piece, piece_attacked)

    elif selected_piece:
        draw_selected_piece(screen, selected_piece)

        draw_valid_moves(screen, selected_piece)

        draw_valid_push_pull_pieces(screen, selected_piece, moves)
        
# Seleccionar una pieza según su posición
def draw_selected_piece(screen, piece):
    """
    Dibuja la pieza seleccionada en la pantalla.
    """
    if piece:
        row, col = piece["position"]

        # Fondo semi-transparente
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(( 224, 163, 255, 100))  # Verde transparente
        screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

        # Borde visible
        pygame.draw.rect(
            screen,
            (224, 163, 255),  # Verde
            (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            width=4
        )
        
# Dibujar movimientos válidos
def draw_valid_moves(screen, selected_piece):
    """
    Dibuja los movimientos válidos en la pantalla.
    """
    # Obtener movimientos válidos
    valid_moves = game_controller.get_valid_moves(selected_piece)

    # Dibujar un rectángulo verde alrededor de las casillas válidas
    for move in valid_moves:
        pygame.draw.rect(screen, (224, 163, 255), (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=4)

# Dibujar movimientos válidos de empujar o tirar
def draw_valid_push_pull_pieces(screen, selected_piece, moves):
    """
    Dibuja los movimientos válidos de empujar o tirar en la pantalla.
    """
    if selected_piece:
        valid_push_pulls = game_controller.get_valid_push_pull_pieces(selected_piece, moves)
        for push_pull in valid_push_pulls:
            pygame.draw.rect(screen, (166, 227, 245), (push_pull[1] * SQUARE_SIZE, push_pull[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=4)

def draw_push_pull_posibility(screen, selected_piece, enemy_piece):
    """
    Dibuja el movimiento de empujar o tirar en la pantalla.
    """

    valid_push_pull = game_controller.get_valid_push_pull(selected_piece, enemy_piece)
    if valid_push_pull:
        # Dibujar las casillas involucradas en el movimiento
        for p in valid_push_pull:
            pygame.draw.rect(screen, (255,255,255), (p[1] * SQUARE_SIZE, p[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=4)

def draw_winner(screen, winner):
    """
    Dibuja el mensaje de ganador en la pantalla.
    """
    if winner:
        font = pygame.font.Font(None, 50)
        if winner == 'gold':  
            text = font.render(f"El ganador es el humano :)", True, (255, 255, 255))
        if winner == 'silver':
            text = font.render(f"El ganador es la maquina :(", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)

            