#!/usr/bin/env python


"""compute and render mandelbrot set"""


# updated: Corey Goldberg (2012)
# original program: Kirby Urner (2004) - http://www.4dsolutions.net/ocn/fractals.html


import time

import Image  # PIL
import ImagePalette



PATH = './'  # path for saving files



class Mandelbrot(object):
    
    def __init__(self, filename, size, n=64, box=((-2.0, 1.25), (0.5, -1.25))):
        self.size = size
        self.filename = filename
        self.n = n
        self.uleft  = box[0]
        self.lright = box[1]
        self.xwidth = self.lright[0] - self.uleft[0]
        self.ywidth = self.uleft[1]  - self.lright[1]
        self.image = self.__new_image()

    def __new_image(self):
        image = Image.new('P', self.size)
        palette = [0, 0, 0]
        for i in xrange(0, 255):
            palette.extend((i*5%200 + 55, i*7%200 + 55, i*11%200 + 55))
        image.putpalette(palette)
        return image
        
    def __save_image(self):
        self.image.save(self.filename)
        print 'saved: %r' % self.filename

    def __get_coords(self, x, y):
        percentx = x / float(self.size[0])
        percenty = y / float(self.size[1])
        xp = self.uleft[0] + percentx * (self.xwidth)
        yp = self.uleft[1] - percenty * (self.ywidth)
        return (xp, yp)
    
    def __fractal(self, x, y):
        z = complex(x, y)
        o = complex(0, 0)
        dotcolor = 0  # default, convergent
        for trials in xrange(self.n):
            if abs(o) <= 2.0:
                o = o**2 + z
            else:
                dotcolor = trials
                break  # diverged
        return dotcolor 
    
    def compute(self):
        print 'computing %s...' % self.__class__.__name__
        start = time.time()
        self.image = self.__new_image()
        for x in xrange(self.size[0]):
            for y in xrange(self.size[1]):
                xp, yp = self.__get_coords(x, y)                
                dotcolor = self.__fractal(xp, yp)
                self.image.putpixel((x, y), dotcolor)
        print 'compute time: %.2f secs' % (time.time() - start)
        self.__save_image()

    
if __name__ == '__main__':
    m = Mandelbrot(PATH + 'mandelbrot.png', (500, 500))
    m.compute()
