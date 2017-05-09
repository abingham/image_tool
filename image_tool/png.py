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


def to_grayscale(filename, outfilename):
    with open(filename, 'rb') as f:
        r = png.Reader(file=f)
        width, height, pixel_iter, metadata = r.asRGBA8()
        pixels = list(pixel_iter)

    def _pixels(row):
        for idx in range(0, len(row), 4):
            yield row[idx:idx + 4]

    def to_gs(r, g, b, a):
        if a == 0:
            return 255
        else:
            return int(r * 0.2989 + g * 0.5870 + b * 0.1140)

    gs_pixels = [
        [to_gs(r, g, b, a)
         for r, g, b, a in _pixels(row)]
        for row in pixels]

    with open(outfilename, 'wb') as f:
        w = png.Writer(width, height, greyscale=True, alpha=False, bitdepth=8)
        w.write(f, gs_pixels)


to_grayscale('llama.png', 'gs_llama.png')
