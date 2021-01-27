from typing import Sequence
import random
import matplotlib.pyplot as plt
from math import *


class Point:
    _name: str
    _x: float
    _y: float

    def __init__(self, x, y, name=None):
        self._x = x
        self._y = y
        self._name = name

    def __repr__(self):
        return f"{'' if self._name is None else self._name}({self.x}, {self.y})"

    def __str__(self):
        return f"{'Point' if self._name is None else self._name}({self.x}, {self.y})"

    @property
    def name(self) -> str:
        return self._name

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

class Segment:
    name: str
    _p: Point
    _q: Point
    _m: float

    def __init__(self, p, q, name=None):
        self.name = name
        self._p = p
        self._q = q
        if self.p.x == self.q.x:
            self._m = inf
        else:
            self._m = (self.p.y - self.q.y) / (self.p.x - self.q.x)

    def length(self):
        return sqrt((self.p.x - self.q.x) ** 2 + (self.p.y - self.q.y) ** 2)

    def __repr__(self):
        return f"{'' if self.name is None else self.name}({self.p.__repr__()} {self.q.__repr__()})"

    def line(self) -> plt.Line2D:
        return plt.Line2D((self.p.x, self.q.x), (self.p.y, self.q.y), label=self.m)

    @property
    def p(self) -> Point:
        return self._p

    @property
    def q(self) -> Point:
        return self._q

    @property
    def m(self) -> float:
        return self._m


def sort_left_right(P: Sequence[Point]) -> Sequence[Point]:
    return sorted(P, key=lambda p: p.x)


def graham_scan(P: Sequence[Point]) -> Sequence[Point]:
    upper_CH: Sequence[Point]

    sorted_P = sort_left_right(P)
    equator = Segment(sorted_P[0], sorted_P[-1])  # line seperating upper and lower convex hull
    upper_CH = [sorted_P[0]]  # upper convex hull


    # TODO: Convex Hull...
    return upper_CH


POINT_CNT = 20

points = [Point(random.randint(0, 100), random.randint(0, 100)) for i in range(POINT_CNT)]
print(points)
sorted_points = sort_left_right(points)
print(sorted_points)


# super cool segments from left to right
segments = [Segment(sorted_points[i], sorted_points[i+1]) for i in range(POINT_CNT-1)]
for s in segments:
    print(f"{s} = {round(s.m, 2)}")

plt.axes()
plt.scatter([p.x for p in sorted_points], [p.y for p in sorted_points])
for s in segments:
    plt.gca().add_line(s.line())

plt.show()
