'''Manages the game mechanics.'''

import pytmx
import pyscroll
import pygame

import app


map = pytmx.util_pygame.load_pygame('data/map/grasslands.tmx')
'''Main map.'''

camera = pyscroll.BufferedRenderer(pyscroll.data.TiledMapData(map),
                                   app.screen.get_size())
'''Camera of the game: rendered objects are relative to this entity.'''
camera.zoom = 1


def update():
    pass

def process_inputs(keys):
    pass



i = 0

def draw():
    global i

    app.screen.fill((0, 0, 0))
    i += 0.5
    _i = int(i)
    pygame.draw.circle(app.screen,
                       (255,0,0),
                       ((_i//10)*100, (_i%10)*100),
                       100)
    if i > 100: i = 0