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
cameraX=0
cameraY=0
ACCEL = 0.001
tile_width = 32
tile_height = 32
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
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_RIGHT:
            cameraX = cameraX + 32
        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_LEFT:
            cameraX = cameraX - 32   
    # we need to investiage this chunk
    delay = (pygame.time.get_ticks() - frame_time)
    if (delay == 0):
        delay = 1
            
    # simulation stuff goes here 
    #print player.name # this is how you print out attributes of objects from tmx file
    
    # draw the background
    screen.fill( (135, 206 , 250) )

    # draw all tiles in world layer to screen and flip
    world = tiled_map.get_layer_by_name("world")

    # camera controls
    #cameraX = cameraX+1
    #cameraY = cameraY+1
    
    for t_x, t_y, tile_image in world.tiles():
        screen.blit(tile_image, (t_x * tile_width - cameraX, t_y * tile_height + cameraY))

    # draw the player (yellow box is player place-holder for now)
    screen.blit(player.image, (player.x - cameraX ,player.y + cameraY ))    
    
    pygame.display.flip()
