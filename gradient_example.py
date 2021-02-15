# source: https://stackoverflow.com/questions/30608035/plot-circular-gradients-using-pil-in-python/30669765

from PIL import Image
import math

imgsize = (250, 250)  # The size of the image

image = Image.new('RGB', imgsize)  # Create the image

innerColor = [80, 80, 255]  # Color at the center
outerColor = [0, 0, 80]  # Color at the corners

for y in range(imgsize[1]):
    for x in range(imgsize[0]):
        # Find the distance to the center
        distanceToCenter = math.sqrt((x - imgsize[0] / 2) ** 2 + (y - imgsize[1] / 2) ** 2)

        # Make it on a scale from 0 to 1
        distanceToCenter = float(distanceToCenter) / (math.sqrt(2) * imgsize[0] / 2)

        # Calculate r, g, and b values
        r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
        g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
        b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)

        # Place the pixel
        image.putpixel((x, y), (int(r), int(g), int(b)))

image.save('circlegradient.jpg')

imgsize = (250, 250)  # The size of the image

image = Image.new('RGB', imgsize)  # Create the image

innerColor = [80, 80, 255]  # Color at the center
outerColor = [0, 0, 80]  # Color at the edge

for y in range(imgsize[1]):
    for x in range(imgsize[0]):
        # Find the distance to the closest edge
        distanceToEdge = min(abs(x - imgsize[0]), x, abs(y - imgsize[1]), y)

        # Make it on a scale from 0 to 1
        distanceToEdge = float(distanceToEdge) / (imgsize[0] / 2)

        # Calculate r, g, and b values
        r = innerColor[0] * distanceToEdge + outerColor[0] * (1 - distanceToEdge)
        g = innerColor[1] * distanceToEdge + outerColor[1] * (1 - distanceToEdge)
        b = innerColor[2] * distanceToEdge + outerColor[2] * (1 - distanceToEdge)

        # Place the pixel
        image.putpixel((x, y), (int(r), int(g), int(b)))

image.save('rectgradient.jpg')
