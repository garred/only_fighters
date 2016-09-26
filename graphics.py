'''Manages things related with the graphics.'''

import pygame

import app


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