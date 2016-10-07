'''Manages the game mechanics.'''

import numpy as np
import random
import pygame
import pytmx
import pyscroll
import app
from pygame.constants import K_1, K_2

def update(keys):
    '''Makes the game seems alive and responsive.'''

    # Processing inputs to change things in the game
    process_inputs(keys)
    # Processing inputs to control the player
    for player in players:
        player.process_inputs(keys)

    # Updating the relative position of the entities to the camera.
    render_group.update()

    # Updating collisions between characters
    update_collisions_between_sprites()

    # Updating AI
    update_ai()

    # Updating animated entities
    for o in animated_objects:
        o.update_animation()



def process_inputs(keys):
    '''Input processing related to the game as a whole.'''

    if keys[K_1]:
        renderer.zoom *= 1.05
    if keys[K_2]:
        renderer.zoom /= 1.05


def update_collisions_between_sprites():
    '''Updates collisions between sprites, in a completly unefficient way.'''

    for a in collisionable_sprites:
        for b in collisionable_sprites:
            if a is b: continue
            a.bounce(b)
            b.bounce(a)


def draw():
    '''Draws all the entities and the background.'''

    global player
    app.screen.fill((0, 0, 0))

    # center the map/screen on our Hero
    render_group.center(players[0].rect.center)

    # draw the map and all sprites
    render_group._spritelist.sort(key=lambda x: x.feet_rect.centery) #Sorting sprites by depth.
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
from characters import DummyCharacter, NinjaCharacter, NinjaEnemy, NinjaPlayer, keymap1, keymap2


# Creating some characters
#DummyCharacter()
player1 = NinjaPlayer(keymap1)
player1.weapon = 'sword'
player2 = NinjaPlayer(keymap2)
player2.weapon = 'axe'
players = [player1, player2]

for i in range(10):
    n = NinjaEnemy()
    n.move((random.randint(-100,100), random.randint(-100,100)))
    n.weapon = random.choice(['unarmed', 'knife', 'sword', 'axe'])