import pygame
from math import sqrt
from glob import glob
import others_src.pyganim.pyganim as pyganim
import itertools


ALL, PLAYER, ENEMY = range(3)


class Character(pygame.sprite.Sprite):

    def __init__(self):
        super(Character, self).__init__()

        self.image = pygame.Surface((64,64)).convert_alpha()
        self.image.fill((0,0,0,0))

        self.rect = self.image.get_rect()
        self.feet_rect = pygame.Rect(0,0,10,10)
        self._position = [0.0, 0.0]
        self.position = game.renderer.map_rect.center
        self.dir = [0,1]

        # Here you should put your animations
        self.animations = {}
        self.animation = None

        # Updating groups
        game.animated_objects.append(self)
        game.render_group.add(self)
        game.collisionable_sprites.append(self)

        # How much this character must bounce when colliding
        self.bounceness = 2

        # Attributes to control the effect of being hitted. If being_hitted>0, then it moves in the direction of the hit.
        self.being_hitted = 0
        self.being_hitted_direction = (0,0)

        self.life = -1
        self.max_life = -1
        self.stamina = -1
        self.max_stamina = -1


    def kill(self):
        game.render_group.remove(self)
        game.collisionable_sprites.remove(self)
        game.animated_objects.remove(self)
        self.animation.stop()


    def update(self):
        '''Updates the animation mechanics and draws the rect.'''

        # Updates the hitted animation
        if self.being_hitted > 0:
            self.move(self.being_hitted_direction, distance=2)
            self.being_hitted -= 1

        # Draws the character in his rect
        self.image.fill((0,0,0,0))
        centerx = self.rect.width*0.5 - self.animation.getRect().centerx
        centery = self.rect.height*0.5 - self.animation.getRect().centery
        self.animation.blit(self.image, (centerx, centery))


    def set_animation(self, name):
        if 'shoot' in name:
            weapon = 'unarmed'
            direction = self.get_direction_name()
            self.animation_name = name + '_' + direction + '_' + weapon
        elif 'death' in name:
            self.animation_name = name
        else:
            weapon = self.weapon
            direction = self.get_direction_name()
            self.animation_name = name + '_' + direction + '_' + weapon

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


    def move(self, dir, distance=1):
        self.__move_single_axis((dir[0]*distance, 0))
        self.__move_single_axis((0, dir[1]*distance))


    def __move_single_axis(self, dir):
        self.position = (self._position[0] + dir[0], self._position[1] + dir[1])

        # We set a maximum number of collision checkings
        for wall_rect in game.collisionable_walls:
            if self.feet_rect.colliderect(wall_rect):
                if dir[0] > 0:  # Moving right; Hit the left side of the wall
                    self.feet_rect.right = wall_rect.left
                    self.put_rect_in_feet()
                    self._position[0] = self.rect[0]
                if dir[0] < 0:  # Moving left; Hit the right side of the wall
                    self.feet_rect.left = wall_rect.right
                    self.put_rect_in_feet()
                    self._position[0] = self.rect[0]
                if dir[1] > 0:  # Moving down; Hit the top side of the wall
                    self.feet_rect.bottom = wall_rect.top
                    self.put_rect_in_feet()
                    self._position[1] = self.rect[1]
                if dir[1] < 0:  # Moving up; Hit the bottom side of the wall
                    self.feet_rect.top = wall_rect.bottom
                    self.put_rect_in_feet()
                    self._position[1] = self.rect[1]



    def bounce(self, other):
        dir = [self.feet_rect.center[0]-other.feet_rect.center[0], self.feet_rect.center[1]-other.feet_rect.center[1]]
        dis = sqrt(dir[0]*dir[0] + dir[1]*dir[1])

        if dis == 0:
            mov = random.choice([[0,1],[1,0],[1,1]])
            self.move((-mov[0],-mov[1]))
            other.move(mov)

        elif dis < (self.radius + other.radius):
            dis = 1.0 / dis
            dir = [dir[0]*dis, dir[1]*dis]

            mov = (dir[0]*self.bounceness, dir[1]*self.bounceness)
            self.move(mov)

            mov = (-dir[0]*other.bounceness, -dir[1]*other.bounceness)
            other.move(mov)


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

    def hitted(self, hitbox):
        self.being_hitted = 20
        self.being_hitted_direction = hitbox.direction



class Hitbox(pygame.Rect):
    def __init__(self, pos, size, dir, distance, tarjet=ALL, strength=1, damage=1, type='cutting'):
        pos = (pos[0] + dir[0]*distance, pos[1] + dir[1]*distance)
        self.rect = (pos[0]-size*0.5, pos[1]-size*0.5, size, size)
        super(Hitbox, self).__init__(self.rect)
        self.tarjet = tarjet
        self.strength = strength
        self.damage = damage
        self.direction = dir
        self.type = type

        game.hitboxes.append(self)




# Animations loading helper

def load_animations(path):
    '''Loads all the animations of a character from a file path. Returns a dict with the animations.'''

    # Names of the animations of any character

    animation_names = ['_'.join(i) for i in itertools.product(
        ['standing', 'walking', 'running', 'hitting', 'jumping', 'shooting', 'throwing'],
        ['front', 'right', 'back'],
        ['unarmed', 'knife', 'sword', 'axe'])]
    animation_names += ['_'.join(i) for i in itertools.product(
        ['hitting', 'jumping', 'running', 'standing', 'throwing', 'walking'],
        ['front', 'right', 'back'],
        ['bow'])]
    animation_names += ['_'.join(i) for i in itertools.product(
        ['slash'],
        ['front', 'right', 'back'],
        ['knife', 'sword', 'axe'])]
    animation_names += ['death']

    # Loading animations
    animations = {
        name: pyganim.PygAnimation([(file, 0.1) for file in sorted(glob(path + 'maps/*' + name + '*.png'))])
        for name in animation_names
        }

    # Copying right animations and fliping them to create left animations
    animation_names_right = [name for name in animation_names if 'right' in name]
    __animations_left = {
        name.replace('right', 'left'):
            pyganim.PygAnimation([(file, 0.1) for file in sorted(glob(path + 'maps/*' + name + '*.png'))]).flip(
                True, False)
        for name in animation_names_right
        }

    # Merging all animations
    animations = {**animations, **__animations_left}

    # Setting hitting animations to non-loop animations
    for name, animation in animations.items():
        if ('hitting' in name
            or 'slash' in name
            or 'jumping' in name
            or 'death' in name):
            animation.loop = False

    return animations


# Loading common sounds

hits_sounds, swing_sounds, aargh_sounds, fail_hits_sounds = range(4)

hits_sounds = [pygame.mixer.Sound(file) for file in glob('data/sounds/hits/*.ogg')]
fast_swing_sounds = [pygame.mixer.Sound(file) for file in glob('data/sounds/swing/swing*.ogg')]
slow_swing_sounds = [pygame.mixer.Sound(file) for file in glob('data/sounds/swing/axe*.ogg')]
aargh_sounds = [pygame.mixer.Sound(file) for file in glob('data/sounds/aargh/*.ogg')]
fail_hits_sounds = [pygame.mixer.Sound(file) for file in glob('data/sounds/fail_hits/*.ogg')]

for s in aargh_sounds:
    s.set_volume(0.125)
for s in hits_sounds:
    s.set_volume(1.0)
for s in slow_swing_sounds:
    s.set_volume(1.0)




# Importing the characters

from data.characters.ninja.character import *
from data.characters.archer.character import *
from data.characters.bandit.character import *