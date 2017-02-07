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
SPEED = 0.2

frame_time = pygame.time.get_ticks()
player = tiled_map.get_object_by_name("player_1")
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
            inputX = 0
        #code for movement
        """    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            inputX -= 1
        if keys[pygame.K_d]:
            inputX += 1

        if inputX != 0:
            player.x = inputX * SPEED
        elif player.x > 0:
            player.x = player.x - 0.001 * delta
            if player.x < 0:
                player.x = 0
        elif player.x < 0:
            player.x = player.x + 0.001 * delta
            if player.x > 0:
                player.x = 0

        #code for jump
        if keys[pygame.K_w]:
            player.y = -0.3

        if player.y > 
        
        """
    delay = (pygame.time.get_ticks() - frame_time)
    if (delay == 0):
        delay = 1
            
    # simulation stuff goes here 
    
    
    # draw the background
    screen.fill( (135, 206 , 250) )

    # draw all tiles in world layer to screen and flip
    world = tiled_map.get_layer_by_name("world")
    for t_x, t_y, tile_image in world.tiles():
        screen.blit(tile_image, (t_x * 32, t_y * 32))

    # draw the player (yellow box is player place-holder for now)
    screen.blit(player.image, (player.x,player.y))    
    
    pygame.display.flip()
