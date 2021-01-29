from collections import deque
from math import inf, sqrt
from typing import List

from matplotlib import pyplot as plt


# TODO: x, y not setable
class Point:
    name: str
    x: float
    y: float

    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self):
        return f"{'' if self.name is None else self.name}({self.x}, {self.y})"

    def __str__(self):
        return f"{'Point' if self.name is None else self.name}({self.x}, {self.y})"


# TODO: points setable
class Segment:
    _name: str
    _p: Point
    _q: Point
    _m: float

    def __init__(self, p, q, name=None):
        self._name = name
        self._p = p
        self._q = q
        if self.p.x == self.q.x:
            if self.p.y < self.q.y:
                self._m = inf
            elif self.p.y > self.q.y:
                self._m = -inf
            else:
                self._m = 0
        else:
            if self.p.y == self.q.y:
                self._m = 0
            else:
                self._m = (self.p.y - self.q.y) / (self.p.x - self.q.x)

    def __repr__(self):
        return f"{'' if self.name is None else self.name}({self.p.__repr__()} {self.q.__repr__()})"

    def length(self):
        return sqrt((self.p.x - self.q.x) ** 2 + (self.p.y - self.q.y) ** 2)

    def line(self, _color=None) -> plt.Line2D:
        return plt.Line2D((self.p.x, self.q.x), (self.p.y, self.q.y), label=self.m, color=_color)

    def height_at(self, x: float) -> float:
        return self.p.y - (self.p.x - x) * self.m

    @property
    def name(self) -> str:
        return self._name

    @property
    def p(self) -> Point:
        return self._p

    @property
    def q(self) -> Point:
        return self._q

    @property
    def m(self) -> float:
        return self._m


class Polygon:
    name: str
    points: List[Point]
    segments: List[Segment]

    def __init__(self, points: List[Point]):
        segs = deque()
        segs.append(Segment(points[0], points[1]))
        for p in points[2:]:
            segs.append(Segment(segs[-1].q, p))
        segs.append(Segment(points[-1], points[0]))
        self.segments = list(segs)
