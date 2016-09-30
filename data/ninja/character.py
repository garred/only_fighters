import itertools
from glob import glob
import others_src.pyganim.pyganim as pyganim
from character import Character
import game
import random
import numpy as np


# Loading all the animation files


# Choosing files to load.
animation_names = ['_'.join(i) for i in itertools.product(
    ['standing', 'walking', 'running', 'hitting'],
    ['front', 'right', 'back'])]

# Loading animations
ninja_animations = {
    name: pyganim.PygAnimation([(file, 0.1) for file in sorted(glob('data/ninja/maps/' + name + '*.png'))])
    for name in animation_names
    }

# Copying right animations and fliping them to create left animations
animation_names_right = ['_'.join(i) for i in itertools.product(['standing', 'walking', 'running', 'hitting'], ['right'])]
__ninja_animations_left = {
    name.replace('right', 'left'):
        pyganim.PygAnimation([(file, 0.1) for file in sorted(glob('data/ninja/maps/' + name + '*.png'))]).flip(True,False)
    for name in animation_names_right
    }

# Merging all animations
ninja_animations = {**ninja_animations, **__ninja_animations_left}

# Setting hitting animations to non-loop animations
for name, animation in ninja_animations.items():
    animation.loop = False if 'hitting' in name else True



# Ninja class


class NinjaCharacter(Character):

    def __init__(self):
        super(NinjaCharacter, self).__init__()

        # Things about ninja behaviour
        self.last_dir = [0,1]   #Direction of the last movement
        self.hitting = False    #Are you hitting?

        # Creating animations (well, copying them from a centralized source)
        self.animations = {name: animation.getCopy() for name, animation in ninja_animations.items()}
        self.animation = self.animations['standing_front']
        self.animation.play()


    def walk(self, dir):
        # You can't move if you are hitting
        if self.hitting and not self.animation.state==pyganim.STOPPED: return
        self.hitting = False

        # Choosing animation
        if dir[1] > 0:
            self.animation = self.animations['walking_front']
        elif dir[1] < 0:
            self.animation = self.animations['walking_back']
        elif dir[0] > 0:
            self.animation = self.animations['walking_right']
        elif dir[0] < 0:
            self.animation = self.animations['walking_left']
        self.animation.play()

        # Moving character
        self.move(dir)


    def run(self, dir):
        # You can't move if you are hitting
        if self.hitting and not self.animation.state==pyganim.STOPPED: return
        self.hitting = False

        # Choosing animation
        if dir[1] > 0:
            self.animation = self.animations['running_front']
        elif dir[1] < 0:
            self.animation = self.animations['running_back']
        elif dir[0] > 0:
            self.animation = self.animations['running_right']
        elif dir[0] < 0:
            self.animation = self.animations['running_left']
        self.animation.play()

        # Moving character
        self.move((dir[0]*2, dir[1]*2))


    def hit(self, dir):
        # You can't move if you are hitting
        if self.hitting and not self.animation.state==pyganim.STOPPED: return
        self.hitting = True

        if dir[0]==0 and dir[1]==0: dir = self.last_dir

        # Choosing animation
        if dir[1] > 0:
            self.animation = self.animations['hitting_front']
        elif dir[1] < 0:
            self.animation = self.animations['hitting_back']
        elif dir[0] > 0:
            self.animation = self.animations['hitting_right']
        elif dir[0] < 0:
            self.animation = self.animations['hitting_left']
        self.animation.play()


    def stand(self):
        # You can't move if you are hitting
        if self.hitting and not self.animation.state==pyganim.STOPPED: return
        self.hitting = False

        # Choosing animation
        if self.last_dir[1] > 0:
            self.animation = self.animations['standing_front']
        elif self.last_dir[1] < 0:
            self.animation = self.animations['standing_back']
        elif self.last_dir[0] > 0:
            self.animation = self.animations['standing_right']
        elif self.last_dir[0] < 0:
            self.animation = self.animations['standing_left']
        else:
            self.animation = self.animations['standing_front']
        self.animation.play()



class NinjaEnemy(NinjaCharacter):

    def __init__(self):
        super(NinjaEnemy, self).__init__()
        self.state = 'waiting'
        self.dir = [0,0]
        self.thinking_time = random.randint(10,200)
        game.ai_objects.append(self)


    def update_ai(self):
        self.thinking_time -= 1

        if self.distance_to(game.player) < 50:
            self.dir = np.sign(self.direction_to(game.player))
            self.hit(self.dir)

        elif self.state == 'waiting':
            if self.thinking_time > 0:
                self.stand()
            else:
                self.state = random.choice(['searching walking', 'searching running'])
                self.dir = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
                self.thinking_time = random.randint(10, 200)

        elif self.state == 'searching walking':
            if self.thinking_time > 0:
                self.walk(self.dir)
            else:
                self.state = 'waiting'
                self.thinking_time = random.randint(10,200)

        elif self.state == 'searching running':
            if self.thinking_time > 0:
                self.run(self.dir)
            else:
                self.state = 'waiting'
                self.thinking_time = random.randint(10, 200)

        else:
            self.stand()

