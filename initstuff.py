#! /usr/bin/env python3
# coding: utf-8
import random, pygame
from collections import OrderedDict
import time, os
from config import *		#~ read varibles


#~ game field interface
class Field:
	def __init__(self):
		self.scale = scale
		self.resx = resx * self.scale
		self.resy = resy * self.scale
		self.backcolor = backcolor
		#~ self.directory = str(time.time())
		#~ os.mkdir(self.directory)
	
	def create_screen(self):
		global screen
		screen = pygame.display.set_mode((self.resx, self.resy))
	
	def drawframe(self, framenum):
		if framenum % everyframe == 0:
			screen.fill(self.backcolor, special_flags=0)
			for pix in Pixel.pixlist:
				screen.set_at((pix.x*self.scale, pix.y*self.scale), pix.color)
				if self.scale == 2:
					screen.set_at((pix.x*self.scale+1, pix.y*self.scale), pix.color)
					screen.set_at((pix.x*self.scale, pix.y*self.scale+1), pix.color)
					screen.set_at((pix.x*self.scale+1, pix.y*self.scale+1), pix.color)
			pygame.display.flip()					#~ update the screen
	
	def saveframe(self, framenum):
		filename = self.directory + '/frame' + str(framenum) + '.png'
		pygame.image.save(screen, filename)

#~ create field
field = Field()

#~ pixel interface
class Pixel:
	pixlist = []
	poslist = []
	for x in range(resx):
		for y in range(resy):
			poslist.append((x,y))
			
	def __init__(self, color):
		Pixel.pixlist.append(self)
		self.color = color if color else [random.randint(0, 255) for i in range(3)]
		self.x, self.y = random.choice(Pixel.poslist)
		del Pixel.poslist[Pixel.poslist.index((self.x,self.y))]
		self.family = [self]
		self.prevpixels = []
		self.done = False
		
	def move(self, newx, newy):
		self.x, self.y = newx, newy
		
	def setcolor(self, newcolor):
		self.color = newcolor
	
	
	def search(self, n):
		pix_deltas = {}
		for pix in Pixel.pixlist:
			if pix is self: continue
			delta = abs(self.x - pix.x) + abs(self.y - pix.y)
			pix_deltas[delta] = pix
		res = []
		for idx, key_delta in enumerate(  OrderedDict( sorted(pix_deltas.items()) )  ):
			if idx >= n: break
			res.append(pix_deltas[key_delta])
		return res
	
	def get_next_pos_to(self, target):
		#~ print('self, target:', (self.x, self.y), (target.x, target.y))
		if self.x < target.x:
			x3 = self.x + 1
		elif self.x > target.x:
			x3 = self.x - 1
		else:
			x3 = self.x
		if self.y < target.y:
			y3 = self.y + 1
		elif self.y > target.y:
			y3 = self.y - 1
		else:
			y3 = self.y
		return x3, y3
	
	#~ def find_nearest_free_pix(self):
		#~ sortedpixels = self.search(pix_q)
		#~ for pix in sortedpixels:
			#~ if len(pix.family) < 3  and  pix not in self.prevpixels:
				#~ return pix
	
	def find_nearest_free_pix(self):
		minim = resx + resy - 1
		for pix in Pixel.pixlist:
			deltax,  deltay  =  abs(self.x - pix.x),  abs(self.y - pix.y)
			if len(pix.family) < 3  and  pix not in self.prevpixels:
				if deltax <= 1  and  deltay <= 1: return pix
				if delta < minim:
					minim = delta
					res = pix
		return res
	
	def find_nearest_free_pix(self):
		sortedpixels = self.search(pix_q)
		for pix in sortedpixels:
			if len(pix.family) < 3  and  pix not in self.prevpixels:
				return pix
	
	def reached(self, target):
		return  not abs(target.x-self.x) > 1  and  not abs(target.y-self.y) > 1
	
	def can_move_to(self, canx, cany):
		return  not (canx, cany) in [(pix.x, pix.y) for pix in Pixel.pixlist]
	
	def make_random_step(self):
		possibilities = [(self.x+i1, self.y+i2) for i1 in (-1, 0, 1) for i2 in (-1, 0, 1)]
		for cn in range(6):
			pos = random.choice(possibilities)
			if self.can_move_to(*pos):
				self.move(*pos)
				self.done = True
				break
	
	def join_family_of(self, target):
		self.family.append(target)
		target.family.append(self)
		target.done = True
		if len(target.family) > 2:		#~ if it is 3 now
			third = [pix for pix in target.family if pix != self and pix != target][0]
			self.family.append(third)
			third.family.append(self)
			third.done = True
	
	def get_the_most_different_family_member(self, pix_around_q):
		#~ calculate average color of around pixels
		around_colors = [pix.color for pix in self.search(pix_around_q + 3)[3:]]
		channels = list(zip(*around_colors))
		around_average = [sum(channels[cn])/pix_around_q for cn in range(3)]
		sum_of_around_average = sum(around_average)
		#~ find the most different one
		maximpix = self.family[0]
		for pix in self.family:
			if abs(sum(pix.color) - sum_of_around_average) > sum(maximpix.color):
				maximpix = pix
		return maximpix
	
	def get_average_of_other_family(self):
		family_colors = [pix.color for pix in self.family if pix != self]
		channels = list(zip(*family_colors))
		return [ int(sum(channels[cn])/(len(self.family)-1)) for cn in range(3) ]
	
	def leave_family(self):
		self.prevpixels.extend(self.family)
		while len(self.prevpixels) > prev_pix_q:
			del self.prevpixels[0]
		self.done = True
		self.family = [self]
