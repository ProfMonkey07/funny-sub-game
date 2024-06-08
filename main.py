import sys
import math
import pygame
from pygame.locals import *
 

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
hp = 100
torpedoes = 5
location = [320, 240]
rotation = 90
maxspeed = 1
speed = .1
accel = .1
radar = 60
radarangle = 0
enemyloc = [100, 100]
ENMOV = 0
# Game loop.
lastknown = [0, 0]
inrange = True
sub = pygame.Surface((20, 30), pygame.SRCALPHA)
pygame.draw.ellipse(sub, (255, 255, 255), (0, 0, 20, 30))
print(pygame.Surface.get_bounding_rect(sub))
torpedoes = []
class torpedo:
    def __init__(self, velo, pos):
        self.velocity = velo
        self.position = pos
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] -= self.velocity[1]
    def destruct(self):
        del self

def anglevector(a, b):
    return((math.cos(a)*b, math.sin(a)*b))

while True:
  screen.fill((0, 0, 0))
  

  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  
  # Update.
  radarangle += .05
  if radarangle >= math.pi*2:
    radarangle = 0
  keys = pygame.key.get_pressed()
  ENMOV += .01
  enemyloc[0] = (math.sin(ENMOV) + 1) * 100
  if keys[pygame.K_LEFT]:
    rotation += .01
  if keys[pygame.K_RIGHT]:
    rotation -= .01
    
  if keys[pygame.K_UP]:
    if speed < maxspeed:
        speed += accel
    if speed > maxspeed:
        speed = maxspeed
  if keys[pygame.K_DOWN]:
    if speed > 0:
        speed -= accel
    if speed < 0:
        speed = 0
  if keys[pygame.K_SPACE]:
    if not pressed:
        torpedoes.append(torpedo([math.cos(rotation)*2, math.sin(rotation)*2], [location[0] + math.cos(rotation-.5)*10, location[1] - math.sin(rotation-.5)*15]))
        pressed = True
  else:
    pressed = False

  for torp in torpedoes:
    torp.move()

  location[0] += math.cos(rotation)*speed
  location[1] -= math.sin(rotation)*speed
  # Draw.
  pygame.draw.circle(screen, (0, 100, 0), location, radar)
  radarvect = anglevector(radarangle, radar)
  pygame.draw.line(screen, (0, 200, 0), location, (radarvect[0] + location[0], radarvect[1] + location[1]))
  if radarangle == 0:
    if distance(location, enemyloc) <= radar:
        lastknown[0] = enemyloc[0]
        lastknown[1] = enemyloc[1]
        inrange = True
    else:
        inrange = False

  if distance(location, lastknown) <= radar and inrange:
    pygame.draw.circle(screen, (255, 0, 0), lastknown, 3)
  for torp in torpedoes:
    pygame.draw.circle(screen, (255, 100, 0), torp.position, 3)
  rotsub = pygame.transform.rotate(sub, math.degrees(rotation) - 90)
  screen.blit(rotsub, (location[0]-10, location[1]-15))
  pygame.display.flip()
  fpsClock.tick(fps)