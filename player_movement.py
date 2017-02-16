import math
import pygame
import sys
from utils import vector2

class player_movement:
    def __init__(self):
        self.thing = "thing"

    def update_velocities(self, SPEED, dt, GRAV, vx, vy, isgrounded):
        #v = vector2((0,0))
        keys = pygame.key.get_pressed()
        inputX = 0
        inputY = 0
        DECCELERATION = 12.5
        JUMPSPEED = 4
        PUNCHING = False
        last_punch = 0
        punch_delay = 750.00

        # this reads the players input
        if ((keys[pygame.K_a])|(keys[pygame.K_LEFT])):
            inputX -= 1
        if ((keys[pygame.K_d])|(keys[pygame.K_RIGHT])):
            inputX += 1
        if ((keys[pygame.K_w])|(keys[pygame.K_UP])):
            inputY -= 1
        if ((keys[pygame.K_s])|(keys[pygame.K_DOWN])):
            inputY += 1
            
        if((pygame.time.get_ticks() - last_punch) > punch_delay):
            if ((keys[pygame.K_SPACE])|(keys[pygame.K_z])):
                last_punch = pygame.time.get_ticks()
                PUNCHING = True
            
            
        #this makes the player instantly re-accelerate on the ground
        if ((inputX != 0) & (isgrounded) ):
            vx = (inputX * SPEED)

        # decceleration is slower while in midair
        elif (isgrounded == False):
            DECCELERATION = (DECCELERATION/16)

        # deccelerate normally while in on the ground
        if vx > 0:
            vx = vx - (DECCELERATION * dt)

            if vx < 0:
                vx = 0
        elif vx < 0:
            vx = vx + (DECCELERATION * dt)
            if vx > 0:
                vx = 0
        '''
        if (isgrounded):
            v.y = 0
            if (inputY < 0):
                v.y = v.y - 75
        #else:
        '''
        # this makes the player jump
        if(isgrounded):
            if inputY < 0:
                vy = inputY * JUMPSPEED

        # this makes the player jumping mid air
        if (isgrounded == False):
            vy = (vy + (GRAV * dt))
        
        '''
        if inputY != 0:
            cats = "cats"
            #v.y = inputY + SPEED
        elif v.y < 0:
            v.y = v.y + DECCELERATION * dt
            if v.y > 0:
                v.y = 0
         elif v.y > 0:
            v.y = v.y - DECCELERATION * dt
            if v.y < 0:
                v.y = 0
        '''
        # calculate for effect of gravity acting on vy
        

        #print v.y
        return vx,vy, PUNCHING

    def check_ground(self, ground_blocks, last_player_x, last_player_y, player_width, player_height, vx, vy, tile_height, tile_width , SPEED, dt):
        isgrounded = False
        touchingwall = False
        movement_x = (vx * dt)
        movement_y = (vy * dt)
        current_player_x = last_player_x + movement_x
        current_player_y = last_player_y + movement_y

        
        # iterate through ground objects and check for collision
        for layer in ground_blocks:
            for block in layer:
                #print block.width
                #print block.height
                # chack if player collides with block in x axis
                #if ( block.x < current_player_x | (current_player_x + player_width)) < (block.x + block.width) ):
                if ( (block.x <= current_player_x <= (block.x + block.width)) | ( block.x < (current_player_x + player_width) <= (block.x + block.width)) ):
                    # check if player collides with block in y axis
                    #if ( block.y < (current_player_y | (current_player_y + player_height)) < (block.x + block.width) ):
                    if ( (block.y <= current_player_y <= (block.y + block.height)) | ( block.y < (current_player_y + player_height) <= (block.y + block.height)) ):
                        #print "vy",vy
                        #print "vx",vx
                        '''

                        if(((vy == 0) | (vx == 0)) == False):
                            if ( ((block.x - last_player_x)/vy) > ((block.y - last_player_y)/vx) ):
                                #print "corner wall"
                                if (vx > 0):
                                    print "touch right wall"
                                    current_player_x = (block.x - player_width)
                                    touchingwall = True
                                elif (vx < 0):
                                    print "touch left wall"
                                    current_player_x = (block.x + block.width)
                                    touchingwall = True
                            else:
                                if (vy >= 0):
                                    print "corner floor"
                                    current_player_y = (block.y - player_height)
                                    isgrounded = True
                                else:
                                    print "corner ceiling"
                                    current_player_y = (block.y + block.height)
                        elif (vy > 0):
                            print "touch floor"
                            current_player_y = (block.y - player_height)
                            isgrounded = True
                        elif (vy < 0):
                            print "touch ceiling"
                            current_player_y = (block.y + block.height)
                        elif (vx > 0):
                            print "touch right wall"
                            current_player_x = (block.x - player_width)
                            touchingwall = True
                        elif (vx < 0):
                            print "touch left wall"
                            current_player_x = (block.x + block.width)
                            touchingwall = True

                       '''
                        #hitting the floor
                        if( (block.y <= current_player_y < (block.y + block.height)) ^ ( block.y < (current_player_y + player_height) <= (block.y + block.height))):
                            # collision bellow player
                            if (( block.y <= (current_player_y + player_height) <= (block.y + block.height)) & (current_player_y < block.y) ):
                                current_player_y = (block.y - player_height)
                                isgrounded = True

                            # collision above player
                            elif (( block.y < (current_player_y) < (block.y + block.height)) & ((current_player_y + player_height)> (block.y + block.height)) ):
                                current_player_y = (block.y + block.height)


                        #hitting a wall
                        elif(( (block.x <= current_player_x < (block.x + block.width)) ^ ( block.x < (current_player_x + player_width) <= (block.x + block.width)) ) ):
                            #print "wall"
                            # collision right of player
                            if ( block.x <= (current_player_x + player_width) <= (block.x + block.width)):
                                current_player_x = (block.x - player_width)
                                vx = 0
                                touchingwall = True

                            # collison left of player
                            elif ( block.x <= (current_player_x) <= (block.x + block.width)):
                                current_player_x = (block.x + block.width)
                                vx = 0
                                touchingwall = True

                        #hitting a corner
                        elif(((vy == 0) | (vx == 0)) == False):
                            if(( (block.y <= current_player_y <= (block.y + block.height)) ^ ( block.y <= (current_player_y + player_height) <= (block.y + block.height)) )&( (block.x <= current_player_x <= (block.x + block.width)) ^ ( block.x <= (current_player_x + player_width) <= (block.x + block.width)))) :

                                #print "corner"
                                if ( ((block.x - last_player_x)/vy) <= ((block.y - last_player_y)/vx) ):
                                    if (vy >= 0):
                                        current_player_y = (block.y - player_height)
                                        
                                    elif (vy <= 0):
                                        current_player_y = (block.y + block.height)
                                        isgrounded = True
                                    
                            

                                elif( ((block.x - last_player_x)/vy) <= ((block.y - last_player_y)/vx) ):
                                    if (vx > 0):
                                        current_player_x = (block.x - player_width)
                                    elif (vx < 0):
                                        current_player_x = (block.x + block.width)
                                    touchingwall = True
                        '''
                        -----------------------------------------------------------------------------------------
                        '''    
                        
                        '''
                        #print "cats"
                        if(vx == 0):
                            #if ( (block.x <= current_player_x <= (block.x + block.width)) & ( block.x <= (current_player_x + player_width) <= (block.x + block.width)) ):
                            if (vy > 0):
                                current_player_y = (block.y - player_height)
                                isgrounded = True
                            elif (vy < 0):
                                current_player_y = (block.y + block.height)
                            

                        elif (vy == 0):
                            #if ( (block.y <= current_player_y <= (block.y + block.height)) & ( block.y <= (current_player_y + player_height) <= (block.y + block.height)) ): 
                            if (vx > 0):
                                current_player_x = (block.x - player_width)
                            elif (vx < 0):
                                current_player_x = (block.x + block.width)
                            touchingwall = True
                            
                        elif ( (movement_y/vy) <= (movement_x/vx) ):
                            if (vy > 0):
                                current_player_y = (block.y - player_height)
                                isgrounded = True
                            elif (vy < 0):
                                current_player_y = (block.y + block.height)
                            

                        elif( (movement_y/vy) > (movement_x/vx) ):
                            if (vx > 0):
                                current_player_x = (block.x - player_width)
                            elif (vx < 0):
                                current_player_x = (block.x + block.width)
                            touchingwall = True
                        '''
        
        if(isgrounded):
            vy = 0
        if(touchingwall):
            vx = 0
            
        current_player_x += vx
        current_player_y += vy
        
        return current_player_x, current_player_y, vx, vy, isgrounded
