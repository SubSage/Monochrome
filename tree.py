import math
import pygame
import sys
from utils import vector2
import random

class tree:
    thing = "thing"

    root_warn_delay = 1000.00
    root_attack_delay = 625.00
    root_down_delay = 2000.00

    last_root_warn = 0
    last_root_attack = 0
    last_root_down = 0

    root_down_height = 0
    root_warn_height = 2050
    root_attack_height = 1892

    root_width = 0
    root_height = 256

    roots = list()
    heart = list()
    root_attacking = False

    hp = 300

    # these are the different states that the roos can be in
    down = True
    warn = False
    attack = False
    
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

    def update(self,dt):
        cats = "cats"
        root_attack = False
        if ( ((pygame.time.get_ticks() - self.last_root_down) > self.root_warn_delay) & ( (self.down) & (not self.warn) & (not self.attack)) ):
            self.root_warn()

        elif ( ((pygame.time.get_ticks() - self.last_root_warn) > self.root_attack_delay) & ((not self.down) & (self.warn) & (not self.attack)) ):
            self.root_attack()

        elif ( ((pygame.time.get_ticks() - self.last_root_attack) > self.root_down_delay) & ((not self.down) & (not self.warn) & (self.attack)) ):
            self.root_down()
        
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

    def root_attack(self):
        self.last_root_attack = pygame.time.get_ticks()
        self.down = False
        self.warn = False
        self.attack = True
        #print "im attacking you"
        for root in self.roots:    
            root.y = self.root_attack_height

        self.root_attacking = True
        return

    def root_down(self):
        self.last_root_down = pygame.time.get_ticks()
        self.down = True
        self.warn = False
        self.attack = False
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

    def root_collision(self, player, player_width, player_height):
        hit = False
        for root in self.roots:
            if ( ((root.x) < (player.x) < (root.x + root.width)) | ( (root.x) < (player.x + player_width) < (root.x + root.width) ) ):
                if ( ((root.y) < (player.y) < (root.y + root.height)) | ( (root.y) < (player.y + player_height) < (root.y + root.height) ) ):
                    hit = True
        if (hit):
            return False
        else:
            return True

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
            #print self.hp
            return
        else:
            return
            #print "miss"
            
        
        
