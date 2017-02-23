import math
import pygame
import sys
from utils import vector2
import random
from sprite import sprite_2

class wraith:
    thing = "thing"

    ice_warn_delay = 1000.00
    ice_attack_delay = 625.00
    ice_down_delay = 100.00
    wraith_teleport_delay = 6000.00
    hurt_teleport_delay = 250.00
    
    last_ice_warn = 0
    last_ice_attack = 0
    last_ice_down = 0
    last_ice_height_reached = 0
    last_wraith_teleport = 0

    ice_up_height = 1300
    ice_warn_height = 2100
    ice_attack_height = 1892

    ice_width = 128
    ice_height = 256
    wraith_height = 592
    wraith_width = 440

    ishurt = False

    ices = list()
    ice_sprites = list()
    heart = list()

    hp = 10
    ice_speed = 175
    x = 0
    y = 1493 

    # these are the different states that the ices can be in
    down = False
    warn = False
    attack = False
    going_up = False
    ice_height_reached = True
    ice_attacking = False
    
    def __init__(self, _ices, _image, _hurt, _hurt2):
        flop = 0
        num = 0
        index = 0
        count = -1
        self.ice_width = 128
        self.idle = _image
        self.hurt = _hurt
        self.hurt2 = _hurt2
        self.image = self.idle
        
        for ice in _ices:
            self.ices.append(ice)
            if (flop == 0):
                numbers = [0,1,2,3,4]
                index = random.randint(0,4)
                num = numbers[index]
                numbers.remove(index)
                flop = 1
                count = (count + 1)
            elif (flop == 1):
                index = random.randint(0,3)
                num = numbers[index]
                flop = 0
            ice.x = (((count * 5) + num) * 128)
           

        self.ices_to_sprites()

    def update(self,dt):
        cats = "cats"
        #ice_attack = False

        
        if ( ((pygame.time.get_ticks() - self.last_wraith_teleport) > self.wraith_teleport_delay)):
            self.wraith_teleport()
            
        if ( ((pygame.time.get_ticks() - self.last_ice_down) > self.ice_attack_delay) & (self.down | self.going_up) ):
            #self.ice_warn()
            self.ice_attack(dt)

        elif ( ((pygame.time.get_ticks() - self.last_ice_height_reached) > self.ice_down_delay) & (self.ice_height_reached) ):
            self.ice_up()

        #print self.ice_height_reached
        return self.ice_attacking

    def wraith_teleport(self):
        self.image = self.idle
        index = random.randint(0,24)
        self.x = (index * 128)
        self.last_wraith_teleport = pygame.time.get_ticks()
        #print "wraith teleporting"
        #print "wraith_x = " , self.x
        
    def ice_warn(self):
        self.last_ice_warn = pygame.time.get_ticks()
        self.down = False
        self.warn = True
        self.attack = False 
        #print "im warning you"
        for ice in self.ices:
            ice.y = self.ice_warn_height
        self.ice_attacking = False
        return
    
    def ice_attack(self,dt):
        self.last_ice_attack = pygame.time.get_ticks()
        self.down = False
        self.warn = False
        self.attack = True
        self.going_up = True
        #print "im attacking you"
        self.ice_attacking = True

        ice_level = (self.ices[0].y + (self.ice_speed * dt))

        if (ice_level > self.ice_attack_height):
            ice_level = self.ice_attack_height
            self.ice_height_reached = True
            self.last_ice_height_reached = pygame.time.get_ticks()
            self.going_up = False

        for ice in self.ices:    
            ice.y = ice_level
            ice.mask = pygame.mask.from_surface(ice.image)
            ice.rect = pygame.Rect(ice.x,ice.y,ice.width,ice.height)

        return

    def ice_up(self):
        self.last_ice_down = pygame.time.get_ticks()
        self.down = True
        self.warn = False
        self.attack = False
        self.ice_height_reached = False
        flop = 0
        num = 0
        index = 0
        count = -1
        #print "ices retreating"
        for ice in self.ices:
            if (flop == 0):
                numbers = [0,1,2,3,4]
                index = random.randint(0,4)
                num = numbers[index]
                numbers.remove(index)
                flop = 1
                count = (count + 1)
            elif (flop == 1):
                index = random.randint(0,3)
                num = numbers[index]
                flop = 0

            ice.x = (((count * 5) + num) * 128)
            ice.y = self.ice_up_height
            self.ice_attacking = False
        return

    def ice_collision(self, player, player_width, player_height,clip, player_image):
        hit = False
        for ice in self.ices:
            if ( ((ice.x) < (player.x) < (ice.x + ice.width)) | ( (ice.x) < (player.x + player_width) < (ice.x + ice.width) ) ):
                if ( ((ice.y) < (player.y) < (ice.y + ice.height)) | ( (ice.y) < (player.y + player_height) < (ice.y + ice.height) ) ):
                    tmp1 = pygame.Surface( (player_width,player_height), pygame.SRCALPHA )
                    tmp1.blit( player_image, (0,0),area = clip)
                    m1 = pygame.mask.from_surface( tmp1 )

                    tmp2 = pygame.Surface( (ice.width,ice.height), pygame.SRCALPHA )
                    tmp2.blit( ice.image, (0,0))
                    m2 = pygame.mask.from_surface( tmp2 )

                    if m1.overlap( m2, (int(math.floor(ice.x - player.x)), int(math.floor(ice.y - player.y))) ) is not None:
                        #cat = "cat"
                        #print "BOOM!"
                        hit = True
                    #else:
                        #print "..."
        if (hit):
            return False
        else:
            return True
    '''
    def pp_ice_collision(self,player):
        
        p_mask = pygame.Rect(player.x, player.y, player.width, player.height)
        tmp1 = pygame.Surface( (player.width,player.height), pygame.SRCALPHA )
        tmp1.blit( player.image, (player.x,player.y), area=p_mask )
        m1 = pygame.mask.from_surface( tmp1 )
        
        for ice in self.ice_sprites:
            r_mask = pygame.Rect(ice.x, ice.y, ice.width, ice.height)
            tmp2 = pygame.Surface( (ice.width,ice.height), pygame.SRCALPHA )
            tmp2.blit( ice.image, (ice.x,ice.y), area=r_mask )
            m2 = pygame.mask.from_surface( tmp2 )
            
            #if m1( m2, ((ice.x - player.x), (ice.y-player.y)) ) is not None:
            if pygame.( m2, (int(math.floor(ice.x - player.x)),int(math.floor(ice.y - player.y))) ) is not None:
                print "collision"
        
        for ice in self.ice_sprites:
            if ( pygame.sprite.spritecollide(player, self.ice_sprites, False, pygame.sprite.collide_mask) )is not None:
                print "collide"
            
        return
    '''
                
        

    def check_hit(self, player, player_width, player_height, player_image, clip):
        hit = False
        #print "punch"
        '''
        for h in self.heart:
            if ( ((h.x) < (player.x) < (h.x + h.width)) | ( (h.x) < (player.x + player_width) < (h.x + h.width) ) ):
                if ( ((h.y) < (player.y) < (h.y + h.height)) | ( (h.y) < (player.y + player_height) < (h.y + h.height) ) ):
                    hit = True
                    #print"hit"
        '''
        if(not self.ishurt):
            tmp1 = pygame.Surface( (player_width,player_height), pygame.SRCALPHA )
            tmp1.blit( player_image, (0,0),area = clip)
            m1 = pygame.mask.from_surface( tmp1 )

            tmp2 = pygame.Surface( (self.wraith_width,self.wraith_height), pygame.SRCALPHA )
            tmp2.blit( self.image, (0,0))
            m2 = pygame.mask.from_surface( tmp2 )

            if m1.overlap( m2, (int(math.floor(self.x - player.x)), int(math.floor(self.y - player.y))) ) is not None:
                #cat = "cat"
                #print "hit wraith"
                hit = True
                ishurt = True
                self.image = self.hurt
                self.last_teleport = (pygame.time.get_ticks() - self.hurt_teleport_delay)

        if (hit):
            self.hp = (self.hp - 1)
            #print "hit wraith"
            #print self.hp
            return
        else:
            return
            #print "miss"
    
    def ices_to_sprites(self):
        ice_sprites = list()
        
        for ice in self.ices:
            tmp_sprite = sprite_2(ice.image,ice.x,ice.y,ice.height,ice.width)
            ice_sprites.append(tmp_sprite)

        self.ice_sprites = ice_sprites
        return     
        
