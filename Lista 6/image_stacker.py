from PIL import Image


def get_concat_v(root, n):
    im1 = Image.open(root)
    dst = Image.new('RGB', (im1.width, im1.height * n))
    for i in reversed(range(n)):
        dst.paste(im1, (0, i * im1.height))
    return dst


get_concat_v("pic10.png", 5).save('out.png')