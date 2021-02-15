#!/usr/bin/python3.8
from PIL import Image, ImageDraw
import numpy
import os

width = 1920 * 2
height = 1080 * 2
num_circle = 30
num_outlines = 10
size = 90

i = 0
fp = '~/wallpapers/autogen_{}.png'
fp = os.path.expanduser(fp)
if not os.path.exists(os.path.dirname(fp)):
    os.makedirs(os.path.dirname(fp))
while os.path.exists(fp.format(i)):
    i += 1
print(fp.format(i))

c_bk = numpy.random.randint(0, 255, (3,))
a_bk = numpy.random.randint(200, 255)

im = Image.new('RGB', (width, height), tuple(c_bk))
draw = ImageDraw.Draw(im, 'RGBA')

width *= 6 / 7

# draw.ellipse((), fill=)
x_lst = numpy.random.randint(0, width, (num_circle,))
y_lst = numpy.random.randint(0, height, (num_circle,))
color_lst = numpy.random.randint(0, 255, (num_circle, 3))
outline_lst = numpy.random.randint(0, 255, (num_outlines, 4))
xyo_lst = numpy.random.randint(0, height, (num_outlines, 2))
alpha_lst = numpy.random.randint(0, 200, (num_circle,))
size_lst = numpy.random.rand(num_circle) * size + 10

for x, y, c, a, s in zip(x_lst, y_lst, color_lst, alpha_lst, size_lst):
    # draw.ellipse((x - s, y - s, x + s, y + s), fill=tuple(c))
    draw.ellipse((x - s, y - s, x + s, y + s), fill=tuple(c) + (a,))

for o, xyo, s in zip(outline_lst, xyo_lst, size_lst):
    xo, yo = xyo
    xo = xo / height * width
    draw.ellipse((xo - s, yo - s, xo + s, yo + s), outline=tuple(o), width=5)

im.save(fp.format(i))
