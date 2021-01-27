from typing import Sequence
import random
import matplotlib.pyplot as plt
from math import *


class Point:
    _name: str
    x: float
    y: float

    def __init__(self, x, y, name=None):
        self.x = x
        self.y = y
        self._name = name

    def __repr__(self):
        return f"{'' if self._name is None else self._name}({self.x}, {self.y})"

    def __str__(self):
        return f"{'Point' if self._name is None else self._name}({self.x}, {self.y})"


class Segment:
    name: str
    p: Point
    q: Point

    def __init__(self, p, q, name=None):
        self.name = name
        self.p = p
        self.q = q

    def length(self):
        return sqrt((self.p.x - self.q.x) ** 2 + (self.p.y - self.q.y) ** 2)

    def __repr__(self):
        return f"{'' if self.name is None else self.name}({self.p.__repr__()} {self.q.__repr__()})"

    def line(self) -> plt.Line2D:
        return plt.Line2D((self.p.x, self.q.x), (self.p.y, self.q.y), label=self.m)

    @property
    def m(self) -> float:
        if self.p.y == self.q.y:
            return 0
        elif self.p.x == self.q.x:
            return inf
        return (self.p.y - self.q.y) / (self.p.x - self.q.x)


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
