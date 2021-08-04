from PIL import Image, ImageOps, ImageFilter
import os
from typing import Iterable


def fn_gen(name: str = 'wallpaper_{}.png', dp: str = '~/wallpapers_wide/combined') -> str:
    """
    Generate filename with numerical postfix if file already exists in the output directory dp to avoid
    overwriting existing files.

    WARNING: not race-condition proof, may still overwrite existing file if subjected to race conditions
    when files are created between filepath generation and actual writing to the file

    :param name: name of file, should include one pair of formatting braces for postfix generating
    :param dp: directory path of filename
    :return: filename with postfix
    """
    dp = os.path.expanduser(dp)
    if not os.path.exists(dp):
        os.makedirs(dp)
    fp = os.path.join(dp, name)
    i = 0
    while os.path.exists(fp.format(i)):
        i += 1
    return fp.format(i)


def horizontal_join(image_lst: Iterable = None, image_fns: Iterable = None, dp: str = '~/Downloads',
                    dp_out: str = '~/wallpapers_wide/combined',
                    name: str = 'combined', fixed_height: int = 1440,
                    smooth_width: int = 0, blend_alpha: float = 0) -> None:
    """
    horizontally join list of images in the order given

    :param image_lst: list of images to join
    :param image_fns: list of image filenames to join, directory path defined in dp
    :param dp: directory path of input files, ignored when images are directly passed in via image_lst
    :param dp_out: directory path of output files
    :param name: name of output image, will auto add numerical postfix to if name already exists
    :param fixed_height: height of output image
    :param smooth_width: width of smoothing at joining edges in pixels; uses blending if blend_alpha != 0 then blur
                        twice the width to cover blending
    :param blend_alpha: alpha of blending at joining edges; 0 means no blending, 1 means the mirror is pasted (weird!)
    :return: None
    """
    dp = os.path.expanduser(dp)
    dp_out = os.path.expanduser(dp_out)
    if not os.path.exists(dp_out):
        os.makedirs(dp_out)

    resized_images = []
    total_width = 0
    image_lst = image_lst or (Image.open(os.path.join(dp, image_fn)) for image_fn in image_fns)

    for image in image_lst:
        width, height = image.size
        new_width = int(width / height * fixed_height)
        resized_image = image.resize((new_width, fixed_height))
        resized_images.append(resized_image)
        total_width += new_width

    if not resized_images:
        return

    new_im = Image.new('RGB', (total_width, fixed_height))
    x_offset = 0
    for im in resized_images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    if blend_alpha:
        new_im_blend = new_im.copy()
        x_offset = 0
        for im in resized_images:
            x_offset += im.size[0]
            strip = (x_offset - smooth_width, 0, x_offset + smooth_width, fixed_height)
            cropped_strip = new_im.crop(strip)
            cropped_strip_mirrored = ImageOps.mirror(cropped_strip)
            new_im_blend.paste(cropped_strip_mirrored, strip)
        new_im = Image.blend(new_im, new_im_blend, alpha=blend_alpha)
        smooth_width *= 2

    # will blur to cover blending if blended
    if smooth_width:
        x_offset = 0
        for im in resized_images:
            x_offset += im.size[0]
            strip = (x_offset - smooth_width, 0, x_offset + smooth_width, fixed_height)
            cropped_strip = new_im.crop(strip)
            cropped_strip_smoothed = cropped_strip.filter(ImageFilter.GaussianBlur(radius=min(smooth_width // 2, 5)))
            # cropped_strip_smoothed = cropped_strip.filter(ImageFilter.MedianFilter(size=smooth_width * 2 + 1))
            new_im.paste(cropped_strip_smoothed, strip)

    fp = fn_gen(name=name + '_{}.png', dp=dp_out)
    print(fp)
    new_im.save(fp)


def self_join_mirrored(image_fn: str, side: str = 'right', dp: str = '~/Downloads',
                       dp_out: str = '~/wallpapers_wide/combined',
                       fixed_height: int = 1440) -> None:
    """
    Joining image to horizontal mirror of itself on either left or right

    :param image_fn: image file name, directory is specified in dp
    :param side: only values allowed: "left" or "right", side on which to put mirror image
    :param dp: directory path of input file
    :param dp_out: directory path of output file
    :param fixed_height: height of output image
    :return: None
    """
    dp = os.path.expanduser(dp)
    dp_out = os.path.expanduser(dp_out)
    if not os.path.exists(dp_out):
        os.makedirs(dp_out)

    resized_images = []
    image = Image.open(os.path.join(dp, image_fn))
    width, height = image.size
    new_width = int(width / height * fixed_height)
    resized_image = image.resize((new_width, fixed_height))
    resized_images.append(resized_image)

    mirrored = ImageOps.mirror(resized_image)
    if side == 'right':
        img_lst = [resized_image, mirrored]
    elif side == 'left':
        img_lst = [mirrored, resized_image]
    else:
        NotImplementedError('Only support self joining of horizontal mirror with side="left" or "right"')
    horizontal_join(img_lst, name='self_mirrored')


if __name__ == '__main__':
    # dp = os.path.expanduser('~/Downloads')
    # dp_out = os.path.expanduser('~/wallpapers_wide/combined')
    # if not os.path.exists(dp_out):
    #     os.makedirs(dp_out)
    # fixed_height = 1440
    #
    # image_fns = ['joel-protasio-LZ9LTA83o-o-unsplash.jpg', 'pawel-czerwinski-z7prq6BtPE4-unsplash.jpg']
    # self_join_mirrored('pawel-czerwinski-z7prq6BtPE4-unsplash.jpg', side='left')
    # image_fns = ['mike-yukhtenko-MDzJF3o8Ajk-unsplash.jpg',
    #              'tesson-thaliath-T37GMvi5R7E-unsplash.jpg',
    #              'parrish-freeman-1cAMinWGc3s-unsplash.jpg',
    #              'zoltan-tasi-6CbDs4T_jZc-unsplash.jpg',
    #              'hans-isaacson-ZqSDrFeAbCg-unsplash.jpg', ]
    image_fns = ['xianyu-hao-vTSOYsCoM_Q-unsplash.jpg',
                 'lean-xview-LH7-_hr5PbM-unsplash.jpg',
                 'jez-timms-VivzPEYabew-unsplash.jpg',
                 'wolfgang-hasselmann-NNt-9kdCf98-unsplash.jpg',
                 'daniel-stone-QIAGXy53Rc8-unsplash.jpg', ]
    horizontal_join(image_fns=image_fns, smooth_width=2, blend_alpha=0.5)
