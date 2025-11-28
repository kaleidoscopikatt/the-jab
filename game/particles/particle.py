import pygame
import random
from game.globals import particles, win


class particle():
    def __init__(self, x: float, y: float, scale: list[0: float, 1: float], color_range: tuple[0: tuple[0: int, 1: int, 2: int], 1: tuple[0: int, 1: int, 2: int]], lifespan: int):

        self.color_range = tuple(
            color_range[1][i] - color_range[0][i]
            for i in range(3)
        )

        self.color = tuple(
            random.randint(color_range[0][i], color_range[1][i])
            for i in range(3)
        )

        self.lifespan = lifespan
        self.x, self.y = x, y
        self.scale = scale

    def update(self):
        self.lifespan -= 1
        if self.lifespan == 0:
            self.remove()

    def second_update(self):
        pass

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.scale[0], self.scale[1]))

    def remove(self):
        particles.remove(self)