from PIL import Image, ImageFilter
import numpy

width = 1920
height = 1080
blending = 0.2
num = 10


data = numpy.abs(numpy.cos(numpy.tan(numpy.random.rand(width*height, 3) * numpy.pi / 2))*255).astype(int)
# data = numpy.random.randint(0, 255, (width*height, 3))
# data = (data * 0.2 + 204).astype(int)
# data = numpy.random.randint(0, 255, (num, width*height, 3))
for row in range(height):
    for col in range(width):
        curr = data[row*width + col]
        data[row*width + col] = (curr * blending + numpy.abs(numpy.cos(numpy.tan(row / height * numpy.pi / 2))) * 255 * (1-blending) / 2 + numpy.abs(numpy.cos(numpy.tan(col / width * numpy.pi / 2))) * 255 * (1-blending) / 2).astype(int)

print(data)

im = Image.new('RGB', (width, height))
im.putdata([tuple(x) for x in data])
# im.putdata([tuple(x) for x in data[0]])

# for i in range(1, num):
#     print(i)
#     im2 = Image.new('RGB', (width, height))
#     im2.putdata([tuple(x) for x in data[i]])
# # im = im.filter(ImageFilter.SMOOTH)
#     im = Image.blend(im, im2, alpha=0.5)
im.show()