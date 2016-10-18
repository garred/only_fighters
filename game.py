'''Manages the game mechanics.'''

import numpy as np
import random
import pygame
import pytmx
import pyscroll
import app
from pygame.constants import K_1, K_2
from character import Hitbox

keys_pressed = {}


def update():
    '''Makes the game seems alive and responsive.'''
    global keys_pressed

    keys_pressed = pygame.key.get_pressed() # Needed to handling keyboard and mouse events

    # Processing inputs
    process_inputs()

    # Updating things in the game
    render_group.update() #Updating the relative position of the entities to the camera.
    update_collisions_between_sprites()
    update_objects()
    update_hitboxes()


def update_hitboxes():
    global hitboxes, animated_objects
    for h in hitboxes:
        for o in animated_objects:
            if h.colliderect(o.feet_rect):
                o.hitted(h)
    # TODO: Restore this
    hitboxes = list()


def update_objects():
    for o in animated_objects:
        o.update()



def process_inputs():
    '''Input processing related to the game as a whole.'''
    global keys_pressed

    if keys_pressed[K_1]:
        renderer.zoom *= 1.05
    if keys_pressed[K_2]:
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

    app.screen.fill((0, 0, 0))

    # center the map/screen on our Heroes
    if players[0] is not None and players[1] is not None:
        center = ((players[0].rect.centerx + players[1].rect.centerx)*0.5,
                  (players[0].rect.centery+players[1].rect.centery)*0.5)
        render_group.center(center)
    else:
        render_group.center(players[0].rect.center)


    # draw the map and all sprites
    render_group._spritelist.sort(key=lambda x: x.feet_rect.centery) #Sorting sprites by depth.
    render_group.draw(app.screen)


    # Draw information about players' life, stamina, etc.
    draw_players_info()

    # # TODO: CLEAN THIS CODE WHEN DEBUGGING CHARACTERS IS NO LONGER NEEDED
    # # Raw way of rendering things for debuging
    # camx = -player1.rect.centerx+app.screen_width*0.5
    # camy = -player1.rect.centery+app.screen_height*0.5
    #
    # for h in hitboxes:
    #     rect = (h.rect[0]+camx, h.rect[1]+camy, h.rect[2], h.rect[3])
    #     pygame.draw.rect(app.screen, (255, 0, 0), rect)
    # hitboxes = list()
    #
    # for e in animated_objects:
    #     rect = (e.feet_rect[0]+camx, e.feet_rect[1]+camy, e.feet_rect[2], e.feet_rect[3])
    #     pygame.draw.rect(app.screen, (0, 255, 0), rect)


def draw_players_info():
    render_group.center((0,0))

    # Player 1 info
    pygame.draw.rect(app.screen, (  0,  0,  0), (20, 20, 200, 20))
    if players[0].life > 0: pygame.draw.rect(app.screen, (255,  0,  0), (23, 23, 194*max(0,players[0].life)/players[0].max_life, 14))
    pygame.draw.rect(app.screen, (  0,  0,  0), (20, 40, 200, 20))
    pygame.draw.rect(app.screen, (255,255,255), (23, 43, 194*max(0,players[0].stamina)/players[0].max_stamina, 14))

    # Player 2 info
    if players[1] is not None:
        pygame.draw.rect(app.screen, (  0,  0,  0), (app.screen_width-20-200, 20, 200, 20))
        if players[1].life > 0: pygame.draw.rect(app.screen, (255,  0,  0), (app.screen_width-17-200, 23, 194*players[1].life/players[1].max_life, 14))
        pygame.draw.rect(app.screen, (  0,  0,  0), (app.screen_width-20-200, 40, 200, 20))
        pygame.draw.rect(app.screen, (255,255,255), (app.screen_width-17-200, 43, 194*max(0, players[1].stamina)/players[1].max_stamina, 14))



# Global objects

# The game mechanics is updating.
active = False
# The game graphics are visible.
visible = True

# Main map.
map = pytmx.util_pygame.load_pygame('data/maps/map1/grasslands.tmx')

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
collisionable_walls = [pygame.Rect(o.x,o.y, o.width,o.height) for o in map.layernames['walls']]

# Sprites that can collide between them
collisionable_sprites = list()

# Hitbox objects
hitboxes = list()


# Importing characters used in the game.
from characters import NinjaPlayer, ArcherPlayer, BanditEnemy, keymap1, keymap2


# Creating some characters
player1 = NinjaPlayer(keymap1)
player1.weapon = 'sword'
player2 = ArcherPlayer(keymap2)
player2.weapon = 'axe'
players = [player1, player2]

for i in range(10):
    n = BanditEnemy()
    n.move((random.randint(-100,100), random.randint(100,200)))
    n.weapon = random.choice(['unarmed', 'knife', 'sword', 'axe'])