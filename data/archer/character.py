import itertools
from glob import glob
import others_src.pyganim.pyganim as pyganim
from data.ninja.character import NinjaCharacter, NinjaEnemy, NinjaPlayer


# Loading all the animation files


# Choosing files to load.

animation_names = ['_'.join(i) for i in itertools.product(
    ['standing', 'walking', 'running', 'hitting', 'jumping', 'shooting', 'throwing'],
    ['front', 'right', 'back'],
    ['unarmed', 'knife', 'sword', 'axe'])]
animation_names = animation_names + ['_'.join(i) for i in itertools.product(
    ['slash'], ['front', 'right', 'back'], ['knife', 'sword', 'axe'])]

# Loading animations
animations = {
    name: pyganim.PygAnimation([(file, 0.1) for file in sorted(glob('data/archer/maps/*' + name + '*.png'))])
    for name in animation_names
    }

# Copying right animations and fliping them to create left animations
animation_names_right = [name for name in animation_names if 'right' in name]
__animations_left = {
    name.replace('right', 'left'):
        pyganim.PygAnimation([(file, 0.1) for file in sorted(glob('data/archer/maps/*' + name + '*.png'))]).flip(True,False)
    for name in animation_names_right
    }

# Merging all animations
animations = {**animations, **__animations_left}

# Setting hitting animations to non-loop animations
for name, animation in animations.items():
    if 'hitting' in name or 'slash' in name or 'jumping' in name:
        animation.loop = False



# Archer class

class ArcherCharacter(NinjaCharacter):

    def __init__(self):
        super(ArcherCharacter, self).__init__()
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}


class ArcherEnemy(NinjaEnemy):

    def __init__(self):
        super(ArcherEnemy, self).__init__()
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}


class ArcherPlayer(NinjaPlayer):

    def __init__(self, keymap):
        super(ArcherPlayer, self).__init__(keymap)
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}