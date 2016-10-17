import pygame
import game
import numpy as np
import math
import random
import app


class Character(pygame.sprite.Sprite):

    def __init__(self):
        super(Character, self).__init__()

        self.image = pygame.Surface((100,100)).convert_alpha()
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
        a = np.array(self.feet_rect.center)
        b = np.array(other.feet_rect.center)
        dir = a - b
        dis = np.sqrt(dir.dot(dir))
        if dis == 0:
            mov = random.choice([[0,1],[1,0],[1,1]])

            new_pos = (self.rect[0] + mov[0], self.rect[1] + mov[1])
            self.position = new_pos
            new_pos = (other.rect[0] - mov[0], other.rect[1] - mov[1])
            other.position = new_pos
        elif dis < (self.radius + other.radius):
            dir = dir / dis

            new_pos = (self.rect[0] + dir[0]*self.bounceness, self.rect[1] + dir[1]*self.bounceness)
            self.position = new_pos

            new_pos = (other.rect[0] - dir[0] * other.bounceness, other.rect[1] - dir[1] * other.bounceness)
            other.position = new_pos


    def diference_to(self, other):
        a = np.array([self.feet_rect[0], self.feet_rect[1]])
        b = np.array([other.feet_rect[0], other.feet_rect[1]])
        return b-a


    def distance_to(self, other):
        dir = self.diference_to(other)
        return np.sqrt(dir.dot(dir))


    def direction_to(self, other):
        return self.diference_to(other) / self.distance_to(other)


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
    ALL, PLAYER, ENEMIES = range(3)

    def __init__(self, pos, size, dir, distance, tarjet=ALL, strength=1):
        pos = (pos[0] + dir[0]*distance, pos[1] + dir[1]*distance)
        self.rect = (pos[0]-size*0.5, pos[1]-size*0.5, size, size)
        super(Hitbox, self).__init__(self.rect)
        self.tarjet = tarjet
        self.strength = strength
        self.direction = dir

        game.hitboxes.append(self)



