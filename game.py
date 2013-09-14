#! /usr/bin/env python3
# coding: utf-8
from initstuff import *

#~ [ Pixel(color=None) for cn in range(int(pix_q)) ]
[ Pixel([255,255,0]) for cn in range(int(pix_q/3)) ]
[ Pixel([0,255,255]) for cn in range(int(pix_q/3)) ]
[ Pixel([255,0,255]) for cn in range(int(pix_q/3)) ]
field.create_screen()

running = True
framenum = 0
while running:
	for pix in Pixel.pixlist:
		if pix.done:
			pix.done = False
			continue
		
		if len(pix.family) == 1:						#~ if alone
			target = pix.find_nearest_free_pix()
			wantx, wanty = pix.get_next_pos_to(target)
			if pix.can_move_to(wantx, wanty):
				pix.move(wantx, wanty)
			else:
				pix.make_random_step()
			if pix.reached(target):
				pix.join_family_of(target)
				
		elif len(pix.family) == 3:						#~ if it a family
			diffpix = pix.get_the_most_different_family_member(pix_around_q)
			newcolor = diffpix.get_average_of_other_family()
			diffpix.setcolor(newcolor)
			for pix1 in pix.family:
				pix1.leave_family()
		
		pix.done = True

	for event in pygame.event.get():		#~ for correct exiting
		if event.type == pygame.QUIT:
			running = False
	
	framenum += 1
	print('frame {0}'.format(framenum))
	field.drawframe(framenum)					#~ update the screen
	#~ field.saveframe(framenum)
