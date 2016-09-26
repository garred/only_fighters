import pygame
from pygame.constants import QUIT, K_ESCAPE

from graphics import Graphics
from menu import Menu
from game import Game


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

menu = Menu(screen)
'''Manages things related with the GUI.'''
graphics = Graphics(screen)
'''Manages things related with the graphics.'''
game = Game()
'''Manages the game mechanics.'''



def run():
    '''Holds the main loop.'''

    global screen, menu, graphics, game

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
    global running, menu

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


