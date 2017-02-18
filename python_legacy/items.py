import pygame
import game
from math import sqrt
import others_src.pyganim.pyganim as pyganim
from glob import glob
from characters import PLAYER




class Item(pygame.sprite.Sprite):

    def __init__(self, pos):
        super(Item, self).__init__()

        self.image = pygame.Surface((64,64)).convert_alpha()
        self.image.fill((0,0,0,0))

        self.rect = self.image.get_rect()
        self.feet_rect = pygame.Rect(0,0,10,10)
        self._position = [0.0, 0.0]
        self.position = pos if pos is not None else game.renderer.map_rect.center

        self.dir = [0,1]
        self.taken = False

        # Here you should put your animations
        self.animations = {}
        self.animation = None

        # Updating groups
        game.animated_objects.append(self)
        game.render_group.add(self)
        game.touchable_objects.append(self)


    def kill(self):
        game.render_group.remove(self)
        game.touchable_objects.remove(self)
        game.animated_objects.remove(self)
        self.animation.stop()


    def update(self):
        '''Updates the animation mechanics and draws the rect.'''

        # Draws the character in his rect
        self.image.fill((0,0,0,0))
        centerx = self.rect.width*0.5 - self.animation.getRect().centerx
        centery = self.rect.height*0.5 - self.animation.getRect().centery
        self.animation.blit(self.image, (centerx, centery))


    def touched_by(self, character):
        dis = self.distance_to(character)
        if dis < 20:
            self.set_animation('touch')


    def set_animation(self, name):
        self.animation_name = name
        self.animation = self.animations[self.animation_name]
        self.animation.play()



    @property
    def position(self):
        return (self._position[0], self._position[1])


    @position.setter
    def position(self, new_pos):
        self._position[0] = new_pos[0]
        self._position[1] = new_pos[1]
        self.rect[0] = self._position[0]
        self.rect[1] = self._position[1]
        self.put_feet_in_rect()


    def put_feet_in_rect(self):
        self.feet_rect.center = self.rect.center


    def put_rect_in_feet(self):
        self.rect.center = self.feet_rect.center


    @property
    def radius(self):
        return self.feet_rect[3]


    def diference_to(self, other):
        try:
            return [other.feet_rect[0]-self.feet_rect[0], other.feet_rect[1]-self.feet_rect[1]]
        except AttributeError:
            return [other[0] - self.feet_rect[0], other[1] - self.feet_rect[1]]


    def distance_to(self, other):
        dir = self.diference_to(other)
        return sqrt(dir[0]*dir[0] + dir[1]*dir[1])


    def direction_to(self, other):
        dif = self.diference_to(other)
        try:
            dis = 1.0 / self.distance_to(other)
        except ZeroDivisionError:
            dis = 0
        dir = [dif[0]*dis, dif[1]*dis]
        return dir


    def is_looking_right(self):
        return self.dir[0] - abs(self.dir[1]) >= 0

    def is_looking_down(self):
        return self.dir[1] - abs(self.dir[0]) >= 0

    def is_looking_left(self):
        return abs(self.dir[1]) + self.dir[0] <= 0

    def is_looking_up(self):
        return abs(self.dir[0]) + self.dir[1] <= 0



def load_animations(path, item_name):
    '''Loads all the animations of an item from a file path. Returns a dict with the animations.'''

    # Names of the animations of any character

    animation_names = ['stand', 'touch']

    # Loading animations
    animations = {
        name: pyganim.PygAnimation([(file, 0.1) for file in sorted(glob(path + 'maps/*' + item_name + '*' + name + '*.png'))])
        for name in animation_names
        }

    return animations



from data.items.life_small.item import *
from data.items.axe.item import *
from data.items.bow.item import *
from data.items.knife.item import *
from data.items.sword.item import *



class Portal(Item):

    animations = {
        name: pyganim.PygAnimation([(file, 0.1) for file in sorted(glob('data/items/portal/*.png'))])
        for name in ['stand','touch']
        }

    def __init__(self, pos):
        super(Portal, self).__init__(pos)
        self.animations = {name: animation.getCopy() for name, animation in Portal.animations.items()}
        self.animation = None
        self.set_animation('stand')


    def touched_by(self, character):
        dis = self.distance_to(character)
        if character.faction == PLAYER and dis < 50:
            game.load_map('data/maps/'+self.to_map)
