import pygame

# Configuraciones de pantalla
ROWS = 8
COLS = 8
SQUARE_SIZE = 100
SCREEN_WIDTH = COLS * SQUARE_SIZE 
SCREEN_HEIGHT = ROWS * SQUARE_SIZE

# Colores
light_purple = (56,41,66)
dark_purple = (35,34,43)
TRAP_COLOR = (0, 0, 0)  # Negro para las casillas trampa
BACKGROUND_COLOR = (255, 255, 255)  # Blanco

# Posiciones de trampas
TRAP_POSITIONS = [
    (2, 2), (2, 5), 
    (5, 2), (5, 5)
]

def get_pieces():
    pieces = [
        # Piezas doradas
        {"type": "rabbit", "color": "gold", "position": (7, 0), "image_path": "assets/golden_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "gold", "position": (7, 1), "image_path": "assets/golden_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "gold", "position": (7, 2), "image_path": "assets/golden_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "gold", "position": (7, 3), "image_path": "assets/golden_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "gold", "position": (7, 4), "image_path": "assets/golden_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "gold", "position": (7, 5), "image_path": "assets/golden_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "gold", "position": (7, 6), "image_path": "assets/golden_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "gold", "position": (7, 7), "image_path": "assets/golden_Rabit.png", "value": 1},
        {"type": "cat", "color": "gold", "position": (6, 0), "image_path": "assets/golden_Cat.png", "value": 3},
        {"type": "dog", "color": "gold", "position": (6, 1), "image_path": "assets/golden_Dog.png", "value": 5},
        {"type": "horse", "color": "gold", "position": (6, 2), "image_path": "assets/golden_Horse.png", "value": 7},
        {"type": "camel", "color": "gold", "position": (6, 3), "image_path": "assets/golden_Camel.png", "value": 9},
        {"type": "elephant", "color": "gold", "position": (6, 4), "image_path": "assets/golden_Elephant.png", "value": 11},
        {"type": "horse", "color": "gold", "position": (6, 5), "image_path": "assets/golden_Horse.png", "value": 7},
        {"type": "dog", "color": "gold", "position": (6, 6), "image_path": "assets/golden_Dog.png", "value": 5},
        {"type": "cat", "color": "gold", "position": (6, 7), "image_path": "assets/golden_Cat.png", "value": 3},

        # Piezas plateadas
        {"type": "rabbit", "color": "silver", "position": (0, 0), "image_path": "assets/silver_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "silver", "position": (0, 1), "image_path": "assets/silver_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "silver", "position": (0, 2), "image_path": "assets/silver_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "silver", "position": (0, 3), "image_path": "assets/silver_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "silver", "position": (0, 4), "image_path": "assets/silver_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "silver", "position": (0, 5), "image_path": "assets/silver_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "silver", "position": (0, 6), "image_path": "assets/silver_Rabit.png", "value": 1},
        {"type": "rabbit", "color": "silver", "position": (0, 7), "image_path": "assets/silver_Rabit.png", "value": 1},
        {"type": "cat", "color": "silver", "position": (1, 0), "image_path": "assets/silver_Cat.png", "value": 3},
        {"type": "dog", "color": "silver", "position": (1, 1), "image_path": "assets/silver_Dog.png", "value": 5},
        {"type": "horse", "color": "silver", "position": (1, 2), "image_path": "assets/silver_Horse.png", "value": 7},
        {"type": "camel", "color": "silver", "position": (1, 3), "image_path": "assets/silver_Camel.png", "value": 9},
        {"type": "elephant", "color": "silver", "position": (1, 4), "image_path": "assets/silver_Elephant.png", "value": 11},
        {"type": "horse", "color": "silver", "position": (1, 5), "image_path": "assets/silver_Horse.png", "value": 7},
        {"type": "dog", "color": "silver", "position": (1, 6), "image_path": "assets/silver_Dog.png", "value": 5},
        {"type": "cat", "color": "silver", "position": (1, 7), "image_path": "assets/silver_Cat.png", "value": 3},
    ]
    return pieces

def get_board():
    board = [[None for _ in range(COLS)] for _ in range(ROWS)]
    return board