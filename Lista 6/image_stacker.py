from PIL import Image
from PIL import ImageEnhance

def get_concat_v(f1, n):
    im1 = Image.open(f1)
    dst = Image.new('RGB', (im1.width, im1.height * n))
    for i in reversed(range(n)):
        dst.paste(im1, (0, i * im1.height))
    return dst


# get_concat_v("graphics/pic10.png", 5).save('graphics/out.png')


def get_concat_v2(f1, f2):
    im1 = Image.open(f1)
    im2 = Image.open(f2)
    # im2 = im2.transpose(Image.FLIP_LEFT_RIGHT)
    dst = Image.new('RGB', (im1.width, 8*im1.height))
    for i in range(4):
        dst.paste(im1, (0, i * im1.height))
    for i in range(4):
        dst.paste(im2, (0, (i+4) * im1.height))
    return dst


# get_concat_v2("graphics/beach_bg1.png", "graphics/beach_bg2.png").save('graphics/out2.png')


def flip_image(f1):
    im1 = Image.open(f1)
    im1 = im1.transpose(Image.FLIP_LEFT_RIGHT)
    im1.save(f1)


# flip_image("graphics/beach_bg2.png")

# img = Image.open('graphics/out2.png')
# converter = ImageEnhance.Color(img)
# img2 = converter.enhance(0.25)
# img2.save('graphics/out4.png')
