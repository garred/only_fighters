'''Manages the game mechanics.'''

import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN
import pytmx
import pyscroll

import random

import app



def update(keys):
    '''Makes the game seems alive and responsive.'''

    # Processing inputs
    if keys[K_LEFT]:
        player.move(-10,0)
    if keys[K_RIGHT]:
        player.move(10,0)
    if keys[K_UP]:
        player.move(0,-10)
    if keys[K_DOWN]:
        player.move(0,10)

    # Updating the relative position of the entities to the camera.
    render_group.update()

    # Updating animated entities
    for o in animated_objects:
        o.update_animation()

    # Updating collisions between characters
    update_collisions_between_sprites()



def update_collisions_between_sprites():
    for a in collisionable_sprites:
        for b in collisionable_sprites:
            if a is b: continue
            quadratic_sum_radius = a.radius + b.radius
            quadratic_sum_radius *= quadratic_sum_radius
            va = np.array(a.feet_rect.center)
            vb = np.array(b.feet_rect.center)
            dif = vb - va
            dis = dif.dot(dif)
            if dis == 0:
                a.move(random.uniform(-1, 1),random.uniform(-1, 1))
                b.move(random.uniform(-1, 1), random.uniform(-1, 1))
            elif dis < quadratic_sum_radius:
                dif = 5.0*(dif / np.sqrt(dis))
                a.move(-dif[0],-dif[1])
                b.move(dif[0], dif[1])


def draw():
    '''Draws all the entities and the background.'''

    global player
    app.screen.fill((0, 0, 0))

    # center the map/screen on our Hero
    render_group.center(player.rect.center)

    # draw the map and all sprites
    render_group._spritelist.sort(key=lambda x: x.feet_rect.centery)
    render_group.draw(app.screen)


active = False
'''The game mechanics is updating.'''
visible = True
'''The game graphics are visible.'''


map = pytmx.util_pygame.load_pygame('data/map/grasslands.tmx')
'''Main map.'''


renderer = pyscroll.BufferedRenderer(
    pyscroll.data.TiledMapData(map),
    app.screen.get_size())
'''"Camera" of the game: it renders objects.'''
renderer.zoom = 1


render_group = pyscroll.group.PyscrollGroup(
    map_layer=renderer,
    default_layer=2)
'''This defines the group of renderizable sprites.'''

animated_objects = list()
'''Holds everything that needs to be updated by PygAnim.'''


map_rect = (0, 0, map.width*map.tilewidth, map.height*map.tileheight)
'''Rectangle of the map.'''


collisionable_walls = [pygame.Rect(o.x,o.y, o.width,o.height) for o in map.objects]
'''This contains the walls of the map'''

collisionable_sprites = []


# Importing characters used in the game.
from characters import *
