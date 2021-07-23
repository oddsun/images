from PIL import Image
import os

dp = os.path.expanduser('~/Downloads')
dp_out = os.path.expanduser('~/wallpapers_wide/combined')
if not os.path.exists(dp_out):
    os.makedirs(dp_out)
fixed_height = 1440

image_fns = ['alberto-restifo-HYA9Ak06qR8-unsplash.jpg', 'joel-protasio-LZ9LTA83o-o-unsplash.jpg']
resized_images = []
total_width = 0
for image_fn in image_fns:
    image = Image.open(os.path.join(dp, image_fn))
    width, height = image.size
    new_width = int(width / height * fixed_height)
    resized_image = image.resize((new_width, fixed_height))
    resized_images.append(resized_image)
    total_width += new_width

new_im = Image.new('RGB', (total_width, fixed_height))
x_offset = 0
for im in resized_images:
    new_im.paste(im, (x_offset, 0))
    x_offset += im.size[0]

fp = os.path.join(dp_out, 'combined_{}.png')
i = 0
while os.path.exists(fp.format(i)):
    i += 1
print(fp.format(i))

new_im.save(fp.format(i))
