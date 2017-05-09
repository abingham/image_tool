def maximum(*iters):
    return [
        [max(vals) for vals in zip(*rows)]
        for rows in zip(*iters)]


def zeros(width, height):
    return [[0] * width for _ in range(height)]
