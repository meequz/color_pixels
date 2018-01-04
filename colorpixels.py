#! /usr/bin/env python3
# coding: utf-8
import random
from collections import OrderedDict

import pixelqt


class Pixel:
    
    def __init__(self, color):
        self.color = color if color else [random.randint(0, 255) for i in range(3)]
        self.x, self.y = random.choice(poslist)
        del poslist[poslist.index((self.x,self.y))]
        self.family = [self]
        self.prevpixels = []
    
    def move(self, newx, newy):
        self.x, self.y = newx, newy
    
    def setcolor(self, newcolor):
        self.color = newcolor
    
    def search(self, n):
        pix_deltas = {}
        for pix in pixlist:
            if pix is self: continue
            delta = abs(self.x - pix.x) + abs(self.y - pix.y)
            pix_deltas[delta] = pix
        res = []
        for idx, key_delta in enumerate(  OrderedDict( sorted(pix_deltas.items()) )  ):
            if idx >= n: break
            res.append(pix_deltas[key_delta])
        return res
    
    def get_next_pos_to(self, target):
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
    
    def find_nearest_free_pix(self):
        sortedpixels = self.search(pix_q)
        for pix in sortedpixels:
            if len(pix.family) == 1  and  pix not in self.prevpixels:
                return pix
            if len(pix.family) == 2  and \
            pix not in self.prevpixels  and \
            pix.family[1] not in self.prevpixels:
                return pix
    
    def reached(self, target):
        return  not abs(target.x-self.x) > 1  and  not abs(target.y-self.y) > 1
    
    def can_move_to(self, canx, cany):
        return  not (canx, cany) in [(pix.x, pix.y) for pix in pixlist]
    
    def make_random_step(self):
        possibilities = [(self.x+i1, self.y+i2) for i1 in (-1, 0, 1) for i2 in (-1, 0, 1)]
        for cn in range(6):
            pos = random.choice(possibilities)
            if self.can_move_to(*pos):
                self.move(*pos)
                break
    
    def join_family_of(self, target):
        self.family.append(target)
        target.family.append(self)
        if len(target.family) == 3:
            third = [pix for pix in target.family if pix != self and pix != target][0]
            #~ third = target.family[1]
            self.family.append(third)
            third.family.append(self)
    
    def get_the_most_different_family_member(self, pix_around_q):
        # calculate average color of around pixels
        around_colors = [pix.color for pix in self.search(pix_around_q + 3)[3:]]
        channels = list(zip(*around_colors))
        around_average = [sum(channels[cn])/pix_around_q for cn in range(3)]
        sum_of_around_average = sum(around_average)
        
        # find the most different one
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
        self.prevpixels.extend(self.family[1:])
        while len(self.prevpixels) > prev_pix_q:
            del self.prevpixels[0]
        self.family = [self]



def get_drawdata(w, h, frame_count):
    if frame_count == 100000:
        exit()
    
    global pix_around_q, prev_pix_q
    
    pix_around_q = cp_game.own_params['Pixels around']
    prev_pix_q = cp_game.own_params['Previous pixels']
    
    if frame_count == 0:
        global pix_q, pixlist, poslist
        pix_q = cp_game.own_params['Pixel quantity']
        
        pixlist, poslist = [], []
        for x in range(cp_game.config['w']):
            for y in range(cp_game.config['h']):
                poslist.append((y, x))
        
        pixlist.extend( [Pixel([255,255,0]) for cn in range(int(pix_q/3))] )
        pixlist.extend( [Pixel([0,255,255]) for cn in range(int(pix_q/3))] )
        pixlist.extend( [Pixel([255,0,255]) for cn in range(int(pix_q/3))] )
        
    # compute pixels
    for pix in pixlist:
        
        # if alone
        if len(pix.family) == 1:
            target = pix.find_nearest_free_pix()
            
            wantx, wanty = pix.get_next_pos_to(target)
            if pix.can_move_to(wantx, wanty):
                pix.move(wantx, wanty)
            else:
                pix.make_random_step()
            
            if pix.reached(target):
                pix.join_family_of(target)
        
        # if it is in family
        elif len(pix.family) == 3:
            diffpix = pix.get_the_most_different_family_member(pix_around_q)
            newcolor = diffpix.get_average_of_other_family()
            diffpix.setcolor(newcolor)
            for pix1 in pix.family:
                pix1.leave_family()
    
    # return dict
    res = {}
    for pix in pixlist:
        res[(pix.x, pix.y)] = pix.color
    return res



cp_game = pixelqt.Game(get_drawdata=get_drawdata)

cp_game.config['name'] = 'Color pixels'
cp_game.config['w'] = 400
cp_game.config['h'] = 300
cp_game.config['zoom'] = 2
cp_game.config['over'] = False
cp_game.config['draw_each'] = 1
cp_game.config['background'] = [0, 0, 0]

cp_game.init_controls('resolution', 'zoom', 'draw_each', 'save_each', 'over')

# pixel quantity
cp_game.add_own_num(name='Pixel quantity', default=701, need_to_restart=True,
                    minimum=1, maximum=9999, step=1)

# quantity of pixels around family from which is average value calculating
cp_game.add_own_num(name='Pixels around', default=10, need_to_restart=False,
                    minimum=1, maximum=9999, step=1)

# how many pixs in every pix's memory of previous families
cp_game.add_own_num(name='Previous pixels', default=698, need_to_restart=False,
                    minimum=1, maximum=9999, step=1)

cp_game.run()
