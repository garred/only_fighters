'''Manages things related with the GUI.'''

import pygame
from pgu import gui
import app


class Menu(gui.App):
    def __init__(self):
        super(Menu, self).__init__(theme=gui.Theme('data/themes/clean'))

        self.active = True
        self.veil = pygame.Surface((app.screen_width, app.screen_height), pygame.SRCALPHA)
        self.veil.fill((0, 0, 0, 128))

        # Some basic elements
        label_title = gui.Label('Only fighters', cls='h1', color=(255, 255, 255))
        keyboard = gui.Image('data/themes/keyboard.png', align=1)
        button_hi = gui.Button('Hi world')
        button_quit = gui.Button('Quit')

        # Making useful the 'Quit' button
        button_quit.connect(gui.CLICK, quit, None)

        # An usage example of a poping dialog
        t = gui.Table(width=50, height=50)
        t.tr()
        t.td(gui.Label('Game made by Álvaro González Redondo'))
        t.tr()
        t.td(gui.Label('garred205@gmail.com'))
        t.tr()
        e = gui.Button("Oh. Great.")
        t.td(e, colspan=2)
        dialog = gui.Dialog(gui.Label('Hello world'), t)
        e.connect(gui.CLICK, dialog.close, None)
        button_hi.connect(gui.CLICK, dialog.open, None)

        # Arranging the elements of the menu
        menu = gui.Table(width=500, height=500)
        menu.tr(); menu.td(label_title)
        menu.tr(); menu.td(keyboard)
        menu.tr(); menu.td(button_hi)
        menu.tr(); menu.td(button_quit)

        # Initializes the object
        self.init(widget=menu)


    def draw(self):
        app.screen.blit(self.veil, (0, 0))
        self.paint()

menu = Menu()

