import pygame
import sys
import math
import pytmx
from utils import vector2
from utils import sprite2
from pytmx.util_pygame import load_pygame
from pygame import Rect
from player_movement import player_movement

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
vx = 0.001
vy = 0.001
cameraX=0
cameraY=0
ACCEL = 0.5
GRAV = 15.000
SPEED = 2.0
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
ground_blocks = [floors]
floorBoxes = list()
stairBoxes = list()
player.box = Rect(player.x, player.y, player.width, player.height)
isgrounded = False
isgroundedStair = False
player_height = 32
player_width = 32
player_movement = player_movement()
for obj in floors:
    box = Rect(obj.points[0][0], obj.points[0][1], obj.points[1][0] - obj.points[0][0], obj.points[3][1] - obj.points[0][1])
    floorBoxes.append(box)
for obj in stairs:
    box = Rect(obj.points[0][0], obj.points[0][1], obj.points[1][0] - obj.points[0][0], obj.points[3][1] - obj.points[0][1])
    stairBoxes.append(box)

    #player.box.y = float(player.box.y)
    #player.box.y = player.box.y + 0.16

temp_num = 5
if(True ^ True):
    print "that is true"
else:
    print "that is not true"

while True:
    # time of current frame
    start_time = pygame.time.get_ticks()
    
    #print player.box.y
    # get user events
    pygame.event.pump()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT or evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
            
    #vy = vy + GRAV * dt
    # get keys pressed
    
    '''
    isgrounded=False
    for fbox in floorBoxes:
        if player.box.colliderect(fbox):
            isgrounded=True
            
    isgroundedStair=False
    for fbox in floorBoxes:
        if player.box.colliderect(fbox):
            isgroundedStair=True
    '''
    
    #                       #
    # update player speed   #
    #                       #
    vx,vy = player_movement.update_velocities(SPEED, dt, GRAV, vx, vy, isgrounded )

    #                               #
    # Check for ground collisions   #
    #                               #
    player.x, player.y, vx, vy, isgrounded = player_movement.check_ground(ground_blocks, player.x, player.y, player_width, player_height, vx, vy, tile_height, tile_width, SPEED, dt)

    #print dogs
    #print player.box.y
    #player.y = player.y + vy
    #player.x = player.x + vx

    '''
    if vx > 0:
        vx = vx * ACCEL * dt
    if vx < 0:
        vx = vx * ACCEL * dt

    
    
    if isgrounded:
        vy = 0
    if isgroundedStair:
        vy = 0
    -------------------------------------
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
        
    # we need to investiage this chunk
    start_time = pygame.time.get_ticks()
    '''

    #move the camera  
    cameraX = player.x - 1280/2
    cameraY = -player.y + 640/2

    #delay = (pygame.time.get_ticks() - start_time)
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
    screen.blit(player.image, (player.x - cameraX, player.y + cameraY ))    
    
    pygame.display.flip()
    dt = (start_time - previousFrameTime) / 1000.0
    previousFrameTime = start_time
    if (dt > 0.02):
        dt = 0.02
    #print dt
    
