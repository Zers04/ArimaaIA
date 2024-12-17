import pygame
from config import ROWS, COLS, SQUARE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, light_purple, dark_purple, TRAP_COLOR, TRAP_POSITIONS
import game_controller 

# Obtener configuraciones

# Dibujar el tablero
def draw_board(screen, board):
    for row in range(ROWS):
        for col in range(COLS):
            # Alternar colores según la posición
            color = light_purple if (row + col) % 2 == 0 else dark_purple
            rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            
            # Dibujar casilla
            pygame.draw.rect(screen, color, rect)
            
            # Dibujar reborde negro
            pygame.draw.rect(screen, (0, 0, 0), rect, width=2)

            # Dibujar trampas en negro si la posición coincide
            if (row, col) in TRAP_POSITIONS:
                trap_rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, TRAP_COLOR, trap_rect)
    
    return board

# Dibujar las piezas
def draw_pieces(screen, pieces):
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
    
    return pieces

#Dibuja los movimientos validos
def draw_valid_moves_board(screen, selected_piece, piece_attacked, current_player, moves, max_moves, pieces):

    if piece_attacked:
        draw_push_pull_posibility(screen, selected_piece, piece_attacked, pieces)

    elif selected_piece:
        draw_selected_piece(screen, selected_piece)

        draw_valid_moves(screen, selected_piece, pieces)

        draw_valid_push_pull_pieces(screen, selected_piece, moves, pieces)
        
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
def draw_valid_moves(screen, selected_piece, pieces):
    """
    Dibuja los movimientos válidos en la pantalla.
    """
    # Obtener movimientos válidos
    valid_moves = game_controller.get_valid_moves(selected_piece, pieces)

    # Dibujar un rectángulo verde alrededor de las casillas válidas
    for move in valid_moves:
        pygame.draw.rect(screen, (224, 163, 255), (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=4)

# Dibujar movimientos válidos de empujar o tirar
def draw_valid_push_pull_pieces(screen, selected_piece, moves, pieces):
    """
    Dibuja los movimientos válidos de empujar o tirar en la pantalla.
    """
    if selected_piece:
        valid_push_pulls = game_controller.get_valid_push_pull_pieces(selected_piece, moves, pieces)
        for push_pull in valid_push_pulls:
            pygame.draw.rect(screen, (166, 227, 245), (push_pull[1] * SQUARE_SIZE, push_pull[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=4)

# Dibujar la posibilidad de empujar o tirar
def draw_push_pull_posibility(screen, selected_piece, enemy_piece, pieces):
    """
    Dibuja el movimiento de empujar o tirar en la pantalla.
    """

    valid_push_pull = game_controller.get_valid_push_pull(selected_piece, enemy_piece, pieces)
    if valid_push_pull:
        # Dibujar las casillas involucradas en el movimiento
        for p in valid_push_pull:
            pygame.draw.rect(screen, (255,255,255), (p[1] * SQUARE_SIZE, p[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width=4)

# Dibujar el mensaje de ganador
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

# Dibujar el menú
def draw_menu(screen):
    """
    Dibuja el menú en la pantalla.
    
    :param screen: La superficie principal donde se dibuja.
    :param screen_width: Ancho de la pantalla.
    :param screen_height: Alto de la pantalla.
    """
    # Cargar y escalar la imagen de fondo
    background = pygame.image.load("assets/Menu.png")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background, (0, 0))

    # Configuración de fuente y colores
    font = pygame.font.Font(None, 36)
    text_color = (255, 255, 255)  # Blanco
    button_color = (255, 215, 0, 180)  # Dorado semi-transparente

    # Crear una superficie con canal alpha para transparencia
    button_surface = pygame.Surface((250, 75), pygame.SRCALPHA)

    # Lista de textos para los botones
    button_texts = ["Player vs Player", "Player vs Machine", "Machine vs Machine"]

    # Dibujar los botones con texto
    for i, text in enumerate(button_texts):
        # Crear la superficie del botón
        button_surface.fill((0, 0, 0, 0))  # Limpiar la superficie
        pygame.draw.rect(button_surface, button_color, (0, 0, 250, 75), border_radius=15)

        # Calcular posición del botón
        button_x = SCREEN_WIDTH // 2 - 125
        button_y = SCREEN_HEIGHT // 2 - 50 + i * 100

        # Blit del botón
        screen.blit(button_surface, (button_x, button_y))

        # Renderizar el texto
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(button_x + 125, button_y + 37))  # Centrar texto en el botón
        screen.blit(text_surface, text_rect)
