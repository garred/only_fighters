from glob import glob
import others_src.pyganim.pyganim as pyganim
import itertools


# Names of the animations of any character

animation_names = ['_'.join(i) for i in itertools.product(
    ['standing', 'walking', 'running', 'hitting', 'jumping', 'shooting', 'throwing'],
    ['front', 'right', 'back'],
    ['unarmed', 'knife', 'sword', 'axe'])]
animation_names += ['_'.join(i) for i in itertools.product(
    ['slash'],
    ['front', 'right', 'back'],
    ['knife', 'sword', 'axe'])]
animation_names += ['death']



# Animations loading helper

def load_animations(path):
    '''Loads all the animations of a character from a file path. Returns a dict with the animations.'''

    global animation_names

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
        if 'hitting' in name or 'slash' in name or 'jumping' in name or 'death' in name:
            animation.loop = False

    return animations



# Importing the characters

from data.characters.ninja.character import *
from data.characters.archer.character import *
from data.characters.bandit.character import *