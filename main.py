import os
import random

import compadre
import uuid

from game.classes import Player, screen_object, Floor, Present
from game.globals import win, Assets

try:
    import pygame
except ModuleNotFoundError as e:
    os.system("pip install pygame --user")

TRIES_TO_RESET = 3

pygame.display.set_caption("Santa's Present-Catcher!")

run = True

compadre.boot(TRIES_TO_RESET) # Three tries until it retries...
pygame.init()

preloaded_images = Assets()

floor_y = 900

screen_objects = [Player(500,floor_y-preloaded_images["player"].get_height(), preloaded_images["player"]),
                  Floor(0,floor_y,preloaded_images["floor"]),
                  Floor(500,floor_y,preloaded_images["floor"]),
                  Floor(1000,floor_y,preloaded_images["floor"]),
                  Floor(1500,floor_y,preloaded_images["floor"]),
                  Present(random.randint(0,2000), 0, preloaded_images["present"], uuid=uuid.uuid4())
                  ]

presents = []
presents_cache = []

score = 0
score_font = pygame.font.SysFont("jetbrains_mono", 30) # No, we're not using comic_sans.
score_text = score_font.render(f"Score: {score}", True, (255,0,0))

def getPresentFloorY():
    return floor_y - 50

def newPresent(x=None, y=None):
    screen_objects.append(Present(x or compadre.getCompadre(screen_objects[0].x, floorWidth=500*4),y or 0, preloaded_images["present"], uuid=uuid.uuid4()))

print("Present Floor Y: " + str(getPresentFloorY()))

while run:
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        run = False

    win.fill((0,0,0))

    score_text = score_font.render(f"Score: {score}", True, (255, 0, 0))
    win.blit(score_text, (80,50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    presents = [present for present in screen_objects if isinstance(present, Present)]

    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        newPresent(pos[0], pos[1])

    for obj in screen_objects:
        if isinstance(obj, screen_object):
            obj.update()

            if isinstance(obj, Player):
                # Present Collisions
                for present in presents:
                    if present.hitbox.colliderect(obj.hitbox) and not present.uuid in presents_cache:
                        if len(presents_cache) == 10:
                            presents_cache.pop(0)
                        
                        presents_cache.append(present.uuid)
                        screen_objects.remove(present)
                        newPresent()

                        score += 1

            if isinstance(obj, Present):
                stopPoint = getPresentFloorY()
                if obj.y >= stopPoint:
                    newPresent()
                    screen_objects.remove(obj)
                    break

    pygame.display.update()
pygame.quit()