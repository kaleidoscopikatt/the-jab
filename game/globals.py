## @last-modified: 12:56 19/10/25
## | Renamed to globals.py as to avoid using too many arbitrary files.

#This exists to avoid a circular import
import pygame
import os

image_types = ['png']

cwd = os.getcwd()
win = pygame.display.set_mode((0,0),0,pygame.FULLSCREEN)
assets_directory = os.path.join(cwd, 'game\\assets')

def Assets() -> dict[str, pygame.Surface]:
    files = os.listdir(assets_directory)
    preloadedAssets = {}

    for file in files:
        path, ext = os.path.basename(file).split(os.path.extsep)

        if ext in image_types:
            preloadedAssets[path] = pygame.image.load(os.path.join(assets_directory, file))
    return preloadedAssets