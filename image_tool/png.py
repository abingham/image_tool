import png


def art():
    s = ['110010010011',
         '101011010100',
         '110010110101',
    '100010010011']
    s = [[int(v) for v in x] for x in s]

    f = open('png.png', 'wb')
    palette = [(0x55,0x55,0x55), (0xff,0x99,0x99)]
    w = png.Writer(len(s[0]), len(s), palette=palette, bitdepth=1)
    w.write(f, s)
    f.close()


def swatch():
    p = [(255,0,0, 0,255,0, 0,0,255),
         (128,0,0, 0,128,0, 0,0,128)]
    f = open('swatch.png', 'wb')
    w = png.Writer(3, 2)
    w.write(f, p)
    f.close()


def stuff(filename):
    with open(filename, 'rb') as f:
        r = png.Reader(file=f)
        width, height, pixel_iter, metadata = r.asRGBA8()
        pixels = list(pixel_iter)
    print(width, height, metadata)
    # for row in pixels:
    #     for ofs in range(0, len(row), 4):
    #         pix = row[ofs:ofs+4]
    #         if pix[0] != 255:
    #             print(pix)


def to_grayscale(pixels, width, height):
    def to_gs(r, g, b, a):
        return int(r * 0.2989 + g * 0.5870 + b * 0.1140) if a else 255

    gs_pixels = [
        [to_gs(r, g, b, a)
         for r, g, b, a in
         [row[idx:idx + 4]
          for idx in range(0, len(row), 4)]]
        for row in pixels]

    return gs_pixels, width, height


def load(filename):
    with open(filename, 'rb') as f:
        r = png.Reader(file=f)
        width, height, pixel_iter, metadata = r.asRGBA8()
        pixels = list(pixel_iter)
    print(metadata)
    return to_grayscale(pixels, width, height)


def save(pixels, width, height, filename):
    with open(filename, 'wb') as f:
        w = png.Writer(width, height, greyscale=True, alpha=False, bitdepth=8, planes=1, interlace=0, size=(width, height))
        w.write(f, pixels)
