#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pygame
from helper_funcs import *

# Consts
WINDOW_SIZE = WIDTH, HEIGHT = 800, 600
FRAMERATE = 60

# Moon
MOON_MASS = 7.348e22 # kg
MOON_RADIUS = 1.736e6 # m

# Earth
EARTH_MASS = 5.972e24 # kg
EARTH_RADIUS = 6.371e6 # m

REDUCED_MASS = (MOON_MASS * EARTH_MASS)/(MOON_MASS + EARTH_MASS) # kg

#
# Game Init
#
pygame.init() # Pygame initialisieren.
pygame.display.set_caption('Apollo 11')
screen = pygame.display.set_mode(WINDOW_SIZE) # Fenstergrösse festlegen
clock = pygame.time.Clock() # Brauchen wir zur Framerate-Kontrolle

bgImage = pygame.image.load('imgs/space_background.png')
screen.blit(bgImage, bgImage.get_rect())

running = True   # Kontrolliert die Repetition des Animations-Loops

class PygameObj:
    # Subclass!

    def __init__(self, screen, x=0.0, y=0.0):
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

class AstronomicalObj(PygameObj):

    def __init__(self, screen, x=0.0, y=0.0, radius=10, img=None):
        super(AstronomicalObj, self).__init__(screen, x, y)
        self.img = img
        self.color = (255,255,255)
        self.radius = radius

    def draw(self):
        if (self.img == None):
            pygame.draw.circle(self.screen, self.color, self.get_pos(), self.radius)
        else:
            pass
            #pygame.draw.
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
    
    # screen.fill((0,0,0))


    # obj.draw()
    pygame.display.update()
    clock.tick(FRAMERATE)

pygame.quit()
