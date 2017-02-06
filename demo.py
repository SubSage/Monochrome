import pygame
import sys
import math
import pytmx
from utils import vector2
from utils import sprite2
from pytmx.util_pygame import load_pygame

# setup goes here
pygame.init()
screen = pygame.display.set_mode((1280,640))
pygame.display.set_caption( "Demo" )
tiled_map = load_pygame('map_1.tmx')
tiles_x = 40
tiles_y = 20
layer = 0
t_x = 0
t_y = 0
x = 10
y = 10
vx = 0
vy = 0
ACCEL = 0.001
frame_time = pygame.time.get_ticks()

while True:

    # time of current frame
    frame_time = pygame.time.get_ticks()
    
    # get user events
    pygame.event.pump()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
            
    delay = (pygame.time.get_ticks() - frame_time)
    if (delay == 0):
        delay = 1
            
    # simulation stuff goes here 
    
    # draw all tiles in layers to screen and flip
    screen.fill( (255,255,255) )
    for layer in tiled_map.layers:
        for t_x, t_y, tile_image in layer.tiles():
            screen.blit(tile_image, (t_x * 32, t_y * 32))

    pygame.display.flip()
