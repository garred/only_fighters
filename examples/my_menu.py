import pygame
from pgu import gui

#from my_app import quit, graphics, menu
import app as app


class MyMenu(gui.App):
    def __init__(self, screen):
        super(MyMenu, self).__init__(theme=gui.Theme('clean'))
        self.screen = screen

        self.active = True
        self.veil = pygame.Surface((1000, 750), pygame.SRCALPHA)
        self.veil.fill((255, 255, 255, 128))

        label_title = gui.Label('Title', cls='h1', color=(255, 255, 255))
        button_hi = gui.Button('Hi world')
        button_quit = gui.Button('Quit')

        button_quit.connect(gui.CLICK, quit, None)

        menu = gui.Table(width=500, height=500)
        menu.tr(); menu.td(label_title)
        menu.tr(); menu.td(button_hi)
        menu.tr(); menu.td(button_quit)

        self.init(widget=menu)

    def draw(self):
        app.graphics.screen.blit(self.veil, (0, 0))
        app.menu.paint()