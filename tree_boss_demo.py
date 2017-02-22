import pygame
import sys
import math
import pytmx
from utils import vector2
from utils import sprite2
from pytmx.util_pygame import load_pygame
from pygame import Rect
from player_movement import player_movement
from tree import tree
import random
# setup goes here
pygame.init()
tile_width = 128
tile_height = 128
screen = pygame.display.set_mode((1280,640))
pygame.display.set_caption( "TreeBoss" )
tiled_map = load_pygame('tree_boss.tmx')
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
SPEED = 1.8
frame_time = pygame.time.get_ticks()
player = tiled_map.get_object_by_name("player_1")
boss_heart = tiled_map.get_object_by_name("heart")
#main_floor = tiled_map.get_object_by_name("main_floor")
#world = tiled_map.get_layer_by_name("world") #this was in main loop, nooooooooooooooooo, but I have saved it!
dt = 0.0 # delta time
delay=0.0
previousFrameTime = 0.0
#floor1 = tiled_map.get_object_by_name("floor1")
#floors = tiled_map.get_layer_by_name("Ground")
#stairs = tiled_map.get_layer_by_name("Stairs")
dirt = tiled_map.get_layer_by_name("dirt")
tree_tiles = tiled_map.get_layer_by_name("tree")
ground = tiled_map.get_layer_by_name("ground")
ground_blocks = [ground]
ground_blocks_rect = list()
boss_hitboxes = tiled_map.get_layer_by_name("hitboxes")
boss_hitboxes_rect = list()
floorBoxes = list()
stairBoxes = list()
player.box = Rect(player.x, player.y, player.width, player.height)
isgrounded = False
isgroundedStair = False
player_height = 155
player_width = 158
player_movement = player_movement()
roots = boss_hitboxes = tiled_map.get_layer_by_name("roots")
root_width = 128
tree_boss = tree(roots, root_width, boss_heart)
player_alive = True
boss_beaten = False
death_screen = pygame.image.load( "death_screen.jpg" ).convert()
win_screen = pygame.image.load( "win_screen.jpg" ).convert()
PUNCHING = False
#frame stuff for animation
flippic = False
frame = 0
frame_timer = 0
FRAME_TIME = .10
FRAME_CT = 6
Aheight = 0

player_image = pygame.image.load( "HMCF2.png" ).convert_alpha()
clip = pygame.Rect( 164 + 158*frame, Aheight * 154 , 160, 154 )
'''
for obj in floors:
    box = Rect(obj.points[0][0], obj.points[0][1], obj.points[1][0] - obj.points[0][0], obj.points[3][1] - obj.points[0][1])
    floorBoxes.append(box)
for obj in stairs:
    box = Rect(obj.points[0][0], obj.points[0][1], obj.points[1][0] - obj.points[0][0], obj.points[3][1] - obj.points[0][1])
    stairBoxes.append(box)
'''
for obj in ground:
     box = Rect(obj.x, obj.y, obj.width, obj.height)
     ground_blocks_rect.append(box)

for obj in boss_hitboxes:
     box = Rect(obj.x, obj.y, obj.width, obj.height)
     boss_hitboxes_rect.append(box)
   
    #player.box.y = float(player.box.y)
    #player.box.y = player.box.y + 0.16
'''
temp_num = 5
if(True ^ True):
    print "that is true"
else:
    print "that is not true"
'''
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

    # simulation stuff goes here            
    if(player_alive):
        if(boss_beaten):
            screen.blit(win_screen, (0,0))
            pygame.display.flip()
            print tree_boss.hp

        else:
            #                       #
            # update player speed   #
            #                       #
            vx,vy, PUNCHING = player_movement.update_velocities(SPEED, dt, GRAV, vx, vy, isgrounded )
                        #sprite controls
            
            mkeys = pygame.key.get_pressed()
            if ((mkeys[pygame.K_a])|(mkeys[pygame.K_LEFT])):
                 flippic = True
                 if frame == 0:
                      Aheight = 0
                      frame = 1
            if ((mkeys[pygame.K_d])|(mkeys[pygame.K_RIGHT])):
                 flippic =False
                 if frame == 0:
                      Aheight = 0
                      frame = 1
            if ((mkeys[pygame.K_w])|(mkeys[pygame.K_UP])):
                 None
            if ((mkeys[pygame.K_z])|(mkeys[pygame.K_SPACE])):
                 if frame == 0:
                      Aheight = 3
                      frame = 1
             
            #                               #
            # Check for ground collisions   #
            #                               #
            player.x, player.y, vx, vy, isgrounded = player_movement.check_ground(ground_blocks, player.x, player.y, player_width, player_height, vx, vy, tile_height, tile_width, SPEED, dt)

            #                   #
            # update tree stuff #
            #                   #
            root_attack = tree_boss.update(dt)

            #                                   #
            # check if player gets hit by roots #
            #                                   #
            if (tree_boss.root_attacking):
                 player_alive = tree_boss.root_collision(player, player_width, player_height, clip, player_image)

            #                                   #
            # check if player gets hits heart   #
            #                                   #
            
            if(PUNCHING):
                tree_boss.check_heart(player, player_width, player_height)

            if(tree_boss.hp < 1):
                boss_beaten = True
                
            #move the camera  
            cameraX = player.x - 1280/2
            cameraY = -player.y + 640/2

            # draw the background
            screen.fill( (48, 24 , 96) )

            # draw all dirt tiles
            for t_x, t_y, tile_image in dirt.tiles():
                screen.blit(tile_image, (t_x * tile_width - cameraX, t_y * tile_height + cameraY))

            # draw_tree [NOTE: this is slowing down the game]
            for t_x, t_y, tile_image in tree_tiles.tiles():
                screen.blit(tile_image, (t_x * tile_width - cameraX, t_y * tile_height + cameraY))

            # draw roots
            for root in tree.roots:
                screen.blit(root.image, (root.x - cameraX, root.y + cameraY))

            # draw the player
            #img = pygame.image.load( "ryu-640.png" ).convert_alpha()
            #clip = pygame.Rect( MARGIN+IMG_W*frame, 0, IMG_W, 151 )
            
            if frame != 0:
                 if frame_timer > FRAME_TIME:
                      frame_timer -= FRAME_TIME
                      frame = (frame + 1) % FRAME_CT
                 frame_timer += dt
            
            img = pygame.image.load( "HMCF.png" ).convert_alpha()
            clip = pygame.Rect( 164 + 158*frame, Aheight * 154 , 160, 154 )            
            
            #screen.blit(img, (22,0), area=clip, special_flags=pygame.BLEND_RGBA_MIN )
            #screen.blit(player.image, (player.x - cameraX, player.y + cameraY ))
            #print player.x
            #print player.y
            if flippic == False:
                 screen.blit(img, (player.x - cameraX, player.y + cameraY ),area = clip )
                 #print isgrounded
                 player_image = img

            else:
                 screen.blit(pygame.transform.flip(img, True, False), (player.x - cameraX, player.y + cameraY ),area = clip)
                 player_image = pygame.transform.flip(img, True, False)
                                                
            pygame.display.flip()
            dt = (start_time - previousFrameTime) / 1000.0
            previousFrameTime = start_time
            if (dt > 0.2):
                dt = 0.2
    else:
        screen.blit(death_screen, (0,0))
        pygame.display.flip()
        
