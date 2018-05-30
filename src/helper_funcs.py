#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

def numerical_integrate(explicit_diff, x_0, t_0, dt, steps=1):
	return runge_kutta(explicit_diff, x_0, t_0, dt, setps=steps)

def runge_kutta(explicit_diff, x_0, t_0, dt, steps):
	x_points = [x_0]
    	y_points = [y_0]
    	for i in range(steps):
        	x = x_points[-1]
        	yp = y_points[-1]
        
        	k1 = explicit_diff(x, yp)
        	yd1 = k1 * (dt/2) + yp
        
        	k2 = explicit_diff(x+(dt/2), yd1)
        	yd2 = k2 * (dt/2) + yp
        
        	k3 = explicit_diff(x+(dt/2), yd2)
        	yd3 = k3 * dt + yp
        
        	k4 = explicit_diff(x+dt, yd3)
        	ktot = (k1 + 2*k2 + 2*k3 + k4)/6
        
        	new_y = yp + dt * ktot
        	y_points.append(new_y)
        	x_points.append(x+dt)
	return (x_points, y_points)
	
