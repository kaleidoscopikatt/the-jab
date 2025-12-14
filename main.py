import os
import random

import compadre
import uuid

from game.classes import Player, screen_object, Floor, Present
from game.globals import win, Assets, particles
from game.particles import particle
from game.particles.present import present as present_particle

import sys

try:
    import pygame
except ModuleNotFoundError as e:
    os.system("pip install pygame --user")

pygame.display.set_caption("Santa's Present-Catcher!")

run = True
pygame.init()

preloaded_images = Assets()

display_info = pygame.display.Info()
screen_width = display_info.current_w
screen_height = display_info.current_h

floor_y = screen_height / 1.05 # Don't ask (or fix it's funny)
floor_n = (screen_width // 600) + 1

curr_round = 0
round_boundaries = [ # No. of Presents Dropped = n + 5
    10,
    15,
    25,
]

dropped_prezzies = 0

current_player = Player(500,floor_y-preloaded_images["player"].get_height(), preloaded_images["player"])
playerReach = floor_y * current_player.speed

screen_objects = [
    current_player,
    Present(random.randint(0,2000), 0, preloaded_images["present"], uuid=uuid.uuid4())
]

## Variable Floor Width
for floor_number in range(floor_n):
    xPos = 600 * floor_number
    screen_objects.append(Floor(xPos, floor_y, preloaded_images["floor"]))

## Compadre Setup
compadre.screenWidth = screen_width
compadre.boot(3)

presents = []
presents_cache = []

score = 0
score_font = pygame.font.SysFont("jetbrains_mono", 50) # Awwwww...
score_text = score_font.render(f"Score: {score}", True, (255,0,0))

def __randomPosition():
    currX = current_player.x
    maxX = min(int(currX + playerReach), screen_width)
    minX = max(0, int(currX - playerReach))

    randomValue = random.randrange(minX, maxX)
    return randomValue

def getPosition():
    randomValue = __randomPosition()
    shouldUnreach = compadre.readCompadre()["flag"]

    currX = current_player.x
    if shouldUnreach:
        print("SHOULD UNREACH!!!")
        if random.randrange(1, 4) == 1 or score == round_boundaries[curr_round] - 1:
            if randomValue >= currX:
                randomValue = min(currX + playerReach + random.randrange(0, 25), screen_width)
            else:
                randomValue = max(0, currX - playerReach - random.randrange(0, 25))

    return randomValue

def getPresentFloorY():
    return floor_y - 50

def newPresent(x=None, y=None):
    r = True
    global dropped_prezzies
    if (dropped_prezzies + 1) >= round_boundaries[curr_round] + 5:
        r = False
    else:
        print(f"{(dropped_prezzies + 1)} / {round_boundaries[curr_round] + 5}")
    dropped_prezzies += 1
    screen_objects.append(Present(x or getPosition(), y or 0 , preloaded_images["present"], uuid=uuid.uuid4()))
    return r

print("Present Floor Y: " + str(getPresentFloorY()))

while run:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        run = False

    win.fill((0,0,0))

    score_text = score_font.render(f"Score: {score}/{round_boundaries[curr_round]}", True, (255, 0, 0) if score < round_boundaries[curr_round] else (0, 255, 0))
    win.blit(score_text, (80,50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    presents = [present for present in screen_objects if isinstance(present, Present)]

    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        newPresent(pos[0], pos[1])

    for particle in particles: #Don't ask why I'm trying to add particles I'm bored
        if isinstance(particle, present_particle):
            particle.update()
            particle.draw()

    for obj in screen_objects:
        if isinstance(obj, screen_object):

            if isinstance(obj, Player):
                # Present Collisions
                for present in presents:
                    if present.hitbox.colliderect(obj.hitbox) and not present.uuid in presents_cache:
                        particles.extend([present_particle(obj.x + (obj.sprite.get_width()/2), obj.y + (obj.sprite.get_height()/2), [5, 5], ((200, 150, 50), (255, 200, 100)), 60) for _ in range(10)])
                        score += 1

                        if len(presents_cache) == 10:
                            presents_cache.pop(0)
                        
                        presents_cache.append(present.uuid)
                        screen_objects.remove(present)
                        res = newPresent()
                        if not res:
                            if (curr_round + 2 > len(round_boundaries)) or (score < round_boundaries[curr_round]):
                                sys.exit()
                                run = False
                            curr_round += 1
                            dropped_prezzies = 0
                            score = 0
                            compadre.writeCompadre(curr_round, 3)

            if isinstance(obj, Present):
                stopPoint = getPresentFloorY()
                if obj.y >= stopPoint:
                    newPresent()
                    screen_objects.remove(obj)
                    continue

            obj.update()
    
    pygame.display.update()
pygame.quit()