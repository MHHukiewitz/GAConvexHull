from typing import Sequence, Deque
import random
import matplotlib.pyplot as plt
from math import *
from collections import deque


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


def sort_left_right(P: Sequence[Point]) -> Sequence[Point]:
    return sorted(P, key=lambda p: p.x)


def graham_scan(P: Sequence[Point]) -> Sequence[Point]:
    upper_CH: Deque[Point]
    upper_CH_segs: Deque[Segment]

    plt.axes()  # prepare drawing

    sorted_P = sort_left_right(P)
    equator = Segment(sorted_P[0], sorted_P[-1])  # line seperating upper and lower convex hull

    upper_P = list(filter(lambda p: p.y >= equator.height_at(p.x), sorted_P))

    upper_CH = deque()            # stack
    upper_CH.extend(upper_P[:2])  # upper convex hull
    upper_CH_segs = deque()
    upper_CH_segs.append(Segment(upper_CH[0], upper_CH[1]))

    for q in upper_P[2:]:
        s = Segment(upper_CH[-1], q)
        delta_m = upper_CH_segs[-1].m - s.m  # vertical up, now again up
        if delta_m is nan or delta_m > 0:  # has this segment a convex angle to the last?
            upper_CH.append(q)               # then just add
            upper_CH_segs.append(s)
        else:                             # is concave angle?
            popped = False
            for i in reversed(range(0, len(upper_CH) - 1)):  # go over last added points
                p = upper_CH[i]
                temp_seg = Segment(p, q)  # and make temporary segments
                # is new segment less steep or equal? Or are both points on the same spot?
                if temp_seg.m <= s.m or p.x == q.x and p.y == q.y:
                    upper_CH.pop()        # then remove last segment
                    plt.gca().add_line(upper_CH_segs[-1].line('grey'))
                    upper_CH_segs.pop()   # and point
                    s = temp_seg        # continue with new segment
                    popped = True
                else:
                    break
            if popped:                    # removed some previous points?
                upper_CH.append(q)        # then also add
                upper_CH_segs.append(s)

    lower_P = list(filter(lambda p: p.y < equator.height_at(p.x), sorted_P))

    # draw something
    plt.scatter([p.x for p in upper_P], [p.y for p in upper_P], c='red')
    plt.scatter([p.x for p in lower_P], [p.y for p in lower_P], c='blue')
    for s in upper_CH_segs:
        plt.gca().add_line(s.line())
        print(f"{s}: m = {round(s.m, 2)}, height_at({s.q.x}) = {s.height_at(s.q.x)}")
    plt.show()

    return upper_CH


POINT_CNT = 20

points = [Point(random.randint(0, 10), random.randint(0, 10)) for i in range(POINT_CNT)]
print(points)

graham_scan(points)


# super cool segments from left to right
"""
segments = [Segment(sorted_points[i], sorted_points[i+1]) for i in range(POINT_CNT-1)]
for s in segments:
    print(f"{s}: m = {round(s.m, 2)}, height_at({s.q.x}) = {s.height_at(s.q.x)}")

plt.axes()
plt.scatter([p.x for p in sorted_points], [p.y for p in sorted_points])
for s in segments:
    plt.gca().add_line(s.line())

plt.show()
"""