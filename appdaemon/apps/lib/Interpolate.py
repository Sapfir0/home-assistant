import bisect

class Interpolate:
    def __init__(self, xs, ys):
        if any(y - x <= 0 for x, y in zip(xs, xs[1:])):
            raise ValueError("xs must be in strictly ascending order!")
        assert len(xs) == len(ys)
        self.xs = xs
        self.ys = ys
        intervals = zip(xs, xs[1:], ys, ys[1:])
        self.slopes = [(y2 - y1) / (x2 - x1) for x1, x2, y1, y2 in intervals]

    def __call__(self, x):
        if not (self.xs[0] <= x <= self.xs[-1]):
            raise ValueError("x out of bounds!")
        if x == self.xs[-1]:
            return self.ys[-1]
        i = bisect.bisect_right(self.xs, x) - 1
        return self.ys[i] + self.slopes[i] * (x - self.xs[i])
