from PIL import Image

im = Image.open('output/autogen_0.png')
im2 = Image.open('output/autogen_1.png')

im = Image.blend(im, im2, 0.5)
im.show()
