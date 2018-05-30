#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

def numerical_integrate(explicit_diff, x_0, x1_0, dt, steps=1):
	return runge_kutta(explicit_diff, x_0, x1_0, dt, steps=steps)

def runge_kutta(explicit_diff, x_0, x1_0, dt, steps):
    rk = np.zeros((steps + 1,2))
    rk[0][0] = x_0
    rk[0][1] = x1_0

    for i in range(steps):
        k1 = np.array([rk[i-1][1], explicit_diff(rk[i-1][0])])
        # Halber Euler-Schritt
        v_tmp = rk[i-1] + k1*dt/2
        k2 = np.array([v_tmp[1], explicit_diff(v_tmp[0])])

        # Halber Euler-Schritt mit der neuen Steigung
        v_tmp = rk[i-1] + k2*dt/2
        k3 = np.array([v_tmp[1], explicit_diff(v_tmp[0])])

        # ganzer Euler-Schritt mit k3
        v_tmp = rk[i-1] + k3*dt
        k4 = np.array([v_tmp[1], explicit_diff(v_tmp[0])])

        rk[i] = rk[i-1] + dt*(k1 + 2*k2 + 2*k3 + k4)/6

    return rk[-1]
