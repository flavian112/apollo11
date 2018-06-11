#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pygame
import numpy as np
from helper_funcs import *

# Consts
WINDOW_SIZE = WIDTH, HEIGHT = 800, 600
FRAMERATE = 120
TIME_SCALE = 100000

def angularMomentum(m,r,v):
    return m*np.cross(r, v)

# Moon
MOON_MASS = 7.348e22 # kg
MOON_RADIUS = 1.736e6 # m
MOON_PERIGEE_DISTANCE = 3.633e8 # m
MOON_PERIGEE_VELOCITY = np.array([0, 1.082e3]) # m/s
MOON_START_POS = np.array([MOON_PERIGEE_DISTANCE, 0.00])
MOON_IMG_PATH = "imgs/moon.png"

# Earth
EARTH_MASS = 5.972e24 # kg
EARTH_RADIUS = 6.371e6 # m
EARTH_START_POS = np.array([0.0, 0.0])
EARTH_IMG_PATH = "imgs/earth.png"

REDUCED_MASS = (MOON_MASS * EARTH_MASS)/(MOON_MASS + EARTH_MASS) # kg

# Saturn V
SATURNV_IMG_PATH = 'imgs/rocket.png'
SATURNV_MASS = 2.97e6 # kg

G = 6.674e-11 # m3 kg-1 s-2



#
# Game Init
#
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

projectionRect = Rect(np.array([3*ld+2*rm, re*2]), pos=np.array([-(1.5*ld+rm), -re]))

initPyGame()

class pyObj:
    def __init__(self, screen, pos=np.array([0.0, 0.0]), size=1.0, img=None):
        self.screen = screen
        self.pos = pos
        self.velocity = np.array([0.0, 0.0])
        self.size = size
        self.rotation = 0.0
        self.img = img
        self.fs = 0.0

    def get_pos(self):
        return self.pos[0], self.pos[1]

    def set_pos(self, x, y):
        self.pos = np.array([x, y])

    def draw(self, screen, translation, rotation, scaleFactor):
        w, h = screen.get_size()
        size = scaleFactor * self.size
        translated_pos = translate(self.pos, translation)
        scaled_pos = scale(translated_pos, scaleFactor)
        pos = flipYaxis(scaled_pos, h)


        if  not(-w < pos[0] < 2*w or -h < pos[1] < 2*h):
            return


        if self.img != None:
            size *= 10
            img = pygame.transform.scale(self.img, (int(size), int(size)))
            screen.blit(img, pos - int(size/2))
        else:
            pygame.draw.circle(screen, (255, 0, 0), (int(pos[0]), int(pos[1])), int(size/2))



earthImg = pygame.image.load(EARTH_IMG_PATH)
earth = pyObj(screen, EARTH_START_POS, size=EARTH_RADIUS*2, img=earthImg)

moonImg = pygame.image.load(MOON_IMG_PATH)
moon = pyObj(screen, MOON_START_POS, size=MOON_RADIUS*2, img=moonImg)
moon.velocity = MOON_PERIGEE_VELOCITY

saturnVImg = pygame.image.load(SATURNV_IMG_PATH)
saturnV = pyObj(screen, EARTH_START_POS + EARTH_RADIUS + MOON_START_POS/2, size=EARTH_RADIUS/2, img=saturnVImg)


objsToDraw = [earth, moon, saturnV]


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

    dt = (1/FRAMERATE)*TIME_SCALE
    steps = 10

    # moon
    def rII_dgl(r):
        return ((-G * EARTH_MASS * MOON_MASS) / np.linalg.norm(r) ** 2) / REDUCED_MASS * r / np.linalg.norm(r)

    r = moon.pos - earth.pos
    v = moon.velocity - earth.velocity
    r_new, v_new = numerical_integrate(rII_dgl, r, v, dt / steps, steps)
    moon.pos = r_new
    moon.velocity = v_new

    # saturnV
    #r_earth = saturnV.pos - earth.pos
    #r_moon = saturnV.pos - moon.pos

    e_pos = earth.pos
    m_pos = moon.pos
    s_pos = saturnV.pos
    s_v = saturnV.velocity
    saturnV_fs = saturnV.fs

    def a_dgl(pos):
        r_earth = pos - e_pos
        r_moon = pos - m_pos
        afg_earth = -((G * EARTH_MASS) / (np.linalg.norm(r_earth)**3)) * r_earth
        afg_moon = -((G * MOON_MASS) / (np.linalg.norm(r_moon)**3)) * r_moon
        return afg_moon + afg_earth + (saturnV_fs / SATURNV_MASS)


    s_pos_new, s_v_new = numerical_integrate(a_dgl, s_pos, s_v, dt / steps, steps)
    print(s_pos_new, s_v_new)


    saturnV.pos = s_pos_new
    saturnV.velocity = s_v_new




    ###############################################################################
    #
    # Drawing
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
