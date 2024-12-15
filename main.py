import pygame
from config import * 
import draw
import game_controller

#Inicializar pygame
pygame.init()

# Crear pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arimaa")

def draw_tool(screen, selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner):
    draw.draw_board(screen)
    draw.draw_pieces(screen)
    draw.draw_valid_moves_board(screen, selected_piece, piece_attacked, current_player, moves, max_moves)
    draw.draw_winner(screen, winner)
    return board


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

    while run:
        
        clock.tick(60)

        

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            # Evento de teclado espacio para pasar turno
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_player, moves = game_controller.change_turn(current_player, moves, old_pieces)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner, old_pieces= game_controller.handle_click(screen, mouse_pos, selected_piece, piece_attacked, current_player, moves, max_moves, winner, old_pieces)


        # Herramienta de dibujo
        board = draw_tool(screen, selected_piece, piece_attacked, mouse_pos, current_player, moves, max_moves, winner)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
                