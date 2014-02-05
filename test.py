#! /usr/bin/env python3
# coding: utf-8

def bresenham_line(x1, y1, x2, y2):
	points = []
	issteep = abs(y2-y1) > abs(x2-x1)
	if issteep:
		x1, y1 = y1, x1
		x2, y2 = y2, x2
	rev = False
	if x1 > x2:
		x1, x2 = x2, x1
		y1, y2 = y2, y1
		rev = True
	deltax = x2 - x1
	deltay = abs(y2-y1)
	error = int(deltax / 2)
	y = y1
	ystep = None
	if y1 < y2:
		ystep = 1
	else:
		ystep = -1
	for x in range(x1, x2 + 1):
		if issteep:
			points.append((y, x))
		else:
			points.append((x, y))
		error -= deltay
		if error < 0:
			y += ystep
			error += deltax
	if rev:
		points.reverse()
	return points

def bresenham_first(x1, y1, x2, y2):
	if x1 < x2:
		x3 = x1 + 1
	elif x1 > x2:
		x3 = x1 - 1
	else:
		x3 = x1
	if y1 < y2:
		y3 = y1 + 1
	elif y1 > y2:
		y3 = y1 - 1
	else:
		y3 = y1
	return x3, y3


x1 = 3
y1 = 3
x2 = 8
y2 = 3

#~ print( bresenham_line(x1, y1, x2, y2)[1] )
print( bresenham_first(x1, y1, x2, y2) )
