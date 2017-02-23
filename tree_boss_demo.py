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
pygame.init()
tile_width = 128
tile_height = 128
screen = pygame.display.set_mode((1280,640), pygame.FULLSCREEN)
pygame.display.set_caption( "TreeBoss" )
tiled_map = load_pygame('tree_boss.tmx')
layer = 0
t_x = 0
t_y = 0
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
dt = 0.0 # delta time
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
death_time = 0
death_delay = 1000.00
#frame stuff for animation
frame = 0
frame_timer = 0
FRAME_TIME = .10
FRAME_CT = 6
Aheight = 0
Mright = True
Mleft = False
titleframe = 0
titleanimations= list()
titlepicture = pygame.image.load( "Art Assets\Ame\Monochrome-Titlescreen\Monochrome-Titlescreen0001.jpg" ).convert()
for x in range(1, 9):
    titlepicture = pygame.image.load( "Art Assets\Ame\Monochrome-Titlescreen\Monochrome-Titlescreen000" + str(x) + ".jpg" ).convert()
    titleanimations.append(titlepicture)
for x in range(10, 24):
    titlepicture = pygame.image.load( "Art Assets\Ame\Monochrome-Titlescreen\Monochrome-Titlescreen00" + str(x) + ".jpg" ).convert()
    titleanimations.append(titlepicture)
gamestate=0 # this is to move the game along from title to fight 1, 2, 3, end title

player_image = pygame.image.load( "HMCF2.png" ).convert_alpha()
clip = pygame.Rect(158*frame, Aheight * 154 , 160, 154 )

for obj in ground:
     box = Rect(obj.x, obj.y, obj.width, obj.height)
     ground_blocks_rect.append(box)

for obj in boss_hitboxes:
     box = Rect(obj.x, obj.y, obj.width, obj.height)
     boss_hitboxes_rect.append(box)

    #player.box.y = float(player.box.y)
    #player.box.y = player.box.y + 0.16
previousFrameTime = pygame.time.get_ticks()
#################################################################################################
while gamestate == 0:
    start_time = pygame.time.get_ticks()
    dt = (start_time - previousFrameTime) / 1000.0
    previousFrameTime = start_time
    pygame.event.pump()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT or evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
            gamestate = gamestate + 1

    titleframe += dt * 12
    print titleframe
    screen.fill( (48, 24 , 96) )
    if(int(titleframe) < 22):
        screen.blit(titleanimations[int(titleframe)], (0,0))
    else:
        screen.blit(titlepicture, (0,0))
    pygame.display.flip()

##################################################################################################
while gamestate == 1:
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
            gamestate = gamestate + 1
            #screen.blit(win_screen, (0,0))
            #pygame.display.flip()

        else:
            # update player speed
            vx,vy, PUNCHING = player_movement.update_velocities(SPEED, dt, GRAV, vx, vy, isgrounded )

            #sprite controls
            mkeys = pygame.key.get_pressed()
            if ((mkeys[pygame.K_a]) or (mkeys[pygame.K_LEFT])):
                 Mleft = True
                 Mright = False
                 if frame == 0:
                      FRAME_CT = 7
                      Aheight = 0
                      frame = 1

            if ((mkeys[pygame.K_d]) or (mkeys[pygame.K_RIGHT])):
                 Mleft = False
                 Mright = True
                 if frame == 0:
                      FRAME_CT = 7
                      Aheight = 0
                      frame = 1

            if ((mkeys[pygame.K_w]) or (mkeys[pygame.K_UP])):
                 if frame ==0:
                      FRAME_CT = 5
                      Aheight = 2
                      frame = 1

            if ((mkeys[pygame.K_z]) or (mkeys[pygame.K_SPACE])):
                 if frame == 0:
                      FRAME_CT = 6
                      Aheight = 3
                      frame = 1

            # Check for ground collisions
            player.x, player.y, vx, vy, isgrounded = player_movement.check_ground(ground_blocks, player.x, player.y, player_width, player_height, vx, vy, tile_height, tile_width, SPEED, dt)

            # update tree stuff
            root_attack = tree_boss.update(dt)


            # check if player gets hits heart

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
            if frame != 0:
                 if frame_timer > FRAME_TIME:
                      frame_timer -= FRAME_TIME
                      frame = (frame + 1) % FRAME_CT
                 frame_timer += dt

           # img = pygame.image.load( "HMCF.png" ).convert_alpha()
            #clip = pygame.Rect( 164 + 158*frame, Aheight * 154 , 160, 154 )

            #screen.blit(img, (22,0), area=clip, special_flags=pygame.BLEND_RGBA_MIN )
            #screen.blit(player.image, (player.x - cameraX, player.y + cameraY ))

            img = player_image
            Bimg = pygame.transform.flip(player_image, True , False)
            clip = pygame.Rect(158*frame, Aheight * 154 , 160, 154 )

            if Mright == True:
                 screen.blit(img, (player.x - cameraX, player.y + cameraY ), clip )
            if Mleft == True:
                 screen.blit(Bimg , (player.x - cameraX, player.y + cameraY ), clip)

            pygame.display.flip()
            dt = (start_time - previousFrameTime) / 1000.0
            previousFrameTime = start_time
            if (dt > 0.2):
                dt = 0.2

            # check if player gets hit by roots
            if (tree_boss.root_attacking):
                 player_alive = tree_boss.root_collision(player, player_width, player_height, clip, player_image)
                 if(not player_alive):
                      death_time = pygame.time.get_ticks()

    else:
        if((pygame.time.get_ticks()) > (death_time + death_delay)):
             screen.blit(death_screen, (0,0))
             pygame.display.flip()
