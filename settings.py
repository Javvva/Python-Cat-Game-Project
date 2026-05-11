import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Cat Game')
CAPTION = 60

PLAYER_START_X    = 80
PLAYER_START_Y    = 300   
PLAYER_GRAVITY    = 0     
PLAYER_JUMP_FORCE = -20   
GRAVITY_INCREMENT = 1     


FONT_PATH = 'assets/fonts/PixelType.ttf'
FONT_SIZE = 50
