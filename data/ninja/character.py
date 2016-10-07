import itertools
from glob import glob
import others_src.pyganim.pyganim as pyganim
from character import Character
import game
import random
import numpy as np

from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_m, K_n,  K_a, K_s, K_w, K_d, K_z, K_x, K_SPACE, K_LSHIFT


# Loading all the animation files


# Choosing files to load.

animation_names = ['_'.join(i) for i in itertools.product(
    ['standing', 'walking', 'running', 'hitting', 'jumping', 'shooting', 'throwing'],
    ['front', 'right', 'back'],
    ['unarmed', 'knife', 'sword', 'axe'])]
animation_names = animation_names + ['_'.join(i) for i in itertools.product(
    ['slash'], ['front', 'right', 'back'], ['knife', 'sword', 'axe'])]

# Loading animations
ninja_animations = {
    name: pyganim.PygAnimation([(file, 0.1) for file in sorted(glob('data/ninja/maps/' + name + '*.png'))])
    for name in animation_names
    }

# Copying right animations and fliping them to create left animations
animation_names_right = [name for name in animation_names if 'right' in name]
__ninja_animations_left = {
    name.replace('right', 'left'):
        pyganim.PygAnimation([(file, 0.1) for file in sorted(glob('data/ninja/maps/' + name + '*.png'))]).flip(True,False)
    for name in animation_names_right
    }

# Merging all animations
ninja_animations = {**ninja_animations, **__ninja_animations_left}

# Setting hitting animations to non-loop animations
for name, animation in ninja_animations.items():
    animation.loop = False if 'hitting' in name or 'slash' in name else True



# Ninja class

class NinjaCharacter(Character):

    def __init__(self):
        super(NinjaCharacter, self).__init__()

        # Things about ninja behaviour
        self.last_dir = [0,1]   #Direction of the last movement
        self.hitting = False    #Are you hitting?
        self.weapon = 'unarmed'

        # Creating animations (well, copying them from a centralized source)
        self.animations = {name: animation.getCopy() for name, animation in ninja_animations.items()}
        self.animation = self.animations['standing_front_unarmed']
        self.animation.play()


    def get_direction_name(self):
        if self.is_looking_down():
            return 'front_'
        elif self.is_looking_up():
            return 'back_'
        elif self.is_looking_right():
            return 'right_'
        elif self.is_looking_left():
            return 'left_'
        else:
            return 'front_'


    def update_direction(self, dir):
        if dir==None:
            if self.last_dir[0] == 0 and self.last_dir[1] == 0: self.last_dir = [0, -1]
        else:
            if dir[0]==0 and dir[1]==0: dir = self.last_dir
            if dir[0]==0 and dir[1]==0: dir = [0,-1]
            self.last_dir = dir


    def walk(self, dir):
        # You can't move if you are hitting
        if self.hitting and not self.animation.state==pyganim.STOPPED: return
        self.hitting = False

        self.update_direction(dir)

        # Choosing animation
        animation_name = 'walking_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[animation_name]
        self.animation.play()

        # Moving character
        self.move(dir)


    def run(self, dir):
        # You can't move if you are hitting
        if self.hitting and not self.animation.state==pyganim.STOPPED: return
        self.hitting = False

        self.update_direction(dir)

        # Choosing animation
        animation_name = 'running_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[animation_name]
        self.animation.play()

        # Moving character
        self.move((dir[0]*2, dir[1]*2))


    def stand(self, dir):
        # You can't move if you are hitting
        if self.hitting and not self.animation.state==pyganim.STOPPED: return
        self.hitting = False

        self.update_direction(dir)

        # Choosing animation
        animation_name = 'standing_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[animation_name]
        self.animation.play()


    def hit(self, dir):
        # You can't move if you are hitting
        if self.hitting and not self.animation.state==pyganim.STOPPED: return
        self.hitting = True

        self.update_direction(dir)

        # Choosing animation
        animation_name = 'hitting_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[animation_name]
        self.animation.play()


    def slash(self, dir):
        if self.weapon == 'unarmed':
            self.hit(dir)
            return

        # You can't move if you are hitting
        if self.hitting and not self.animation.state == pyganim.STOPPED: return
        self.hitting = True

        self.update_direction(dir)

        # Choosing animation
        animation_name = 'slash_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[animation_name]
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

        tarjet = game.players[0] if self.distance_to(game.players[0]) < self.distance_to(game.players[1]) else game.players[1]

        if self.distance_to(tarjet) < 25:
            self.dir = self.direction_to(tarjet)#np.sign(self.diference_to(tarjet))
            if self.thinking_time > 0:
                self.stand(self.dir)
            else:
                self.hit(self.dir)
                self.thinking_time = random.randint(10,40)

        elif self.distance_to(tarjet) < 50:
            self.dir = self.direction_to(tarjet)#np.sign(self.diference_to(tarjet))
            if self.thinking_time > 0:
                self.stand(self.dir)
            else:
                self.slash(self.dir)
                self.thinking_time = random.randint(10, 100)

        elif self.state == 'waiting':
            if self.thinking_time > 0:
                self.stand(self.dir)
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
            self.stand(self.dir)


class NinjaPlayer(NinjaCharacter):
    def __init__(self, keymap):
        super(NinjaPlayer, self).__init__()
        self.keymap = keymap

    def process_inputs(self, keys):
        dir = [0, 0]
        keymap = self.keymap

        if keys[keymap['left']]:
            dir[0] -= 1
        if keys[keymap['right']]:
            dir[0] += 1
        if keys[keymap['up']]:
            dir[1] -= 1
        if keys[keymap['down']]:
            dir[1] += 1

        if keys[keymap['hit']]:
            self.hit(dir)
        elif keys[keymap['slash']]:
            self.slash(dir)
        elif keys[keymap['left']] or keys[keymap['right']] or keys[keymap['up']] or keys[keymap['down']]:
            if keys[keymap['run']]:
                self.run(dir)
            else:
                self.walk(dir)
        else:
            self.stand(dir)

keymap1 = {'left': K_LEFT, 'right': K_RIGHT, 'up': K_UP, 'down': K_DOWN, 'hit': K_n, 'run': K_SPACE, 'slash': K_m}
keymap2 = {'left': K_a, 'right': K_d, 'up': K_w, 'down': K_s, 'hit': K_z, 'run': K_LSHIFT, 'slash': K_x}