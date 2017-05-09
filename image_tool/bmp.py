from construct.examples.formats.graphics.bmp import bitmap_file


def load(filename):
    """Load a BMP file and return the `Construct` associated with it.

    The return value's `pixels` attribute is a 2D array of pixels where each
    pixel is a 3-element vector.
    """
    with open(filename, 'rb') as f:
        data = f.read()
    return bitmap_file.parse(data)


def save(data, filename):
    with open(filename, mode='wb') as f:
        bitmap_file.build_stream(data, f)


class Kernel:
    def __init__(self, k):
        self._k = k
        self._hoffset = len(k) // 2
        self._woffset = len(k[0]) // 2

    def __getitem__(self, index):
        row, col = index
        col += self._woffset
        row += self._hoffset
        return self._k[row][col]

EDGE_DETECTOR_KERNELS = [
    Kernel(k)
    for k in
    [
        [[-1, 0, 1],
         [-1, 0, 1],
         [-1, 0, 1]],
        [[1, 1, 1],
         [0, 0, 0],
         [-1, -1, -1]],
        [[-1, -1, -1],
         [-1, 8, -1],
         [-1, -1, -1]],
        [[0, 1, 0],
         [-1, 0, 1],
         [0, -1, 0]],
    ]
]


def maximum(*iters):
    for tup in zip(*iters):
        yield max(*tup)


def convolve_cell(kernel, data, col, row):
    result = sum(
        kernel[kernel_row, kernel_col] * data[row + kernel_row][col + kernel_col]
        for kernel_col in (-1, 0, 1)
        for kernel_row in (-1, 0, 1))
    result = min(result, 255)
    return max(result, 0)


def convolve(data, kernels):
    out = data.copy()
    for row in range(1, data.height - 1):
        for col in range(1, data.width - 1):
            val = data.pixels[row][col]
            val = max(convolve_cell(k, data.pixels,
                                    col=col, row=row)
                      for k in kernels)
            out.pixels[row][col] = val
    return out


def detect_edges(data):
    return convolve(data, EDGE_DETECTOR_KERNELS)


def to_grayscale(data):
    gs = data.copy()

    if data.bpp == 1:
        return gs

    gs.planes = 1

    for row in range(data.height):
        for col in range(data.width):
            r, g, b = data.pixels[row][col]
            gray = int(r * 0.2989 + g * 0.5870 + b * 0.1140)
            gs.pixels[row][col] = gray
    return gs


data = load('llama2.bmp')
gray = to_grayscale(data)
save(gray, 'gray.bmp')
edges = detect_edges(gray)
save(edges, 'edges.bmp')
