from ui import Shape, Line, Point, Rect, UI
from math import sqrt
from algorithms import a_star, distance
from typing import Iterable
import time


thing = Shape(
    (4, 6),
    (6, 6),
    (6, 4),
    (7, 4),
    (7, 7),
    (4, 7)
)

thing2 = Shape(
    (5, 0),
    (5, 4),
    (6, 4),
    (6, 0)
)

all_lines = list(thing.lines) + list(thing2.lines)


def neighbors(point: Point):
    candidates = {Point(point.x - 1, point.y), Point(point.x + 1, point.y), Point(point.x, point.y - 1),
                  Point(point.x, point.y + 1), Point(point.x - 1, point.y - 1), Point(point.x - 1, point.y + 1),
                  Point(point.x + 1, point.y - 1), Point(point.x + 1, point.y + 1)}

    for cand in set(candidates):
        # if cand.x < 0 or cand.y < 0:
        #     candidates.remove(cand)
        #     continue
        if any(cand in line for line in all_lines):
            candidates.remove(cand)
            continue

    return candidates


ui = UI(screen_dim=Rect((0, -4), (13, 10)), bg_color="white")

ui.add(thing, thing2, width=20)
ui.render()

pathbuf = None


def draw_path(points: Iterable[Point]):
    global pathbuf

    # if pathbuf is not None:
        # ui.remove(*pathbuf, width=20, color="red")
    tmp = list(points)
    lin = list(Line(x, y) for x, y in zip(tmp[:-1], tmp[1:]))
    pathbuf = lin
    ui.add(*pathbuf, width=10, color="blue")
    ui.render()
    # time.sleep(0.4)


res = a_star(
    Point(8, 2),
    Point(5, 5),
    neighbors,
    distance,
    lambda point: distance(point, Point(5, 5)),
    draw_path
)

if not res:
    print("no path")

res_list = list(res)
res_lines = [Line(x, y) for x, y in zip(res_list[:-1], res_list[1:])]

ui.add(*res_lines, width=20, color="red")

ui.done()
