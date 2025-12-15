## @last-modified: 12:59 19/10/25
## | Merged 'classes' directory into classes.py

import pygame
from game.globals import win
from game.helpers.ImageHelper import generate_hitbox


class screen_object(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite, has_spritesheet = False, sprite_index: int =None):
        super().__init__()
        self.x: float = x
        self.y: float = y
        self.sprite = sprite
        self.has_spritesheet = has_spritesheet
        self.sprite_index = sprite_index

    def update(self):
        self.draw()

    def draw(self):
        if self.has_spritesheet is False:
            win.blit(self.sprite,(self.x,self.y))

        elif self.has_spritesheet is True:
            win.blit(self.sprite[self.sprite_index],(self.x,self.y))

class Player(screen_object):
    def __init__(self, x: float, y: float, sprite, speed=1):
        super().__init__(x, y , sprite)
        self.speed = speed
        self.x: float = x
        self.y: float = y
        self.hitbox = generate_hitbox(self.sprite, self.x, self.y)

    def update(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.x -= self.speed
        elif keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.x += self.speed

        self.hitbox = generate_hitbox(self.sprite, self.x, self.y)
        self.draw()
    
    def draw(self):
        if self.has_spritesheet is False:
            win.blit(self.sprite,(self.x, self.y))

        elif self.has_spritesheet is True:
              win.blit(self.sprite[self.sprite_index],(self.x, self.y))

class Floor(screen_object):
    def __init__(self,x,y,spr):
        super().__init__(x,y,spr,False,None)
        self.hitbox = generate_hitbox(spr, x, y)

    def update(self):
        self.hitbox = generate_hitbox(self.sprite, self.x, self.y)
        self.draw()

    def draw(self):
        win.blit(self.sprite, (self.x, self.y))

class Present(screen_object):
    def __init__(self, x, y, sprite, uuid):
        super().__init__(x, y, sprite) # Why were you parsing vel into this...?
        self.x = x
        self.y = y
        self.sprite = pygame.transform.scale(sprite,(50*2,50*2))
        self.falling: bool = True
        self.hitbox = generate_hitbox(self.sprite, self.x, self.y)
        self.uuid=uuid

    def update(self):
        if self.falling is True:
            self.y += 1

        self.hitbox = generate_hitbox(self.sprite, self.x, self.y)
        self.draw()

    def draw(self):
        win.blit(self.sprite, (self.x,self.y))