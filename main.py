import sys
import math
import pygame
from pygame.locals import QUIT
import collision

def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

pygame.font.init()
my_font = pygame.font.SysFont('Times New Roman', 30)
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
speed = 0.1
accel = 0.1
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
terrain = [[(100, 100), (120, 100)], [(80, 90), (100, 100)], [(80, 90),(120, 100)]]



class Torpedo:
    def __init__(self, velo, pos):
        self.velocity = velo
        self.position = pos

    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] -= self.velocity[1]

    def destruct(self):
        del self

def anglevector(a, b):
    return (math.cos(a) * b, math.sin(a) * b)

def text(imagedir, t):
    speech = my_font.render(t, False, (255, 255,255))
    screen.blit(speech, (100, 400))
    image = pygame.image.load(imagedir)
    screen.blit(image, (30, 400))


while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update.
    radarangle += 0.05
    if radarangle >= math.pi * 2:
        radarangle = 0
    keys = pygame.key.get_pressed()
    ENMOV += 0.01
    enemyloc[0] = (math.sin(ENMOV) + 1) * 100
    if keys[pygame.K_LEFT]:
        rotation += 0.01
    if keys[pygame.K_RIGHT]:
        rotation -= 0.01

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
            torpedoes.append(
                Torpedo(
                    [math.cos(rotation) * 2, math.sin(rotation) * 2],
                    [
                        location[0] + math.cos(rotation) * 10,
                        location[1] - math.sin(rotation) * 15,
                    ],
                )
            )
            pressed = True
    else:
        pressed = False

    for torp in torpedoes:
        torp.move()
    nocol = True

    #defining a hitbox before doing collision detection
    front = ((math.cos(rotation)*15)+location[0],(math.sin(rotation)*15)+location[1])
    back = (location[0]-(math.cos(rotation)*15),location[1]-(math.sin(rotation)*15))
    left = ((math.cos(rotation-90)*10)+location[0],(math.sin(rotation-90)*10)+location[1])
    right = ((math.cos(rotation+90)*10)+location[0],(math.sin(rotation+90)*10)+location[1])
    hitbox = [[front, left], [left, back], [back, right], [right, front]]
    for segment in terrain:
        for side in hitbox:
            if collision.collides(side, segment):
                print("collision!")
                nocol = False
    if nocol:
        location[0] += math.cos(rotation) * speed
        location[1] -= math.sin(rotation) * speed
    else:
        speed=0
    # Draw.
    pygame.draw.circle(screen, (0, 100, 0), location, radar)
    radarvect = anglevector(radarangle, radar)
    pygame.draw.line(
        screen,
        (0, 200, 0),
        location,
        (radarvect[0] + location[0], radarvect[1] + location[1]),
    )
    for segment in terrain:
        pygame.draw.line(screen, (100, 100, 100), segment[0], segment[1])
    if radarangle == 0:
        if distance(location, enemyloc) <= radar:
            lastknown[0] = enemyloc[0]
            lastknown[1] = enemyloc[1]
            inrange = True
        else:
            inrange = False
    #drawing red dot
    if distance(location, lastknown) <= radar and inrange:
        pygame.draw.circle(screen, (255, 0, 0), lastknown, 3)
    #drawing torpedoes
    for torp in torpedoes:
        pygame.draw.circle(screen, (255, 100, 0), torp.position, 3)
    #rotate and blit the submarine surface
    rotsub = pygame.transform.rotate(sub, math.degrees(rotation) - 90)
    screen.blit(rotsub, (location[0] - 10, location[1] - 15))
    #text display
    text("eye.png", "THE EYE")
    for side in hitbox:
        pygame.draw.line(screen, (0, 0, 255), side[0], side[1])
    pygame.display.flip()
    fpsClock.tick(fps)
