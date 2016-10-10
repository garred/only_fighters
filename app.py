'''Stores global variables and objects.'''

import pygame
from pygame.constants import QUIT, K_ESCAPE


# Initializing all global variables of the App

# Global settings

fps = 60
'''Frames per second of the application.'''
screen_width = 800
'''Screen width.'''
screen_height = 600
'''Screen height.'''
screen = pygame.display.set_mode((screen_width, screen_height))
'''Main display where things are drawn.'''
clock = pygame.time.Clock()
'''A clock to control the framerate.'''
running = True
'''True if the app is still running.'''

# Global objects

from menu import menu
import game




def run():
    '''Holds the main loop.'''

    while running:
        # Reading inputs from the user
        handle_events()

        # Processing next step
        if game.active: game.update()
        if menu.active: menu.update()

        # Drawing everything
        if game.visible: game.draw()
        if menu.active: menu.draw()

        # Waiting in order to mainting fps.
        clock.tick(fps)
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
            game.active = 1 - game.active
        else:
            menu.event(e)


def quit(*args):
    '''Close the app'''
    global running
    running = False