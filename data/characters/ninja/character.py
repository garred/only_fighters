import others_src.pyganim.pyganim as pyganim
from characters import Character, Hitbox, ALL, PLAYER, ENEMY
from characters import load_animations, fast_swing_sounds, slow_swing_sounds, aargh_sounds, fail_hits_sounds, hits_sounds
import game
import random
import numpy as np
from items import LifePotionSmall, Axe, Bow, Knife, Sword


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
        self.attacked = False   #Record if the current attack action has been done (with a hitbox)
        self.tarjet_type = ALL
        self.life = self.max_life = 10
        self.stamina = self.max_stamina = 100
        self.faction = None

        # Creating animations (well, copying them from a centralized source)
        self.animations = {name: animation.getCopy() for name, animation in animations.items()}

        self.set_animation('standing')

        self.is_death = False



    def get_direction_name(self):
        if self.is_looking_down():
            return 'front'
        elif self.is_looking_up():
            return 'back'
        elif self.is_looking_right():
            return 'right'
        elif self.is_looking_left():
            return 'left'
        else:
            return 'front'


    def walk(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = False

        # The character inprove his stamina a bit
        self.stamina = min(self.max_stamina, self.stamina+3)

        self.set_animation('walking')

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

        self.set_animation('running')

        # Moving character
        self.move(self.dir, 1)


    def stand(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = False

        # Character inproves stamina
        self.stamina = min(self.max_stamina, self.stamina+2)

        self.set_animation('standing')


    def hit(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state==pyganim.STOPPED: return
        self.action_locked = True

        self.set_animation('hitting')


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

        self.set_animation('slash')


    def shooting(self):
        # You can't move if you are hitting
        if self.action_locked and not self.animation.state == pyganim.STOPPED: return

        self.set_animation('shooting')


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
        self.set_animation('jumping')


    def death(self):

        if not self.is_death:
            if random.randint(1,8)==1:
                LifePotionSmall(self.position)
            else:
                if self.weapon == 'knife': Knife(self.position)
                if self.weapon == 'sword': Sword(self.position)
                if self.weapon == 'axe': Axe(self.position)
                if self.weapon == 'bow': Bow(self.position)

            self.is_death = True

        # You can't do anything else when you are dying
        self.action_locked = True
        if self.animation_name=='death' and self.animation.state==pyganim.STOPPED:
            self.kill()
        elif self.animation_name != 'death':
            self.set_animation('death')


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
                        Hitbox(pos=self.feet_rect.center, size=20, dir=self.dir, distance=20, tarjet=self.tarjet_type,
                               strength=10, damage=1, type='blunt')
                        random.choice(fast_swing_sounds).play()

                    if 'slash' in self.animation_name:
                        self.attacked = True
                        if self.weapon == 'knife':
                            Hitbox(pos=self.feet_rect.center, size=20, dir=self.dir, distance=20, tarjet=self.tarjet_type,
                                   strength=5, damage=2, type='penetrating')
                            random.choice(fast_swing_sounds).play()
                        elif self.weapon == 'sword':
                            Hitbox(pos=self.feet_rect.center, size=30, dir=self.dir, distance=20, tarjet=self.tarjet_type,
                                   strength=10, damage=4, type='cutting')
                            random.choice(fast_swing_sounds).play()
                        elif self.weapon == 'axe':
                            Hitbox(pos=self.feet_rect.center, size=30, dir=self.dir, distance=30, tarjet=self.tarjet_type,
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



DECISION, WAIT, CHASE, WANDER, PATROL, COMBAT, FLEE = range(7)

class NinjaEnemy(NinjaCharacter):

    def __init__(self):
        super(NinjaEnemy, self).__init__()
        self.tarjet_type = PLAYER
        self.faction = ENEMY

        self.state = WAIT
        self.thinking_time = random.randint(10,200)
        self.tarjet = None
        self.path = None
        self.next_point = -1
        self.origin = None
        self.territory_radius = 200


    def update(self):
        '''Updates the character with artificial intelligence.'''

        super(NinjaEnemy, self).update()

        if self.origin is None: self.origin = self.position


        # Behaviour parameters based on weapon used.

        attack_range = 0
        flee_range = -1
        spot_range = 200
        if self.weapon == 'unarmed' or self.weapon == 'knife':
            attack_range = 30
        elif self.weapon == 'sword':
            attack_range = 40
        elif self.weapon == 'axe':
            attack_range = 50
        elif self.weapon == 'bow':
            attack_range = 200
            flee_range = 100
            spot_range = 300




        self.thinking_time -= 1

        # Choosing tarjet again
        if self.thinking_time <= 0:
            if len(game.players) == 2:
                self.tarjet = game.players[0] if self.distance_to(game.players[0]) < self.distance_to(
                    game.players[1]) else game.players[1]
            elif len(game.players) == 1:
                self.tarjet = game.players[0]
            else:
                self.tarjet = None


        # State machine changes that can happen anytime

        # Yep. It's the enemy really close?
        if self.tarjet is not None and self.distance_to(self.tarjet) < attack_range:
            if self.thinking_time%100 == 0:
                self.dir = self.direction_to(self.tarjet)

            if self.thinking_time <= 0:
                self.slash()
                self.state = COMBAT
                self.thinking_time = random.randint(10, 200)


        # Slower state machine changes

        # Waiting
        if self.state == WAIT:

            self.stand()

            if self.thinking_time%100==0:
                self.dir = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

                # It's the enemy close?
                if self.tarjet is not None and self.distance_to(self.tarjet) < spot_range:
                    self.state = CHASE
                    self.thinking_time = random.randint(10, 100)
                    self.dir = self.direction_to(self.tarjet)

            if self.thinking_time <= 0:
                self.thinking_time = random.randint(10, 200)
                self.state = DECISION

        # Making decisions with your life
        elif self.state == DECISION:
            self.stand()

            if self.thinking_time <= 0:
                self.thinking_time = random.randint(10, 200)

                # Tarjet too close?
                if self.tarjet is not None and self.distance_to(self.tarjet) < flee_range:
                    self.state = FLEE

                # No. Tarjet spoted?
                elif self.tarjet is not None and self.distance_to(self.tarjet) < spot_range:
                    self.state = CHASE
                    self.thinking_time = random.randint(10, 50)
                    self.dir = self.direction_to(self.tarjet)

                # No. Have patrol points?
                elif self.path is not None:
                    self.state = PATROL
                    self.thinking_time = random.randint(200, 500)

                # No. Nothing to do. Just wander around.
                else:
                    self.state = WANDER
                    self.dir = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])

        # Chase that motherfucker
        elif self.state == CHASE:
            if self.tarjet is None:
                self.thinking_time = random.randint(0,5)
                self.state = DECISION

            else:
                if self.tarjet.distance_to(self.origin) > self.territory_radius*3:
                    self.stand()
                elif self.tarjet.distance_to(self.origin) > self.territory_radius*2:
                    self.walk()
                else:
                    self.run()

                if self.thinking_time <= 0 or self.distance_to(self.tarjet) > spot_range:
                    self.thinking_time = random.randint(10, 200)
                    self.dir = self.direction_to(self.tarjet)
                    self.state = WAIT

        elif self.state == WANDER:
            self.walk()
            if self.distance_to(self.origin) > self.territory_radius:
                self.dir = self.direction_to(self.origin)

            if self.thinking_time <= 0:
                self.thinking_time = random.randint(10, 200)
                self.state = WAIT

        elif self.state == PATROL:
            # Are we close to the next point? go to the next
            if self.distance_to(self.path[self.next_point]) < 20:
                self.next_point = (self.next_point+1) % len(self.path)
                self.origin = self.path[self.next_point]

            # Nop. Do we have to decide next action?
            elif self.thinking_time <=0:

                # Yep. It's the enemy close?
                if self.tarjet is not None and self.distance_to(self.tarjet) < spot_range:
                    self.state = CHASE
                    self.thinking_time = random.randint(10, 200)
                    self.dir = self.direction_to(self.tarjet)

                # Nop. Let's wait
                else:
                    self.thinking_time = random.randint(10, 200)
                    self.state = WAIT

            # Nop. Let's walk.
            else:
                self.dir = self.direction_to(self.path[self.next_point])
                self.walk()


        elif self.state == COMBAT:
            self.stand()
            if self.thinking_time <= 0:
                if self.tarjet is not None and 'slash' in self.tarjet.animation_name and not self.action_locked:
                    self.dir = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])
                    self.jump()
                else:
                    self.thinking_time = random.randint(100,200)
                    self.state = random.choice([WAIT, WANDER])
                    self.dir = random.choice([(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)])


        elif self.state == FLEE:
            pass






    def __update(self):

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
            pass #TODO

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