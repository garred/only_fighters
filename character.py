import pygame
import game
import numpy as np


class Character(pygame.sprite.Sprite):

    def __init__(self):
        super(Character, self).__init__()

        self.image = pygame.Surface((100,100)).convert_alpha()
        self.image.fill((0,0,0,0))

        self.rect = self.image.get_rect()
        self.feet_rect = pygame.Rect(0,0,10,10)
        self.position = game.renderer.map_rect.center

        # Here you should put your animations
        self.animations = {}
        self.animation = None

        # Updating groups
        game.animated_objects.append(self)
        game.render_group.add(self)
        game.collisionable_sprites.append(self)

        # How much this character must bounce when colliding
        self.bounceness = 1


    def kill(self):
        game.render_group.remove(self)
        game.collisionable_sprites.remove(self)
        game.animated_objects.remove(self)
        self.animation.stop()


    def update_animation(self):
        self.image.fill((0,0,0,0))
        centerx = self.rect.width*0.5 - self.animation.getRect().centerx
        centery = self.rect.height*0.5 - self.animation.getRect().centery
        self.animation.blit(self.image, (centerx, centery))


    @property
    def position(self):
        return (self.rect[0], self.rect[1])


    @position.setter
    def position(self, new_pos):
        self.rect[0] = new_pos[0]
        self.rect[1] = new_pos[1]
        self.put_feet_in_rect()


    def put_feet_in_rect(self):
        self.feet_rect.center = self.rect.center


    def put_rect_in_feet(self):
        self.rect.center = self.feet_rect.center


    @property
    def radius(self):
        return self.feet_rect[3] * 0.5


    def move(self, dir):
        self.__move_single_axis((dir[0], 0))
        self.__move_single_axis((0, dir[1]))
        self.last_dir = dir


    def __move_single_axis(self, dir):
        self.position = (self.position[0] + dir[0], self.position[1] + dir[1])

        # We set a maximum number of collision checkings
        for wall_rect in game.collisionable_walls:
            if self.feet_rect.colliderect(wall_rect):
                if dir[0] > 0:  # Moving right; Hit the left side of the wall
                    self.feet_rect.right = wall_rect.left
                if dir[0] < 0:  # Moving left; Hit the right side of the wall
                    self.feet_rect.left = wall_rect.right
                if dir[1] > 0:  # Moving down; Hit the top side of the wall
                    self.feet_rect.bottom = wall_rect.top
                if dir[1] < 0:  # Moving up; Hit the bottom side of the wall
                    self.feet_rect.top = wall_rect.bottom

        self.put_rect_in_feet()


    def bounce(self, other):
        a = np.array(self.feet_rect.center)
        b = np.array(other.feet_rect.center)
        dir = a - b
        dir = dir / np.sqrt(dir.dot(dir))

        new_pos = (self.rect[0] + dir[0]*self.bounceness, self.rect[1] + dir[1]*self.bounceness)
        self.position = new_pos

        new_pos = (other.rect[0] - dir[0] * other.bounceness, other.rect[1] - dir[1] * other.bounceness)
        other.position = new_pos


    def direction_to(self, other):
        a = np.array([self.feet_rect[0], self.feet_rect[1]])
        b = np.array([other.feet_rect[0], other.feet_rect[1]])
        return b-a

    def distance_to(self, other):
        dir = self.direction_to(other)
        return np.sqrt(dir.dot(dir))
