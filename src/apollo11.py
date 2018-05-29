#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pygame
from helper_funcs import *

# Consts
WINDOW_SIZE = WIDTH, HEIGHT = 800, 600
STEP = 1 
FRAMERATE = 60

#
# Game Init
#
pygame.init() # Pygame initialisieren.
pygame.display.set_caption('Apollo 11')
screen = pygame.display.set_mode(WINDOW_SIZE) # Fenstergrösse festlegen
clock = pygame.time.Clock() # Brauchen wir zur Framerate-Kontrolle

running = True   # Kontrolliert die Repetition des Animations-Loops
animate = True   # Ob die Animation gerade läuft

class PygameObj:
    # Subclass!

    def __init__(self, screen, x=0, y=0):
        self.screen = screen
        self.set_pos(x, y)

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        # Overwrite!
        pass


#
# Animations-Loop
#
while running:

    
    
    ###############################################################################
    #
    # EVENT HANDLING
    #
    #
    # Zur Kontrolle der Animation notwendig. In diesem Fall erlauben wir nur Stop
    # und start.
    ###############################################################################

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Animation beenden.
            running = False


    ###############################################################################
    #
    # Animation 
    #
    ###############################################################################
    
    screen.fill((0,0,0))


    # obj.draw()
    pygame.display.update()
    clock.tick(FRAMERATE)

pygame.quit()
