import others_src.pyganim.pyganim as pyganim
from character import Character, Hitbox, ALL, PLAYER, ENEMY
from characters import load_animations, fast_swing_sounds, slow_swing_sounds, aargh_sounds, fail_hits_sounds, hits_sounds
import game
import random
import numpy as np


from pygame.constants import K_LEFT, K_RIGHT, K_UP, K_DOWN, K_m, K_n,  K_a, K_s, K_w, K_d, K_z, K_x, K_SPACE, K_LSHIFT, K_COMMA, K_c


# Loading all the animation files

animations = load_animations('data/characters/ninja/')



# Ninja class

class NinjaCharacter(Character):

    def __init__(self):
        super(NinjaCharacter, self).__init__()

        # Things about ninja behaviour
        self.action_locked = False    #Are you hitting, jumping or slashing?
        self.weapon = 'unarmed'
        self.animation_name = 'standing_front_unarmed'
        self.attacked = False   #Record if the current attack action has been done (with a hitbox)
        self.tarjet = ALL

        # Creating animations (well, copying them from a centralized source)
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}
        self.animation = self.animations[self.animation_name]
        self.animation.play()

        self.life = self.max_life = 10
        self.stamina = self.max_stamina = 100

        self.faction = None


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

        # The character inprove his stamina a bit
        self.stamina = min(self.max_stamina, self.stamina+3)

        # Choosing animation
        self.animation_name = 'walking_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()

        # Moving character
        self.move(self.dir, 0.5)


    def run(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = False

        # Character can't run if it lacks stamina
        self.stamina = max(0, self.stamina-0.5)
        if self.stamina == 0:
            self.walk()
            self.stamina = 0
            return

        # Choosing animation
        self.animation_name = 'running_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()

        # Moving character
        self.move(self.dir, 1)


    def stand(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = False

        # Character inproves stamina
        self.stamina = min(self.max_stamina, self.stamina+2)

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

        if self.weapon == 'bow':
            self.shooting()
            return

        # You can't move if you are hitting
        if self.action_locked and not self.animation.state == pyganim.STOPPED: return
        self.action_locked = True

        # Choosing animation
        self.animation_name = 'slash_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()

    def shooting(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state == pyganim.STOPPED: return

        # Choosing animation
        self.animation_name = 'shooting_' + self.get_direction_name() + 'unarmed'
        self.animation = self.animations[self.animation_name]
        self.animation.play()


    def jump(self):
        # You can't jump if you are tired
        if ('jumping' in self.animation_name and not self.animation.state == pyganim.STOPPED):
            return
        if self.stamina == 0:
            self.walk()
            self.stamina = 0
            return

        self.stamina = max(0, self.stamina - 50)
        self.action_locked = True

        # Choosing animation
        self.animation_name = 'jumping_' + self.get_direction_name() + self.weapon
        self.animation = self.animations[self.animation_name]
        self.animation.play()


    def death(self):
        # You can't do anything else when you are dying
        self.action_locked = True
        if self.animation_name=='death' and self.animation.state==pyganim.STOPPED:
            self.kill()

        # Choosing animation
        self.animation_name = 'death'
        self.animation = self.animations[self.animation_name]
        self.animation.play()


    def update(self):
        '''
        Updates various things related with the animation and the mechanics of the game, like animation-related movement
        (when jumping for example), hitting zones mechanics, and life.
        '''
        super(NinjaCharacter, self).update()

        # Life
        if self.life <= 0:
            if not 'death' in self.animation_name:
                random.choice(aargh_sounds).play()
            self.death()

        else:
            # Jumping movement
            if 'jump' in self.animation_name:
                self.move(self.dir, 1)

            # Hitting zones
            if self.animation.currentFrameNum > (self.animation.numFrames // 3):
                if self.attacked == False:
                    if 'hit' in self.animation_name:
                        self.attacked = True
                        Hitbox(pos=self.feet_rect.center, size=20, dir=self.dir, distance=20, tarjet=self.tarjet,
                               strength=10, damage=1, type='blunt')
                        random.choice(fast_swing_sounds).play()

                    if 'slash' in self.animation_name:
                        self.attacked = True
                        if self.weapon == 'knife':
                            Hitbox(pos=self.feet_rect.center, size=20, dir=self.dir, distance=20, tarjet=self.tarjet,
                                   strength=5, damage=2, type='penetrating')
                            random.choice(fast_swing_sounds).play()
                        elif self.weapon == 'sword':
                            Hitbox(pos=self.feet_rect.center, size=30, dir=self.dir, distance=20, tarjet=self.tarjet,
                                   strength=10, damage=4, type='cutting')
                            random.choice(fast_swing_sounds).play()
                        elif self.weapon == 'axe':
                            Hitbox(pos=self.feet_rect.center, size=30, dir=self.dir, distance=30, tarjet=self.tarjet,
                                   strength=20, damage=8, type='cutting')
                            random.choice(slow_swing_sounds).play()
            else:
                self.attacked = False


    def hitted(self, hitbox):
        if ((self.faction==ENEMY and hitbox.tarjet==ENEMY)
            or (self.faction == PLAYER and hitbox.tarjet == PLAYER)
            or hitbox.tarjet==ALL):
            self.being_hitted = hitbox.strength
            self.being_hitted_direction = hitbox.direction

            # Conditions to avoid the damage
            if ((hitbox.direction[0]*self.dir[0] + hitbox.direction[1]*self.dir[1]) < 0 and ('slash' in self.animation_name or 'hit' in self.animation_name)):
                random.choice(fail_hits_sounds).play()
            elif 'jump' in self.animation_name:
                random.choice(fast_swing_sounds).play()
            else:
                random.choice(hits_sounds).play()
                self.life -= hitbox.damage



class NinjaEnemy(NinjaCharacter):

    def __init__(self):
        super(NinjaEnemy, self).__init__()
        self.state = 'waiting'
        self.thinking_time = random.randint(10,200)
        self.tarjet = PLAYER
        self.faction = ENEMY


    def update(self):
        '''Updates the character with artificial intelligence.'''

        super(NinjaEnemy, self).update()

        self.thinking_time -= 1

        # Choosing tarjet
        if len(game.players) == 2:
            tarjet = game.players[0] if self.distance_to(game.players[0]) < self.distance_to(game.players[1]) else game.players[1]
        elif len(game.players) == 1:
            tarjet = game.players[0]
        else:
            tarjet = None

        # If you have a bow, and tarjet is not very far, use the bow
        if tarjet is not None and self.weapon == 'bow' and self.distance_to(tarjet) < 200:


        # If tarjet is close, reacts
        elif tarjet is not None and self.distance_to(tarjet) < 40:

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
                    self.thinking_time = random.randint(100, 200)

        elif self.state is 'waiting':
            if self.thinking_time > 0:
                self.stand()
            else:
                self.state = random.choice(['searching walking', 'searching running'])
                self.dir = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
                self.thinking_time = random.randint(10, 200)

        elif self.state is 'searching walking':
            if self.thinking_time > 0:
                self.walk()
            else:
                self.state = 'waiting'
                self.thinking_time = random.randint(10,200)

        elif self.state is 'searching running':
            if self.thinking_time > 0:
                self.run()
            else:
                self.state = 'waiting'
                self.thinking_time = random.randint(10, 200)

        else:
            self.stand()


class NinjaPlayer(NinjaCharacter):

    def __init__(self, keymap):
        super(NinjaPlayer, self).__init__()
        self.keymap = keymap
        self.tarjet = ENEMY
        self.faction = PLAYER


    def kill(self):
        super(NinjaPlayer, self).kill()
        game.players.remove(self)


    def update(self):
        '''Makes this character playable.'''

        super(NinjaPlayer, self).update()

        if self.action_locked and self.animation.state == pyganim.STOPPED: self.action_locked = False


        keymap = self.keymap
        keys = game.keys_pressed

        dir = [0, 0]
        if keys[keymap['left']]:
            dir[0] -= 1
        if keys[keymap['right']]:
            dir[0] += 1
        if keys[keymap['up']]:
            dir[1] -= 1
        if keys[keymap['down']]:
            dir[1] += 1
        if np.sum(np.abs(dir))==0: dir = self.dir

        if not self.action_locked: self.dir = dir

        if keys[keymap['hit']]:
            self.hit()
        elif keys[keymap['slash']]:
            self.slash()
        elif keys[keymap['jump']]:
            if not 'jumping' in self.animation_name: self.dir = dir
            self.jump()
        elif keys[keymap['left']] or keys[keymap['right']] or keys[keymap['up']] or keys[keymap['down']]:
            if keys[keymap['run']]:
                self.run()
            else:
                self.walk()
        else:
            self.stand()



keymap1 = {
    'left': K_LEFT, 'right': K_RIGHT, 'up': K_UP, 'down': K_DOWN,
    'hit': K_n, 'run': K_SPACE, 'slash': K_m, 'jump': K_COMMA}
keymap2 = {
    'left': K_a, 'right': K_d, 'up': K_w, 'down': K_s,
    'hit': K_z, 'run': K_LSHIFT, 'slash': K_x, 'jump': K_c}