import math
import pygame
import sys


class vector2:
   # note, no data member declarations needed

   # constructor
   def __init__(self, x, y):
      # unlike C/Java, no implicit "this" pointer
      # instead, reference is passed in as first argument (self in this case)
      self.x = x
      self.y = y
      self.vx = 0
      self.vy = 0
   # method definitions
   def add(self, other):
      v = vector2(self.x + other.x, self.y + other.y)
      return v

   def subtract(self, other):

      v = vector2(1,1)

      if(self.x > other.x):
         v.x = (self.x - other.x)
      else:
         v.x = ( (other.x - self.x) * (-1) )

      if(self.y > other.y):
         v.y = (self.y - other.y)
      else:
         v.y = ( (other.y - self.y) * (-1) )

      return v
    
   def scale(self, scalar):
      v = vector2(self.x * scalar, self.y * scalar)
      return v

   def magnitude(self):
      m = math.sqrt( (self.x *  self.x) + (self.y * self.y) )
      #print "</magnitude>"
      return m

   def normalize(self):
      magnitude = self.magnitude() 
      self.x = ( self.x / magnitude )
      self.y = ( self.y / magnitude )
      return
   

   # overload return-this-as-string for printing
   def __str__(self):
      # format allows you to replace "{}" with variable values
      return "({}, {})".format(self.x, self.y)

class sprite2:
   # constructor
   def __init__(self, x, y, vx, vy):
      pygame.image = pygame.Surface((50,50))
      self.x = x
      self.y = y
      self.vx = vx
      self.vy = vy
      self.radius = 50
      self.color = (0,255,0)
      self.thickness = 10
   # method definitions
   
   def update(self, delta):

      #check for wall collision
      if ((self.x + self.vx + self.radius) > 1024):
         self.x = 1024 - self.radius
         self.vx = self.vx * (-1)
      elif ((self.x + self.vx - self.radius) < 0):
         self.x = self.radius
         self.vx = self.vx * (-1)

      if ((self.y + self.vy + self.radius) > 768):
         self.y = 768 - self.radius
         self.vy = self.vy * (-1)
      elif ((self.y + self.vy - self.radius) < 0):
         self.y = self.radius
         self.vy = self.vy * (-1)

      #update positions
      self.x = ( self.x + (self.vx * delta) )
      self.y = ( self.y + (self.vy * delta) )
      return

   def collision_check(self, list, screen):
      cx = 1
      cy = 1
      cn = 1
      for obj in list:
         if ( (self.x != obj.x) & (self.y != obj.y) ):
            '''
            if(self.x > obj.x):
               cx = self.x - obj.x
               cy = self.y - obj.y
            else:
               cx = obj.x - self.x
               cy = obj.y - self.y
            
            '''
            if(self.x > obj.x):
               cx = self.x - obj.x
            else:
               cx = obj.x - self.x
            if(self.y > obj.y):
               cy = self.y - obj.y
            else:
               cy = obj.y - self.y
            
            cn = math.sqrt((cy*cy) + (cx*cx))
            #print "cn"
            #print cn
            #print "self.radius + obj.radius"
            #print (self.radius + obj.radius)
            #if circles overlap
            if (cn < (self.radius + obj.radius )):
               #change color of circles
               if ( (self.color != (255,0,0)) & (obj.color != (255,0,0)) ):
                  self.color = (255,0,0)
                  obj.color = (255,0,0)
                  
               elif ( (self.color != (0,0,255)) & (obj.color != (0,0,255)) ):
                  self.color = (0,0,255)
                  obj.color = (0,0,255)
                  
               elif ( (self.color != (0,255,0)) & (obj.color != (0,255,0)) ):
                  self.color = (0,255,0)
                  obj.color = (0,255,0)
                  
               if(self.x > obj.x):
                  self.x = (self.x + (self.x-obj.x) + 1)
               elif(obj.x > self.x):
                  obj.x = (obj.x + (obj.x-self.x) + 1)
               if(self.y > obj.y):
                  self.y = (self.y + (self.y-obj.y) + 1)
               elif(obj.y > self.y):
                  obj.y = (obj.y + (obj.y-self.y) + 1)

               self.draw(screen)
               obj.draw(screen)
               pygame.display.flip()
               self.vx = self.vx * (-1)
               self.vy = self.vy * (-1)
               obj.vx = obj.vx * (-1)
               obj.vy = obj.vy * (-1)
               

   def draw(self, screen):
      pygame.draw.circle(screen, self.color, (self.x,self.y), self.radius)
      return

   def magnitude(self):
      m = math.sqrt( (self.x *  self.x) + (self.y * self.y) )
      return m
   
   # overload return-this-as-string for printing
   def __str__(self):
      # format allows you to replace "{}" with variable values
      return "({}, {})".format(self.x, self.y)
