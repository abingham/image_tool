from .convolution import convolve, Kernel
from .util import maximum

FALER_KERNELS = [
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


def detect_edges(src, height, width):
    convs = (convolve(src, height, width, k)
             for k in FALER_KERNELS)
    return maximum(*convs)
