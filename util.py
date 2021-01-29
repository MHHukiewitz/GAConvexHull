from collections import deque
from math import sqrt
from typing import Sequence, List, Deque

from entities import Point, Segment


def sort_left_right(P: Sequence[Point]) -> Sequence[Point]:
    return sorted(P, key=lambda p: p.x)


def abc_line(mirror_s):
    """A line (segment) can be represented as: a*x + b*y + c = 0
    see: https://stackoverflow.com/questions/8954326/how-to-calculate-the-mirror-point-along-a-line"""
    a = mirror_s.q.y - mirror_s.p.y
    b = -(mirror_s.q.x - mirror_s.p.x)
    c = -a * mirror_s.p.x - b * mirror_s.p.y
    # normalize
    m = sqrt(a ** 2 + b ** 2)
    a /= m
    b /= m
    c /= m
    return a, b, c


def mirror_points(P: Sequence[Point], mirror_s: Segment) -> List[Point]:
    """Produces a set of points mirrored along a given line."""
    mirrored_P: Deque[Point]

    a, b, c = abc_line(mirror_s)

    mirrored_P = deque()
    for p in P:
        D = a * p.x + b * p.y + c
        mirrored_P.append(Point(p.x - 2 * a * D, p.y - 2 * b * D, name=p.name))
    return list(mirrored_P)


def mirror_segments(S: Sequence[Segment], mirror_s: Segment) -> List[Segment]:
    """Produces a set of segments mirrored along a given line."""
    mirrored_S: Deque[Segment]

    a, b, c = abc_line(mirror_s)

    mirrored_S = deque()
    for s in S:
        Dp = a * s.p.x + b * s.p.y + c
        Dq = a * s.q.x + b * s.q.y + c
        mirrored_S.append(Segment(
            Point(s.p.x - 2 * a * Dp, s.p.y - 2 * b * Dp, name=s.p.name),
            Point(s.q.x - 2 * a * Dq, s.q.y - 2 * b * Dq, name=s.p.name)))
    return list(mirrored_S)