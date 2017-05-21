#!/usr/bin/env python


"""Compute and render Mandelbrot set.

updates: Corey Goldberg (2012)
original: Kirby Urner (2004)

"""


import time

from PIL import Image, ImagePalette


class Mandelbrot(object):

    def __init__(self, outfile, size, n=64, box=((-2.0, 1.25), (0.5, -1.25))):
        self.size = size
        self.outfile = outfile
        self.n = n
        self.uleft  = box[0]
        self.lright = box[1]
        self.xwidth = self.lright[0] - self.uleft[0]
        self.ywidth = self.uleft[1]  - self.lright[1]
        self.image = self.__new_image()

    def __new_image(self):
        image = Image.new('P', self.size)
        palette = [0, 0, 0]
        for i in range(0, 255):
            palette.extend((i*5%200+55, i*7%200+55, i*11%200+55))
        image.putpalette(palette)
        return image

    def __save_image(self):
        self.image.save(self.outfile)
        print('saved: {}'.format(self.outfile))

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
        for trials in range(self.n):
            if abs(o) <= 2.0:
                o = o**2 + z
            else:
                dotcolor = trials
                break  # diverged
        return dotcolor

    def compute(self):
        print('computing {}...'.format(self.__class__.__name__))
        start = time.time()
        self.image = self.__new_image()
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                xp, yp = self.__get_coords(x, y)
                dotcolor = self.__fractal(xp, yp)
                self.image.putpixel((x, y), dotcolor)
        self.__save_image()
        end = time.time()
        print('compute time: {} secs'.format(end - start))


if __name__ == '__main__':
    outfile ='./mandelbrot.png'
    dimensions = (500, 500)
    Mandelbrot(outfile, dimensions).compute()
