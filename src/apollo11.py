#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import pygame
import numpy as np
from helper_funcs import *

# Konstanten
WINDOW_SIZE = WIDTH, HEIGHT = 800, 600
FRAMERATE = 120
TIME_SCALE = 100000

# Ressource - Pfade
RESSOURCES_PATH = 'ressources/'
IMGS_PATH = RESSOURCES_PATH + 'imgs/'
FONTS_PATH = RESSOURCES_PATH + 'fonts/'

# Mond
MOON_MASS = 7.348e22 # kg
MOON_RADIUS = 1.736e6 # m
MOON_PERIGEE_DISTANCE = 3.633e8 # m
MOON_PERIGEE_VELOCITY = np.array([0, 1.082e3]) # m/s
MOON_START_POS = np.array([MOON_PERIGEE_DISTANCE, 0.00])
MOON_IMG_PATH = IMGS_PATH + 'moon.png'

# Erde
EARTH_MASS = 5.972e24 # kg
EARTH_RADIUS = 6.371e6 # m
EARTH_START_POS = np.array([0.0, 0.0])
EARTH_IMG_PATH = IMGS_PATH + 'earth.png'

REDUCED_MASS = (MOON_MASS * EARTH_MASS)/(MOON_MASS + EARTH_MASS) # kg

# Saturn V
SATURNV_IMG_PATH = IMGS_PATH + 'rocket.png'
SATURNV_MASS = 2.97e6 # kg
SATURNV_SIZE = 110

# Eagle
EAGLE_IMG_PATH = IMGS_PATH + 'eagle.png'
EAGLE_MASS = 1.64e4
EAGLE_SIZE = 30

G = 6.674e-11 # m3 kg-1 s-2

fontPath = FONTS_PATH + 'font.TTF'


#
# Game Init
#
#

def initPyGame():
    global screen
    global clock
    global bgImage
    global txtfont

    pygame.init() # Pygame initialisieren.
    pygame.display.set_caption('Apollo 11')
    screen = pygame.display.set_mode(WINDOW_SIZE) # Fenstergrösse festlegen
    clock = pygame.time.Clock() # Brauchen wir zur Framerate-Kontrolle

    bgImage = pygame.image.load(IMGS_PATH + 'space_background.png')
    txtfont = pygame.font.Font(fontPath, 16)


running = True   # Kontrolliert die Repetition des Animations-Loops

re = EARTH_RADIUS
rm = MOON_RADIUS
ld = MOON_START_POS[0]

# Kamerarechteck welches auf den Bildschirm Projeziert wird
projectionRect = Rect(np.array([3*ld+2*rm, re*2]), pos=np.array([-(1.5*ld+rm), -re]))

initPyGame()

# PyGame Klasse, welche Position, usw. für ein Objekt speichert und gewisse Hilfsmethoden bietet
class pyObj:
    def __init__(self, screen, pos=np.array([0.0, 0.0]), size=1.0, img=None, name='', color=(255, 255, 255)):
        self.screen = screen
        self.pos = pos # Ortsvektor in [m]
        self.velocity = np.array([0.0, 0.0])
        self.size = size # Grösse bzw Durchmesser in [m]
        self.rotation = 0.0 # Rotation in [rad]
        self.img = img
        self.fs = 0.0 # Schubkraft in [N]
        self.color = color
        self.name = name

    def get_pos(self):
        return self.pos[0], self.pos[1]

    def set_pos(self, x, y):
        self.pos = np.array([x, y])

    def draw(self, screen, translation, rotation, scaleFactor):
        # Transformation des Projektionsrechtecks auf die Fenstergrösse
        w, h = screen.get_size()
        size = scaleFactor * self.size
        translated_pos = translate(self.pos, translation)
        scaled_pos = scale(translated_pos, scaleFactor)
        pos = flipYaxis(scaled_pos, h)

        # Objekt wird nur gezeichnet, falls objekt im Projektionsrechteck ist
        if  not(-w < pos[0] < 2*w or -h < pos[1] < 2*h):
            return


        if self.img != None:
            size *= 10
            # Bild des Objekts wird gezeichnet falls vorhanden.
            img = pygame.transform.scale(self.img, (int(size), int(size)))
            screen.blit(img, pos - int(size/2))

            # Falls das Bild zu klein ist wird ein Kreis Gezeichnet
            minSize = int((w+h)/2/200)
            if size < minSize:
                pygame.draw.circle(screen, self.color, (int(pos[0]), int(pos[1])), minSize)

            # Label
            nameTag = txtfont.render(self.name, 1, self.color)
            self.screen.blit(nameTag, pos + np.array([0.0, -size - 10]))


        else:
            pygame.draw.circle(screen, self.color, (int(pos[0]), int(pos[1])), int(size/2))




