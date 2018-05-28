#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Beispiel von Beni Keller, 2018-05-20
#
# Dieses Programm ist ein Minimalbeispiel, wie Himmelskörper und
# ihre Bewegung mit Pygame simuliert werden können. Physikalisch ist
# es jedoch komplett unrealistisch.

import pygame as p # Sorry, ich bin zu faul, um immer 'pygame' auszuschreiben.

# Einige Konstanten zur Konfiguration der Simulation.
SIZE = WIDTH, HEIGHT = 800, 600
PLANET_STARTPOS = (200, 300)
MOON_STARTPOS = (600, 300)
PLANET_COLOR = (255,0,0)
MOON_COLOR = (0,255,0) 
PLANET_DIAMETER = 10
MOON_DIAMETER = 3
STEP = 1 
FRAMERATE = 60

#
# Game initialisieren und alle Initialwerte korrekt setzen.
#
p.init() # Pygame initialisieren.
p.display.set_caption('Multiplayer Beispiel')
screen = p.display.set_mode(SIZE) # Fenstergrösse festlegen
clock = p.time.Clock() # Brauchen wir zur Framerate-Kontrolle

running = True   # Kontrolliert die Repetition des Animations-Loops
animate = True   # Ob die Animation gerade läuft

class Orb:
    def __init__(self, screen, x=0, y=0, diameter=10, color=(255,255,255)):
        self.screen = screen
        self.set_pos(x, y)
        self.color = color
        self.diameter = diameter

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def move_horizontally(self, step):
        self.x += step

    def move_vertically(self, step):
        self.y += step
        
    def draw(self):
        p.draw.circle(self.screen, self.color, self.get_pos(), self.diameter)
        
planet = Orb(screen, *PLANET_STARTPOS, PLANET_DIAMETER, PLANET_COLOR)
moon = Orb(screen, *MOON_STARTPOS, MOON_DIAMETER, MOON_COLOR)
dm = dp = 1

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

    
    for event in p.event.get():
        if event.type == p.QUIT:
            # Animation beenden.
            running = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_s: # s für stop
                animate = False
            if event.key == p.K_r: # r für run
                animate = True

    ###############################################################################
    #
    # Animation 
    #
    ###############################################################################
    
    screen.fill((0,0,0))
    px, py = planet.get_pos()
    mx, my = moon.get_pos()

    if px < 20:
        dp = 1
    elif px > 600:
        dp = -1

    if my < 20:
        dm = 3
    elif my > 400:
        dm = -3

    if animate:
        planet.move_horizontally(dp)
        moon.move_vertically(dm)
        
    planet.draw()
    moon.draw()
    p.display.update()
    clock.tick(FRAMERATE)

p.quit()
