import pygame
import sys
import math
import pytmx
from utils import vector2
from utils import sprite2
from pytmx.util_pygame import load_pygame
from pygame import Rect

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
vy = 2
cameraX=0
cameraY=0
ACCEL = 0.5
GRAV = 3
tile_width = 32
tile_height = 32
frame_time = pygame.time.get_ticks()
player = tiled_map.get_object_by_name("player_1")
#main_floor = tiled_map.get_object_by_name("main_floor")
world = tiled_map.get_layer_by_name("world") #this was in main loop, nooooooooooooooooo, but I have saved it!
dt = 0.0 # delta time
delay=0.0
previousFrameTime = 0.0
floor1 = tiled_map.get_object_by_name("floor1")
floors = tiled_map.get_layer_by_name("Ground")
stairs = tiled_map.get_layer_by_name("Stairs")
floorBoxes = list()
stairBoxes = list()
player.box = Rect(player.x, player.y, player.width, player.height)
isgrounded = False
isgroundedStair = False

for obj in floors:
    box = Rect(obj.points[0][0], obj.points[0][1], obj.points[1][0] - obj.points[0][0], obj.points[3][1] - obj.points[0][1])
    floorBoxes.append(box)
for obj in stairs:
    box = Rect(obj.points[0][0], obj.points[0][1], obj.points[1][0] - obj.points[0][0], obj.points[3][1] - obj.points[0][1])
    stairBoxes.append(box)
    
while True:
    # time of current frame
    #print pygame.time.get_ticks()
    
    #print player.box.y
    # get user events
    pygame.event.pump()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT or evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
            
    isgrounded=False
    for fbox in floorBoxes:
        if player.box.colliderect(fbox):
            isgrounded=True
            
    isgroundedStair=False
    for fbox in floorBoxes:
        if player.box.colliderect(fbox):
            isgroundedStair=True

    player.box.y = player.box.y + vy
    player.box.x = player.box.x + vx
    
    if vx > 0:
        vx = vx * ACCEL * dt
    if vx < 0:
        vx = vx * ACCEL * dt

    
    
    if isgrounded:
        vy = 0
    if isgroundedStair:
        vy = 0
    else:
        vy = vy + GRAV * dt
    
        #move the camera
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        vx = -1
        #cameraX = cameraX - 5 * 32 * dt
    if keys[pygame.K_RIGHT]:
        vx = 1
        #cameraX = cameraX + 5 * 32 * dt
    if keys[pygame.K_UP]:
        vy = -.1
        #cameraY = cameraY + 5 * 32 * dt
    #if keys[pygame.K_DOWN]:
        #cameraY = cameraY - 5 * 32 * dt
    cameraX = player.box.x - 1280/2
    cameraY = -player.box.y + 640/2
        
    # we need to investiage this chunk
    start_time = pygame.time.get_ticks()
    
    delay = (pygame.time.get_ticks() - start_time)
    '''
    if (delay == 0):
        delay = 1
    '''  
    # simulation stuff goes here 
    #print player.name # this is how you print out attributes of objects from tmx file
    
    # draw the background
    screen.fill( (135, 206 , 250) )

    # draw all tiles in world layer to screen and flip

    # camera controls
    #cameraX = cameraX+1
    #cameraY = cameraY+1
    
    for t_x, t_y, tile_image in world.tiles():
        screen.blit(tile_image, (t_x * tile_width - cameraX, t_y * tile_height + cameraY))

    # draw the player (yellow box is player place-holder for now)
    screen.blit(player.image, (player.box.x - cameraX, player.box.y + cameraY ))    
    
    pygame.display.flip()
    dt = (start_time - previousFrameTime) / 1000.0
    previousFrameTime = start_time
