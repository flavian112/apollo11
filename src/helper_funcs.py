#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import numpy as np


# Klasse für ein Rechteck mit verschiedenen Hilfsmethoden
class Rect:
    def __init__(self, size, pos=np.array([0.0,0.0]), rotation=0.0):
        self.size = size
        self.pos = pos
        self.rotation = rotation

    def width(self):
        return self.size[0]

    def height(self):
        return self.size[1]

    def center(self):
        center_p = self.size/2
        rotated_p = rotate(center_p, self.rotation)
        translated_p = translate(rotated_p, self.pos)
        return translated_p



# Methode für die Translation eines Ortvektors
def translate(p, v):
    return p + v

# Methode um Ortsvektoren relativ zu einem gegebenen Punkt zu rotieren
def rotate(p, ang, o=np.array([0.0, 0.0])):
    s = np.sin(ang)
    c = np.cos(ang)
    rotM = np.array([[c,  s],
                     [-s, c]])
    return translate(rotM.dot(translate(p, -o)), o)

# Methode um Ortsvektoren relativ zu einem gegebenen Punkt zu skalieren
def scale(p, fac, o=np.array([0.0, 0.0])):
    return translate(fac * translate(p, -o), o)


# Methode um Ortsvektoren an der X-Achse zu spieglen
def flipYaxis(p, offset):
    scaleM = np.array([[1.0,  0.0],
                       [0.0, -1.0]])
    return  scaleM.dot(translate(p, np.array([0.0, -offset])))



def numerical_integrate(explicit_diff, x_0, xI_0, dt, steps=1):
    return runge_kutta(explicit_diff, x_0, xI_0, dt, steps=steps)


def runge_kutta(explicit_diff, x_0, xI_0, dt, steps):
    # Initialisierung
    rk = np.empty((steps + 1, 2,2))
    rk[0][0] = x_0
    rk[0][1] = xI_0
    # Hiermit kann man die anzahl Runge-Kutta Iterationen steuern
    for i in range(1, steps + 1):
        k1 = np.array([rk[i-1][1], explicit_diff(rk[i-1][0])])
        # Halber Euler-Schritt
        v_tmp = rk[i-1] + k1*dt/2
        k2 = np.array([v_tmp[1], explicit_diff(v_tmp[0])])

        # Halber Euler-Schritt mit der neuen Steigung
        v_tmp = rk[i-1] + k2*dt/2
        k3 = np.array([v_tmp[1], explicit_diff(v_tmp[0])])

        # Ganzer Euler-Schritt mit k3
        v_tmp = rk[i-1] + k3*dt
        k4 = np.array([v_tmp[1], explicit_diff(v_tmp[0])])

        rk[i] = rk[i-1] + dt*(k1 + 2*k2 + 2*k3 + k4)/6

    return rk[-1]


# Methode zum Herausfinden, ob ein Punkt innerhalb eines Kreises liegt
def point_in_circle(m,r,p):
    return not (np.linalg.norm(p-m) > r)
