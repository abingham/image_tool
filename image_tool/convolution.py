from .util import zeros


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


def convolve_cell(kernel, data, col, row):
    result = sum(
        kernel[kernel_row, kernel_col] * data[row + kernel_row][col + kernel_col]
        for kernel_col in (-1, 0, 1)
        for kernel_row in (-1, 0, 1))
    result = min(result, 255)
    return max(result, 0)


def convolve(data, height, width, kernel):
    dest = zeros(width, height)
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            val = convolve_cell(kernel, data, col=col, row=row)
            dest[row][col] = val

    return dest
