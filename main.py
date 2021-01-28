from typing import Sequence, Deque
import random
import matplotlib.pyplot as plt
from math import *
from collections import deque

from entities import Point, Segment


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