'''Manages the game mechanics.'''

import pygame
from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN
import pytmx
import pyscroll
import others_src.pyganim.pyganim as pyganim

import app


active = False
'''The game is updating.'''
visible = True
'''The game graphics are visible.'''


map = pytmx.util_pygame.load_pygame('data/map/grasslands.tmx')
'''Main map.'''

renderer = pyscroll.BufferedRenderer(
    pyscroll.data.TiledMapData(map),
    app.screen.get_size())
'''"Camera" of the game: render objects.'''
renderer.zoom = 1

render_group = pyscroll.group.PyscrollGroup(
    map_layer=renderer,
    default_layer=2)
'''This defines the group of renderizable objects.'''


standing_anim = pyganim.PygAnimation(
    [('data/standing/standin_000.png', 0.1),
     ('data/standing/standin_001.png', 0.1),
     ('data/standing/standin_002.png', 0.1),
     ('data/standing/standin_003.png', 0.1),
     ('data/standing/standin_004.png', 0.1),
     ('data/standing/standin_005.png', 0.1)]
)
'''An animation of a standing character.'''
standing_anim.play()


class DummyCharacter(pygame.sprite.Sprite):
    def __init__(self):
        super(DummyCharacter, self).__init__()

        self.image = pygame.Surface((100,100)).convert_alpha()
        self.image.fill((0,0,0,0))

        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = renderer.map_rect.center

        self.animation = standing_anim
        self.animation.blit(self.image, (0,0))

        render_group.add(self)

    def update_animation(self):
        self.image.fill((0,0,0,0))
        self.animation.blit(self.image, (0,0))

animated_objects = list()

character = DummyCharacter()
animated_objects.append(character)

i = 0


def update():
    # Updating the relative position of the entities.
    render_group.update()

    # Updating animated entities
    for o in animated_objects:
        o.update_animation()


def process_inputs(keys):
    if keys[K_LEFT]:
        character.rect[0] -= 10
    if keys[K_RIGHT]:
        character.rect[0] += 10
    if keys[K_UP]:
        character.rect[1] -= 10
    if keys[K_DOWN]:
        character.rect[1] += 10


def draw():
    global i, character
    app.screen.fill((0, 0, 0))

    i += 0.05
    x = int(i/10)*100
    y = int(i%10)*100

    # Draws the map
    # center the map/screen on our Hero
    render_group.center(character.rect.center)
    # draw the map and all sprites
    render_group.draw(app.screen)


    # Draws a big moving dot
    pygame.draw.circle(app.screen,
                       (255,0,0),
                       (x, y), 10)
    if i > 100: i = 0

