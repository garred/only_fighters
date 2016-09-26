'''Stores global variables and objects.'''

import pygame
from pygame.constants import QUIT, K_ESCAPE


# Initializing all global variables of the App

# Global settings

FPS = 60
'''Frames per second of the application.'''
SCREEN_WIDTH = 800
'''Screen width.'''
SCREEN_HEIGHT = 600
'''Screen height.'''
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
'''Main display where things are drawn.'''
clock = pygame.time.Clock()
'''A clock to control the framerate.'''
running = True
'''True if the app is still running.'''

# Global objects

from menu import menu
import game
import graphics


def run():
    '''Holds the main loop.'''

    global screen

    while running:
        # Reading inputs
        handle_events()

        # Processing next step
        game.update()
        if menu.active: menu.update()

        # Drawing everything
        graphics.draw()
        if menu.active: menu.draw()

        # Waiting to mainting fps.
        clock.tick(FPS)
        pygame.display.flip()


def handle_events():
    '''Handle inputs in general: events, keystrokes and mousestrokes.'''
    global running

    # Handling events. If the event isn't for the game engine, then it should be for the menu.
    for e in pygame.event.get():
        if e.type is QUIT:
            running = False
        elif e.type is pygame.KEYUP and e.key is K_ESCAPE:
            menu.active = 1 - menu.active
        else:
            menu.event(e)

    # Handling keyboard and mouse
    keys_pressed = pygame.key.get_pressed()
    game.process_inputs(keys_pressed)



def quit(*args):
    global running
    running = False


class MyGraphics():
    def __init__(self, screen):
        self.screen = screen
        self.i = 0

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.i += 0.5
        i = int(self.i)
        pygame.draw.circle(self.screen,
                           (255,0,0),
                           ((i//10)*100, (i%10)*100),
                           100)
        if self.i > 100: self.i = 0


class MyGame():
    def update(self):
        pass

    def process_inputs(self, keys):
        pass