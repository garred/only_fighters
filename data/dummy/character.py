import pygame
import others_src.pyganim.pyganim as pyganim

from character import Character


standing_anim = pyganim.PygAnimation(
    [('data/dummy/standin_000.png', 0.1),
     ('data/dummy/standin_001.png', 0.1),
     ('data/dummy/standin_002.png', 0.1),
     ('data/dummy/standin_003.png', 0.1),
     ('data/dummy/standin_004.png', 0.1),
     ('data/dummy/standin_005.png', 0.1)]
)
'''An animation of a standing character.'''
standing_anim.play()


class DummyCharacter(Character):
    def __init__(self):
        super(DummyCharacter, self).__init__()
        self.animation = standing_anim
        self.feet_rect = pygame.Rect(0, 0, 30, 30)
        self.put_feet_in_rect()

    def put_feet_in_rect(self):
        self.feet_rect.centerx = self.rect.centerx
        self.feet_rect.bottom = self.rect.bottom
    def put_rect_in_feet(self):
        self.rect.centerx = self.feet_rect.centerx
        self.rect.bottom = self.feet_rect.bottom

    def walk(self, dir):
        pass

    def run(self, dir):
        pass