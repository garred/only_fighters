'''Manages things related with the GUI.'''

import pygame
from pgu import gui
import app


class Menu(gui.App):
    def __init__(self):
        super(Menu, self).__init__(theme=gui.Theme('data/themes/clean'))

        self.active = True
        self.veil = pygame.Surface((1000, 750), pygame.SRCALPHA)
        self.veil.fill((0, 0, 0, 128))

        # Some basic elements
        label_title = gui.Label('Only fighters', cls='h1', color=(255, 255, 255))
        button_hi = gui.Button('Hi world')
        button_quit = gui.Button('Quit')

        # Making useful the 'Quit' button
        button_quit.connect(gui.CLICK, quit, None)

        # An usage example of a poping dialog
        dialog = gui.Dialog(gui.Label('Hola mundo'), gui.Table(width=50, height=50))
        button_hi.connect(gui.CLICK, dialog.open, None)

        # Arranging the elements of the menu
        menu = gui.Table(width=500, height=500)
        menu.tr(); menu.td(label_title)
        menu.tr(); menu.td(button_hi)
        menu.tr(); menu.td(button_quit)

        # Initializes the object
        self.init(widget=menu)


    def draw(self):
        app.screen.blit(self.veil, (0, 0))
        self.paint()

menu = Menu()

