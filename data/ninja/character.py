import itertools
from glob import glob
import others_src.pyganim.pyganim as pyganim
from character import Character, Hitbox
import game
import random
import numpy as np


from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_m, K_n,  K_a, K_s, K_w, K_d, K_z, K_x, K_SPACE, K_LSHIFT, K_COMMA, K_c


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
    if 'hitting' in name or 'slash' in name or 'jumping' in name:
        animation.loop = False



# Ninja class

class NinjaCharacter(Character):

    def __init__(self):
        super(NinjaCharacter, self).__init__()

        # Things about ninja behaviour
        self.dir = [0,1]
        self.action_locked = False    #Are you hitting, jumping or slashing?
        self.weapon = 'unarmed'
        self.animation_name = 'standing_front_unarmed'
        self.attacked = False   #Record if the current attack action has been done (with a hitbox)
        self.tarjet = Hitbox.ALL

        # Creating animations (well, copying them from a centralized source)
        self.animations = {name: animation.getCopy() for name, animation in ninja_animations.items()}
        self.animation = self.animations[self.animation_name]
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


    def walk(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = False

        # Choosing animation
        self.animation_name = 'walking_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()

        # Moving character
        self.move(self.dir)


    def run(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = False

        # Choosing animation
        self.animation_name = 'running_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()

        # Moving character
        self.move(self.dir, 2)


    def stand(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = False

        # Choosing animation
        self.animation_name = 'standing_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()


    def hit(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = True

        # Choosing animation
        self.animation_name = 'hitting_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()


    def slash(self):
        if self.weapon == 'unarmed':
            self.hit()
            return

        # You can't move if you are hitting
        if self.action_locked and not self.animation.state == pyganim.STOPPED: return
        self.action_locked = True

        # Choosing animation
        self.animation_name = 'slash_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()


    def jump(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state == pyganim.STOPPED: return
        self.action_locked = True

        # Choosing animation
        self.animation_name = 'jumping_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()


    def update(self):
        '''
        Updates various things related with the animation and the mechanics of the game, like animation-related movement
        (when jumping for example) and hitting zones mechanics.
        '''
        super(NinjaCharacter, self).update()

        # Jumping movement
        if 'jumping' in self.animation_name:
            self.move(self.dir, 2)

        # Hitting zones
        if self.animation.currentFrameNum > (self.animation.numFrames // 3):
            if self.attacked == False:
                if 'hit' in self.animation_name:
                    self.attacked = True

                if 'slash' in self.animation_name:
                    self.attacked = True
                    if self.weapon == 'knife':
                        Hitbox(pos=self.feet_rect.center, size=20, dir=self.dir, distance=20, tarjet=self.tarjet,
                               strength=1)
                    elif self.weapon == 'sword':
                        Hitbox(pos=self.feet_rect.center, size=30, dir=self.dir, distance=20, tarjet=self.tarjet,
                               strength=4)
                    elif self.weapon == 'axe':
                        Hitbox(pos=self.feet_rect.center, size=40, dir=self.dir, distance=30, tarjet=self.tarjet,
                               strength=10)
        else:
            self.attacked = False



class NinjaEnemy(NinjaCharacter):

    def __init__(self):
        super(NinjaEnemy, self).__init__()
        self.state = 'waiting'
        self.dir = [0,-1]
        self.thinking_time = random.randint(10,200)
        self.tarjet = Hitbox.PLAYER


    def update(self):
        '''Updates the character with artificial intelligence.'''

        super(NinjaEnemy, self).update()

        self.thinking_time -= 1

        tarjet = game.players[0] if self.distance_to(game.players[0]) < self.distance_to(game.players[1]) else game.players[1]

        if self.distance_to(tarjet) < 40:

            if self.action_locked==False:
                self.dir = self.direction_to(tarjet)  # np.sign(self.diference_to(tarjet))

            if self.thinking_time > 0:
                self.stand()
            else:
                if random.randint(0,4)==0:
                    self.hit()
                    self.thinking_time = 100
                else:
                    self.slash()
                    self.thinking_time = 0#random.randint(100, 200)

        elif self.state == 'waiting':
            if self.thinking_time > 0:
                self.stand()
            else:
                self.state = random.choice(['searching walking', 'searching running'])
                self.dir = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
                self.thinking_time = random.randint(10, 200)

        elif self.state == 'searching walking':
            if self.thinking_time > 0:
                self.walk()
            else:
                self.state = 'waiting'
                self.thinking_time = random.randint(10,200)

        elif self.state == 'searching running':
            if self.thinking_time > 0:
                self.run()
            else:
                self.state = 'waiting'
                self.thinking_time = random.randint(10, 200)

        else:
            self.stand()

    def hitted(self, hitbox):
        if hitbox.tarjet==Hitbox.ENEMIES or hitbox.tarjet==Hitbox.ALL:
            self.being_hitted = 10
            self.being_hitted_direction = hitbox.direction
            self.kill()


class NinjaPlayer(NinjaCharacter):

    def __init__(self, keymap):
        super(NinjaPlayer, self).__init__()
        self.keymap = keymap
        self.tarjet = Hitbox.ALL

    def update(self):
        '''Makes this character playable.'''

        super(NinjaPlayer, self).update()

        dir = [0, 0]
        keymap = self.keymap
        keys = game.keys_pressed

        if keys[keymap['left']]:
            dir[0] -= 1
        if keys[keymap['right']]:
            dir[0] += 1
        if keys[keymap['up']]:
            dir[1] -= 1
        if keys[keymap['down']]:
            dir[1] += 1
        if np.sum(np.abs(dir))==0: dir = self.dir
        self.dir = dir

        if keys[keymap['hit']]:
            self.hit()
        elif keys[keymap['slash']]:
            self.slash()
        elif keys[keymap['jump']]:
            self.jump()
        elif keys[keymap['left']] or keys[keymap['right']] or keys[keymap['up']] or keys[keymap['down']]:
            if keys[keymap['run']]:
                self.run()
            else:
                self.walk()
        else:
            self.stand()


    def hitted(self, hitbox):
        if hitbox.tarjet == Hitbox.PLAYER or hitbox.tarjet == Hitbox.ALL:
            self.being_hitted = 10
            self.being_hitted_direction = hitbox.direction


keymap1 = {
    'left': K_LEFT, 'right': K_RIGHT, 'up': K_UP, 'down': K_DOWN,
    'hit': K_n, 'run': K_SPACE, 'slash': K_m, 'jump': K_COMMA}
keymap2 = {
    'left': K_a, 'right': K_d, 'up': K_w, 'down': K_s,
    'hit': K_z, 'run': K_LSHIFT, 'slash': K_x, 'jump': K_c}