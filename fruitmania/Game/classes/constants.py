import pygame

# все константы
W = 1700
H = 900
SCREEN = pygame.display.set_mode((W, H))
PLAYER_SIZE = 200
PLAYER_SPEED = 12

FRUITS_SIZE = 70
BANANA_SPEED = 5
BOMB_SPEED = 6
STRAWBERRY_SPEED = 8
ORANGE_SPEED = 5.5

FRUITS_TIMER = 2500
CONTACT_DISTANCE = 80
MAX_SCORE_FOR_WIN = 999

DATA_FILE = '../registered_player/players_data.txt'
LAST_PLAYER_FILE = '../registered_player/last_player.txt'
