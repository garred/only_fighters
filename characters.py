import itertools

import pygame
import others_src.pyganim.pyganim as pyganim
import game
import numpy as np


animation_names = ['_'.join(i) for i in itertools.product(
    ['standing', 'walking', 'running', 'jumping', 'hitting', 'dead'],
    ['left', 'right', 'up', 'down'],
    ['unarmed', 'sword'])]

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
        self.feet_rect = pygame.Rect(0,0,25,25)
        self.position = game.renderer.map_rect.center

        self.animation = standing_anim
        self.animation.blit(self.image, (0,0))

        game.render_group.add(self)
        game.animated_objects.append(self)
        game.collisionable_sprites.append(self)

    def __del__(self):
        game.collisionable_sprites.remove(self)

    def update_animation(self):
        self.image.fill((0,0,0,0))
        self.animation.blit(self.image, (0,0))

    @property
    def position(self):
        return (self.rect[0], self.rect[1])

    @position.setter
    def position(self, new_pos):
        self.rect[0] = new_pos[0]
        self.rect[1] = new_pos[1]
        self.feet_rect.centerx = self.rect.centerx
        self.feet_rect.bottom = self.rect.bottom

    @property
    def radius(self):
        return self.feet_rect[3] * 0.5


    def move(self, dx, dy):
        self.__move_single_axis(dx, 0)
        self.__move_single_axis(0, dy)

    def __move_single_axis(self, dx, dy):
        self.position = (self.position[0] + dx, self.position[1] + dy)

        # We set a maximum number of collision checkings
        for wall_rect in game.collisionable_walls:
            if self.feet_rect.colliderect(wall_rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.feet_rect.right = wall_rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.feet_rect.left = wall_rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.feet_rect.bottom = wall_rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.feet_rect.top = wall_rect.bottom

        self.rect.bottom = self.feet_rect.bottom
        self.rect.centerx = self.feet_rect.centerx

    def bounce(self, other):
        a = np.array(self.feet_rect.center)
        b = np.array(other.feet_rect.center)
        dir = a - b
        dir = dir / np.sqrt(dir.dot(dir))
        new_pos = (self.rect[0] + dir[0]*3, self.rect[1] + dir[1]*3)
        self.position = new_pos



DummyCharacter()
player = DummyCharacter()

i = 0