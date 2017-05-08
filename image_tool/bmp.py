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
        col, row = index
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


def convolve_cell(kernel, data, col, row):
    return sum(
        kernel[row_offset, col_offset] * data[row + row_offset][col + col_offset][1]
        for col_offset in (-1, 0, 1)
        for row_offset in (-1, 0, 1))


def convolve(data, height, width, dest, kernels):
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            val = data[row][col]
            val = max(convolve_cell(k, data, col=col, row=row)
                      for k in kernels)
            val = min(val, 255)
            val = max(val, 0)
            dest[row][col] = [0, val, 0]


def detect_edges(data, height, width, dest):
    convolve(data, height, width, dest, EDGE_DETECTOR_KERNELS)


data = load('llama.bmp')
edges = data.copy()
detect_edges(data.pixels, data.height, data.width, edges.pixels)
save(edges, 'foobar.bmp')