# Initialisierung der PyGame Objekten
earthImg = pygame.image.load(EARTH_IMG_PATH)
earth = pyObj(screen, EARTH_START_POS, size=EARTH_RADIUS*2, img=earthImg, name='Earth', color=(0,0,255))

moonImg = pygame.image.load(MOON_IMG_PATH)
moon = pyObj(screen, MOON_START_POS, size=MOON_RADIUS*2, img=moonImg, name='Moon', color=(0,255,0))
moon.velocity = MOON_PERIGEE_VELOCITY

saturnVImg = pygame.image.load(SATURNV_IMG_PATH)
saturnV = pyObj(screen, EARTH_START_POS + np.array([0.0, EARTH_RADIUS]), size=SATURNV_SIZE, img=saturnVImg, name='Saturn V', color=(255,0,0)) #EARTH_START_POS + EARTH_RADIUS + MOON_START_POS/2
saturnV.velocity = np.array([0.0, 0.0])#1.485e3])
saturnV.fs = np.array([0.0, 3e7])


eagleImg = pygame.image.load(EAGLE_IMG_PATH)
eagle = pyObj(screen, size=EAGLE_SIZE, img=eagleImg, name='Eagle', color=(0,255,255))



def detatchEagle():
    eagle.pos = saturnV.pos
    eagle.velocity = saturnV.velocity
    objsToDraw.append(eagle)



rocket = [eagle, saturnV]
spaceBodies = [earth, moon] # Objekte welche andere durch Gravitation beeinflussen
objsToDraw = spaceBodies + [saturnV] # Objekte welche Gezeichnet werden sollen


#
# Runloop
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
    # Animation und Berechnungen der neuen Positionen
    #
    ###############################################################################


    # Berechnung von dt
    dt = (1/FRAMERATE)*TIME_SCALE
    steps = 10

    # Collision detection

    for spaceBody in spaceBodies:
        for rocket_element in rocket:
            pB = spaceBody.pos
            rB = spaceBody.size/2
            pS = rocket_element.pos
            if point_in_circle(pB, rB, pS):
                BS = pS - pB
                lBS = np.linalg.norm(BS)
                d = rB - lBS
                rocket_element.pos += (BS)/lBS*d
                rocket_element.velocity = np.array([0.0, 0.0])

    # Mond

    # DGL für Zweikörperproblem von Erde und Mond
    def rII_dgl(r):
        return ((-G * EARTH_MASS * MOON_MASS) / np.linalg.norm(r) ** 2) / REDUCED_MASS * r / np.linalg.norm(r)

    r = moon.pos - earth.pos
    v = moon.velocity - earth.velocity
    r_new, v_new = numerical_integrate(rII_dgl, r, v, dt / steps, steps)
    moon.pos = r_new
    moon.velocity = v_new

    # Saturn V
    e_pos = earth.pos
    m_pos = moon.pos
    s_pos = saturnV.pos
    s_v = saturnV.velocity
    saturnV_fs = saturnV.fs

    # print("Pos: " + str(saturnV.pos) + "  Velocity: "+str (saturnV.velocity))

    # DGL für Position von Rackete Berechnene
    def a_s_dgl(pos):
        r_earth = pos - e_pos
        r_moon = pos - m_pos
        afg_earth = -((G * EARTH_MASS) / (np.linalg.norm(r_earth)**3)) * r_earth
        afg_moon = -((G * MOON_MASS) / (np.linalg.norm(r_moon)**3)) * r_moon
        return afg_moon + afg_earth + (saturnV_fs / SATURNV_MASS)


    s_pos_new, s_v_new = numerical_integrate(a_s_dgl, s_pos, s_v, dt / steps, steps)


    saturnV.pos = s_pos_new
    saturnV.velocity = s_v_new


    # Eagle

    egl_pos = eagle.pos
    egl_v = eagle.velocity
    egl_fs = eagle.fs

    # DGL für Position von Eagle berechnen
    def a_egl_dgl(pos):
        r_earth = pos - e_pos
        r_moon = pos - m_pos
        afg_earth = -((G * EARTH_MASS) / (np.linalg.norm(r_earth)**3)) * r_earth
        afg_moon = -((G * MOON_MASS) / (np.linalg.norm(r_moon)**3)) * r_moon
        return afg_moon + afg_earth + (egl_fs / EAGLE_MASS)


    egl_pos_new, egl_v_new = numerical_integrate(a_egl_dgl, egl_pos, egl_v, dt / steps, steps)

    eagle.pos = egl_pos_new
    eagle.velocity = egl_v_new



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
        
    pygame.display.update()
    pygame.display.flip()
    clock.tick(FRAMERATE)

pygame.quit()
