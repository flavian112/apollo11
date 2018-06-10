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
MOON_START_POS = np.array([3.565e8, 0])
MOON_IMG_PATH = "imgs/moon.png"

# Earth
EARTH_MASS = 5.972e24 # kg
EARTH_RADIUS = 6.371e6 # m
EARTH_START_POS = np.array([0.0, 0.0])
EARTH_IMG_PATH = "imgs/earth.png"

REDUCED_MASS = (MOON_MASS * EARTH_MASS)/(MOON_MASS + EARTH_MASS) # kg

#
# Game Init
#

def initPyGame():
    global screen
    global clock
    global bgImage

    pygame.init() # Pygame initialisieren.
    pygame.display.set_caption('Apollo 11')
    screen = pygame.display.set_mode(WINDOW_SIZE) # Fenstergrösse festlegen
    clock = pygame.time.Clock() # Brauchen wir zur Framerate-Kontrolle

    bgImage = pygame.image.load('imgs/space_background.png')


running = True   # Kontrolliert die Repetition des Animations-Loops

re = EARTH_RADIUS
rm = MOON_RADIUS
ld = MOON_START_POS[0]

projectionRect = Rect(np.array([re+rm+ld, re*2]), pos=np.array([-re, -re]))

initPyGame()

class pyObj:
    def __init__(self, screen, pos=np.array([0.0, 0.0]), size=1.0, img=None):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.rotation = 0.0
        self.img = img

    def get_pos(self):
        return self.pos[0], self.pos[1]

    def set_pos(self, x, y):
        self.pos = np.array([x, y])

    def draw(self, screen, translation, rotation, scaleFactor):
        size = scaleFactor * self.size
        translated_pos = translate(self.pos, translation)
        scaled_pos = scale(translated_pos, scaleFactor)
        pos = flipYaxis(scaled_pos, screen.get_height())


        if self.img != None:

            img = pygame.transform.scale(self.img, (int(size), int(size)))
            screen.blit(img, pos - int(size/2))
        else:
            pygame.draw.circle(screen, (255, 255, 255), (int(pos[0]), int(pos[1])), int(size / 2))

earthImg = pygame.image.load(EARTH_IMG_PATH)
earth = pyObj(screen, EARTH_START_POS, size=EARTH_RADIUS*2, img=earthImg)

moonImg = pygame.image.load(MOON_IMG_PATH)
moon = pyObj(screen, MOON_START_POS, size=MOON_RADIUS*2, img=moonImg)


objsToDraw = [earth, moon]


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
    screen.blit(bgImage, bgImage.get_rect())

    # screen.fill((0,0,0))
    w, h = screen.get_size()
    scaleFactorW = w / projectionRect.width()
    scaleFactorH = h / projectionRect.height()
    # scaleFactor = scaleFactorW if scaleFactorW < scaleFactorH else scaleFactorH

    translation = -projectionRect.pos

    if scaleFactorW < scaleFactorH:
        scaleFactor = scaleFactorW
        t = np.array([0.0, h / 2 - (scaleFactorW / scaleFactorH) * h / 2]) / scaleFactor
        translation += t
    else:
        scaleFactor = scaleFactorH
        t = np.array([w / 2 - (scaleFactorH / scaleFactorW) * w / 2, 0.0]) / scaleFactor
        translation += t



    for obj in objsToDraw:
        obj.draw(screen, translation, projectionRect.rotation, scaleFactor)

    # obj.draw()
    pygame.display.update()
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()
