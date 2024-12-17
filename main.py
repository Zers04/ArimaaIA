import pygame
from config import * 
import draw
import game_controller
import ia_controller

#Inicializar pygame
pygame.init()

# Crear pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arimaa")

# Función para dibujar en pantalla
def draw_tool(screen, selected_piece, piece_attacked, current_player, moves, max_moves, winner, pieces, board, game_mode):
    if game_mode is None:
        draw.draw_menu(screen)
    else:
        draw.draw_board(screen, board)
        draw.draw_pieces(screen, pieces)
        draw.draw_valid_moves_board(screen, selected_piece, piece_attacked, current_player, moves, max_moves, pieces)
        draw.draw_winner(screen, winner)

def main():

    # Reloj para controlar la velocidad de actualización de la pantalla
    clock = pygame.time.Clock()

    # Bucle principal
    run = True 
    selected_piece = None # Variable para almacenar la pieza seleccionada
    piece_attacked = None # Variable para almacenar la pieza atacada
    winner = None # Variable para almacenar el ganador
    current_player = 'gold'  # Empieza el jugador dorado
    moves = 0  # Contador de movimientos
    max_moves = 4  # Número máximo de movimientos
    mouse_pos = None # Posición del mouse
    old_pieces = game_controller.get_pieces() # Piezas iniciales
    pieces = get_pieces() # Piezas actuales
    board = get_board() # Tablero
    game_mode = None # Modo de juego

    button_positions = [ # Posiciones
        (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 50, 250, 75),  # Player vs Player
        (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 50, 250, 75),  # Player vs Machine
        (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 150, 250, 75)  # Machine vs Machine
    ]

    while run:
        
        clock.tick(60)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            # casos para game_mode
            if game_mode == 'player vs player': # Modo jugador vs jugador
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        current_player, moves = game_controller.change_turn(current_player, moves, old_pieces, pieces)
                    if event.key == pygame.K_ESCAPE:
                        mouse_pos, selected_piece, piece_attacked, winner, game_mode = None, None, None, None, None
                        current_player = 'gold'
                        moves = 0
                        old_pieces = game_controller.get_pieces()
                        pieces = get_pieces()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner, old_pieces, pieces= game_controller.handle_click(screen, mouse_pos, selected_piece, piece_attacked, current_player, moves, max_moves, winner, old_pieces, pieces)


            if game_mode == 'player vs ia': # Modo jugador vs IA
                if current_player == 'gold':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            current_player, moves = game_controller.change_turn(current_player, moves, old_pieces, pieces)
                        if event.key == pygame.K_ESCAPE:
                            mouse_pos, selected_piece, piece_attacked, winner, game_mode = None, None, None, None, None
                            current_player = 'gold'
                            moves = 0
                            old_pieces = game_controller.get_pieces()
                            pieces = get_pieces()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner, old_pieces, pieces= game_controller.handle_click(screen, mouse_pos, selected_piece, piece_attacked, current_player, moves, max_moves, winner, old_pieces, pieces)           

                if current_player == 'silver':
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            mouse_pos, selected_piece, piece_attacked, winner, game_mode = None, None, None, None, None
                            current_player = 'gold'
                            moves = 0
                            old_pieces = get_pieces()
                            pieces = get_pieces()
                    else:

                        # Llamada a la IA
                        current_player, moves, max_moves, winner, pieces= ia_controller.play(screen, current_player, moves, max_moves, winner, pieces)


            if game_mode == 'ia vs ia': # Modo IA vs IA
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                            mouse_pos, selected_piece, piece_attacked, winner, game_mode = None, None, None, None, None
                            current_player = 'gold'
                            moves = 0
                            old_pieces = get_pieces()
                            pieces = get_pieces()
                else:
                    # Llamada a la IA
                    current_player, moves, max_moves, winner, pieces= ia_controller.play(screen, current_player, moves, max_moves, winner, pieces)

            elif game_mode is None: # Menú de selección de modo de juego

                 # Detectar clics del ratón
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos  # Coordenadas del clic

                    # Verificar en qué botón se hizo clic
                    for i, (x, y, width, height) in enumerate(button_positions):
                        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
                            if i == 0:
                                game_mode = 'player vs player'
                            elif i == 1:
                                game_mode = 'player vs ia'
                            elif i == 2:
                                game_mode = 'ia vs ia'
                            print(f"Seleccionado: {game_mode}")

        # Dibujar en pantalla
        draw_tool(screen, selected_piece, piece_attacked, current_player, moves, max_moves, winner, pieces, board, game_mode)

        # Actualizar pantalla
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
                