from typing import Sequence, Deque, List
import random
import matplotlib.pyplot as plt
from math import *
from collections import deque

from entities import Point, Segment
from util import sort_left_right

DEBUG = True


def graham_scan(P: Sequence[Point]) -> List[Point]:
    upper_CH: Deque[Point]
    upper_CH_segs: Deque[Segment]

    plt.axes()  # prepare drawing

    sorted_P = sort_left_right(P)
    middle_line = Segment(sorted_P[0], sorted_P[-1])  # line seperating upper and lower convex hull
    middle_line.p.name = 'mid_p'
    middle_line.q.name = 'mid_q'
    upper_P = list(filter(lambda p: p.y >= middle_line.height_at(p.x), sorted_P))

    upper_CH, upper_CH_segs = upper_graham_scan(upper_P)

    lower_P = list(filter(lambda p: p.y <= middle_line.height_at(p.x), sorted_P))

    #mirrored_lower_P = sort_left_right(mirror_points(lower_P, middle_line))

    #mirrored_lower_CH, mirrored_lower_CH_segs = upper_graham_scan(mirrored_lower_P)
    '''Because of issues with mirrored points having larger/smaller x-coordinates than 
    mid_p and mid_q, simply mirroring lower_P and putting them in upper_graham_scan() didn't work
    as expected. Attempts to resolve this failed unspectacularly.'''
    lower_CH, lower_CH_segs = lower_graham_scan(lower_P)
    #lower_CH = mirror_points(mirrored_lower_CH, middle_line)
    #lower_CH_segs = mirror_segments(mirrored_lower_CH_segs, middle_line)

    # draw something
    if DEBUG:
        plt.scatter([p.x for p in upper_P], [p.y for p in upper_P], c='red')
        plt.scatter([p.x for p in lower_P], [p.y for p in lower_P], c='blue')

        plt.gca().add_line(middle_line.line())

        for s in upper_CH_segs:
            plt.gca().add_line(s.line())
            print(f"{s}: m = {round(s.m, 2)}, height_at({s.q.x}) = {s.height_at(s.q.x)}")
        for s in lower_CH_segs:
            plt.gca().add_line(s.line())
            print(f"{s}: m = {round(s.m, 2)}, height_at({s.q.x}) = {s.height_at(s.q.x)}")
        plt.show()

    return upper_CH + list(reversed(lower_CH))


def upper_graham_scan(upper_P: Sequence[Point]) -> (List[Point], List[Segment]):
    upper_CH = deque()            # stack
    upper_CH.extend(upper_P[:2])  # upper convex hull
    upper_CH_segs = deque()
    upper_CH_segs.append(Segment(upper_CH[0], upper_CH[1]))
    for q in upper_P[2:]:
        s = Segment(upper_CH[-1], q)
        delta_m = upper_CH_segs[-1].m - s.m  # vertical up, now again up
        if delta_m is nan or delta_m > 0:  # has this segment a convex angle to the last?
            upper_CH.append(q)  # then just add
            upper_CH_segs.append(s)
        else:  # is concave angle?
            popped = False
            for i in reversed(range(0, len(upper_CH) - 1)):  # go over last added points
                p = upper_CH[i]
                temp_seg = Segment(p, q)  # and make temporary segments
                # is new segment less steep or equal? Or are both points on the same spot?
                if temp_seg.m <= s.m or p.x == q.x and p.y == q.y:
                    upper_CH.pop()  # then remove last segment
                    if DEBUG:
                        plt.gca().add_line(upper_CH_segs[-1].line('grey'))
                    upper_CH_segs.pop()  # and point
                    s = temp_seg  # continue with new segment
                    popped = True
                else:
                    break
            if popped:  # removed some previous points?
                upper_CH.append(q)  # then also add
                upper_CH_segs.append(s)

    return list(upper_CH), list(upper_CH_segs)


def lower_graham_scan(lower_P: Sequence[Point]) -> (List[Point], List[Segment]):
    lower_CH = deque()            # stack
    lower_CH.extend(lower_P[:2])  # upper convex hull
    lower_CH_segs = deque()
    lower_CH_segs.append(Segment(lower_CH[0], lower_CH[1]))
    for q in lower_P[2:]:
        s = Segment(lower_CH[-1], q)
        delta_m = lower_CH_segs[-1].m - s.m  # vertical down, now again down
        if delta_m is inf or delta_m < 0:  # [Difference] has this segment a convex angle to the last?
            lower_CH.append(q)  # then just add
            lower_CH_segs.append(s)
        else:  # is concave angle?
            popped = False
            for i in reversed(range(0, len(lower_CH) - 1)):  # go over last added points
                p = lower_CH[i]
                temp_seg = Segment(p, q)  # and make temporary segments
                # [Difference] is new segment more steep or equal? Or are both points on the same spot?
                if temp_seg.m >= s.m or p.x == q.x and p.y == q.y:
                    lower_CH.pop()  # then remove last segment
                    if DEBUG:
                        plt.gca().add_line(lower_CH_segs[-1].line('grey'))
                    lower_CH_segs.pop()  # and point
                    s = temp_seg  # continue with new segment
                    popped = True
                else:
                    break
            if popped:  # removed some previous points?
                lower_CH.append(q)  # then also add
                lower_CH_segs.append(s)

    return list(lower_CH), list(lower_CH_segs)


POINT_CNT = 1000


points = [Point(random.randint(0, 100), random.randint(0, 100)) for i in range(POINT_CNT)]

CH = graham_scan(points)

