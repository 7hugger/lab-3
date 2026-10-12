import pygame
from pygame import Surface
import os

pygame.mixer.init()
size = (500,500)
# Доска
CHESS_BOARD_IMG: Surface = pygame.image.load(os.path.join("Assets", "blue.png"))
CHESS_BOARD: Surface = pygame.transform.scale(CHESS_BOARD_IMG, (600, 600))

# Фигуры
WHITE_PAWN: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "wP.png"))
WHITE_PAWN: Surface = pygame.transform.smoothscale(WHITE_PAWN, size=size)
WHITE_ROOK: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "wR.png"))
WHITE_ROOK: Surface = pygame.transform.smoothscale(WHITE_ROOK, size=(60,60))
WHITE_KNIGHT: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "wN.png"))
WHITE_KNIGHT: Surface = pygame.transform.smoothscale(WHITE_KNIGHT, size=(60,60))
WHITE_QUEEN: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "wQ.png"))
WHITE_QUEEN: Surface = pygame.transform.smoothscale(WHITE_QUEEN, size=(60,60))
WB: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "wB.png")) # фигура слона справа
WB: Surface = pygame.transform.smoothscale(WB, size=size)

WHITE_BISHOP: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "wB.png"))
WHITE_BISHOP: Surface = pygame.transform.scale(WHITE_BISHOP, size=(60,60))
WHITE_KING: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "wK.png"))
WHITE_KING: Surface = pygame.transform.smoothscale(WHITE_KING, size=size)


BLACK_PAWN: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "bp.png"))
BLACK_PAWN: Surface = pygame.transform.smoothscale(BLACK_PAWN, size=size)
BLACK_ROOK: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "bR.png"))
BLACK_ROOK: Surface = pygame.transform.smoothscale(BLACK_ROOK, size=size)
BLACK_KNIGHT: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "bN.png"))
BLACK_KNIGHT: Surface = pygame.transform.smoothscale(BLACK_KNIGHT, size=size)
BLACK_BISHOP: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "bB.png"))
BLACK_BISHOP: Surface = pygame.transform.smoothscale(BLACK_BISHOP, size=size)
BLACK_QUEEN: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "bQ.png"))
BLACK_QUEEN: Surface = pygame.transform.smoothscale(BLACK_QUEEN, size=size)
BLACK_KING: Surface = pygame.image.load(os.path.join("Assets\chesspieces", "bK.png"))
BLACK_KING: Surface = pygame.transform.smoothscale(BLACK_KING, size=size)

# Звуки
MOVE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Move.wav"))