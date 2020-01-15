from ui import Shape, Line, Point, UI
from math import sqrt
from algorithms import a_star, distance


thing = Shape(
    Point(4, 6),
    Point(6, 6),
    Point(6, 4),
    Point(7, 4),
    Point(7, 7),
    Point(4, 7)
)

thing2 = Shape(
    Point(5, 0),
    Point(5, 2),
    Point(6, 2),
    Point(6, 0)
)

all_lines = list(thing.lines) + list(thing2.lines)


def neighbors(point: Point):
    candidates = {Point(point.x - 1, point.y), Point(point.x + 1, point.y), Point(point.x, point.y - 1),
                  Point(point.x, point.y + 1), Point(point.x - 1, point.y - 1), Point(point.x - 1, point.y + 1),
                  Point(point.x + 1, point.y - 1), Point(point.x + 1, point.y + 1)}

    for cand in set(candidates):
        if cand.x < 0 or cand.y < 0:
            candidates.remove(cand)
            continue
        if any(cand in line for line in all_lines):
            candidates.remove(cand)
            continue

    return candidates


res = a_star(
    Point(8, 0),
    Point(5, 5),
    neighbors,
    distance,
    lambda point: distance(point, Point(5, 5))
)

if not res:
    print("no path")
    exit(0)

points = list(res)
lines = [Line(x, y) for x, y in zip(points[:-1], points[1:])]

ui = UI(bg_color="white")

ui.add(thing, width=20)
ui.add(thing2, width=20)
ui.add(*lines, width=20, color="red")

ui.render()
