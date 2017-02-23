import math
import pygame
import sys
from utils import vector2
import random
from sprite import sprite_2

class tree:
    thing = "thing"

    root_warn_delay = 1000.00
    root_attack_delay = 625.00
    root_down_delay = 500.00

    last_root_warn = 0
    last_root_attack = 0
    last_root_down = 0
    last_root_height_reached = 0
    

    root_down_height = 2100
    root_warn_height = 2100
    root_attack_height = 1892

    root_width = 128
    root_height = 256

    roots = list()
    root_sprites = list()
    heart = list()

    hp = 5
    root_speed = 40

    # these are the different states that the roots can be in
    down = False
    warn = False
    attack = False
    going_up = False
    root_height_reached = True
    root_attacking = False
    
    def __init__(self, _roots, _root_width, _heart):
        flop = 0
        num = 0
        index = 0
        count = -1
        self.root_width = _root_width

        self.heart.append(_heart)
        
        for root in _roots:
            self.roots.append(root)
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
            root.x = (((count * 5) + num) * 128)

        self.roots_to_sprites()

    def update(self,dt):
        cats = "cats"
        #root_attack = False
        if ( ((pygame.time.get_ticks() - self.last_root_down) > self.root_attack_delay) & (self.down | self.going_up) ):
            #self.root_warn()
            self.root_attack(dt)

        elif ( ((pygame.time.get_ticks() - self.last_root_height_reached) > self.root_down_delay) & (self.root_height_reached) ):
            self.root_down()

        #print self.root_height_reached
        return self.root_attacking

    def root_warn(self):
        self.last_root_warn = pygame.time.get_ticks()
        self.down = False
        self.warn = True
        self.attack = False 
        #print "im warning you"
        for root in self.roots:
            root.y = self.root_warn_height
        self.root_attacking = False
        return
    
    def root_attack(self,dt):
        self.last_root_attack = pygame.time.get_ticks()
        self.down = False
        self.warn = False
        self.attack = True
        self.going_up = True
        #print "im attacking you"
        self.root_attacking = True

        root_level = (self.roots[0].y - (self.root_speed * dt))

        if (root_level < self.root_attack_height):
            root_level = self.root_attack_height
            self.root_height_reached = True
            self.last_root_height_reached = pygame.time.get_ticks()
            self.going_up = False

        for root in self.roots:    
            root.y = root_level
            root.mask = pygame.mask.from_surface(root.image)
            root.rect = pygame.Rect(root.x,root.y,root.width,root.height)

        return

    def root_down(self):
        self.last_root_down = pygame.time.get_ticks()
        self.down = True
        self.warn = False
        self.attack = False
        self.root_height_reached = False
        flop = 0
        num = 0
        index = 0
        count = -1
        #print "roots retreating"
        for root in self.roots:
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

            root.x = (((count * 5) + num) * 128)
            root.y = self.root_down_height
            self.root_attacking = False
        return

    def root_collision(self, player, player_width, player_height,clip, player_image):
        hit = False
        for root in self.roots:
            if ( ((root.x) < (player.x) < (root.x + root.width)) | ( (root.x) < (player.x + player_width) < (root.x + root.width) ) ):
                if ( ((root.y) < (player.y) < (root.y + root.height)) | ( (root.y) < (player.y + player_height) < (root.y + root.height) ) ):
                    tmp1 = pygame.Surface( (player_width,player_height), pygame.SRCALPHA )
                    tmp1.blit( player_image, (0,0),area = clip)
                    m1 = pygame.mask.from_surface( tmp1 )

                    tmp2 = pygame.Surface( (root.width,root.height), pygame.SRCALPHA )
                    tmp2.blit( root.image, (0,0))
                    m2 = pygame.mask.from_surface( tmp2 )

                    if m1.overlap( m2, (int(math.floor(root.x - player.x)), int(math.floor(root.y - player.y))) ) is not None:
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
    def pp_root_collision(self,player):
        
        p_mask = pygame.Rect(player.x, player.y, player.width, player.height)
        tmp1 = pygame.Surface( (player.width,player.height), pygame.SRCALPHA )
        tmp1.blit( player.image, (player.x,player.y), area=p_mask )
        m1 = pygame.mask.from_surface( tmp1 )
        
        for root in self.root_sprites:
            r_mask = pygame.Rect(root.x, root.y, root.width, root.height)
            tmp2 = pygame.Surface( (root.width,root.height), pygame.SRCALPHA )
            tmp2.blit( root.image, (root.x,root.y), area=r_mask )
            m2 = pygame.mask.from_surface( tmp2 )
            
            #if m1( m2, ((root.x - player.x), (root.y-player.y)) ) is not None:
            if pygame.( m2, (int(math.floor(root.x - player.x)),int(math.floor(root.y - player.y))) ) is not None:
                print "collision"
        
        for root in self.root_sprites:
            if ( pygame.sprite.spritecollide(player, self.root_sprites, False, pygame.sprite.collide_mask) )is not None:
                print "collide"
            
        return
    '''
                
        

    def check_heart(self, player, player_width, player_height):
        hit = False
        #print "punch"
        for h in self.heart:
            if ( ((h.x) < (player.x) < (h.x + h.width)) | ( (h.x) < (player.x + player_width) < (h.x + h.width) ) ):
                if ( ((h.y) < (player.y) < (h.y + h.height)) | ( (h.y) < (player.y + player_height) < (h.y + h.height) ) ):
                    hit = True
                    #print"hit"
        
        if (hit):
            self.hp = (self.hp - 1)
            #print "hit"
            #print "hp: " , self.hp
            return
        else:
            return
            #print "miss"
    
    def roots_to_sprites(self):
        root_sprites = list()
        
        for root in self.roots:
            tmp_sprite = sprite_2(root.image,root.x,root.y,root.height,root.width)
            root_sprites.append(tmp_sprite)

        self.root_sprites = root_sprites
        return     
        
