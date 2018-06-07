#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pygame
import numpy as np
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

screen = None

def initPyGame():
    pygame.init() # Pygame initialisieren.
    pygame.display.set_caption('Apollo 11')
    screen = pygame.display.set_mode(WINDOW_SIZE) # Fenstergrösse festlegen
    clock = pygame.time.Clock() # Brauchen wir zur Framerate-Kontrolle

    bgImage = pygame.image.load('imgs/space_background.png')
    screen.blit(bgImage, bgImage.get_rect())


running = True   # Kontrolliert die Repetition des Animations-Loops
projectionRect = Rect(np.array([3800.0, 2800.0]), pos=np.array([200, 200]))



class pyObj:
    def __init__(self, screen, drawfunc, pos=np.array([0.0, 0.0])):
        self.screen = screen
        self.pos = pos
        self.draw = drawfunc
        self.size = 1.0
        self.rotation = 0.0

    def get_pos(self):
        return self.pos[0], self.pos[1]

    def set_pos(self, x, y):
        self.pos = np.array([x, y])


def drawfuncPlanet(screen, pos, size):
    pygame.draw.circle(screen, (255,255,255), (int(pos[0]), int(pos[1])), int(size/2))

planetSize = 500
planet1 = pyObj(screen,drawfuncPlanet, np.array([200, 200]))
planet2 = pyObj(screen,drawfuncPlanet, np.array([200, 3000]))
planet3 = pyObj(screen,drawfuncPlanet, np.array([4000, 3000]))
planet4 = pyObj(screen,drawfuncPlanet, np.array([4000, 300]))
planet5 = pyObj(screen,drawfuncPlanet, np.array([2100, 1600]))
objsToDraw =[planet1, planet2, planet3, planet4, planet5]

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
    w, h = screen.get_size()
    scaleFactorW = w / projectionRect.width()
    scaleFactorH = h / projectionRect.height()
    scaleFactor = scaleFactorW if scaleFactorW < scaleFactorH else scaleFactorH

    translation = scale(projectionRect.pos, scaleFactor)

    for obj in objsToDraw:
        obj.draw(screen, flipYaxis(translate(scale(obj.pos, scaleFactor), -translation), h), scaleFactor * planetSize)

    # obj.draw()
    pygame.display.update()
    clock.tick(FRAMERATE)

pygame.quit()
