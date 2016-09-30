'''Manages the game mechanics.'''

import numpy as np
import random
import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_LSHIFT, K_SPACE
import pytmx
import pyscroll
import app


def update(keys):
    '''Makes the game seems alive and responsive.'''

    # Processing inputs to control the player
    process_inputs(keys)

    # Updating the relative position of the entities to the camera.
    render_group.update()

    # Updating animated entities
    for o in animated_objects:
        o.update_animation()

    # Updating collisions between characters
    update_collisions_between_sprites()

    # Updating AI
    update_ai()


def process_inputs(keys):
    dir = [0,0]
    if keys[K_LEFT]:
        dir[0] -= 1
    if keys[K_RIGHT]:
        dir[0] += 1
    if keys[K_UP]:
        dir[1] -= 1
    if keys[K_DOWN]:
        dir[1] += 1

    if keys[K_SPACE]:
        player.hit(dir)
    elif keys[K_LEFT] or keys[K_RIGHT] or keys[K_UP] or keys[K_DOWN]:
        if keys[K_LSHIFT]:
            player.run(dir)
        else:
            player.walk(dir)
    else:
        player.stand()


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
                a.move((random.uniform(-1, 1),random.uniform(-1, 1)))
                b.move((random.uniform(-1, 1), random.uniform(-1, 1)))
            elif dis < quadratic_sum_radius:
                dif = (dif / np.sqrt(dis))
                a.move((-dif[0]*a.bounceness,-dif[1]*a.bounceness))
                b.move((dif[0]*b.bounceness, dif[1]*b.bounceness))


def draw():
    '''Draws all the entities and the background.'''

    global player
    app.screen.fill((0, 0, 0))

    # center the map/screen on our Hero
    render_group.center(player.rect.center)

    # draw the map and all sprites
    render_group._spritelist.sort(key=lambda x: x.feet_rect.centery)
    render_group.draw(app.screen)


def update_ai():
    '''Updates all the objects with artificial intelligence.'''
    for o in ai_objects:
        o.update_ai()


# Global objects

# The game mechanics is updating.
active = False
# The game graphics are visible.
visible = True

# Main map.
map = pytmx.util_pygame.load_pygame('data/map/grasslands.tmx')

# "Camera" of the game: it renders objects.'''
renderer = pyscroll.BufferedRenderer(pyscroll.data.TiledMapData(map), app.screen.get_size())
renderer.zoom = 1

# This defines the group of renderizable sprites.
render_group = pyscroll.group.PyscrollGroup(map_layer=renderer, default_layer=2)

# Holds everything that needs to be updated by PygAnim.
animated_objects = list()

# Rectangle of the map.
map_rect = (0, 0, map.width*map.tilewidth, map.height*map.tileheight)

# This contains the walls of the map
collisionable_walls = [pygame.Rect(o.x,o.y, o.width,o.height) for o in map.objects]

# Sprites that can collide between them
collisionable_sprites = list()

# Artificial intelligence objects
ai_objects = list()


# Importing characters used in the game.
from characters import DummyCharacter, NinjaCharacter, NinjaEnemy


# Creating some characters
DummyCharacter()
player = NinjaCharacter()

for i in range(10):
    n = NinjaEnemy()
    n.move((random.randint(-100,100), random.randint(-100,100)))