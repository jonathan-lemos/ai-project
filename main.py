from ui import Shape, Line, Point, Rect, UI, Number, Coord, conv_coord
from algorithms import a_star, distance
from typing import Iterable
import time


def neighbors_free_space(lines: Iterable[Line], grid_size: Number, point: Point):
    candidates = {Point(point.x - grid_size, point.y), Point(point.x + grid_size, point.y), Point(point.x, point.y - grid_size),
                  Point(point.x, point.y + grid_size), Point(point.x - grid_size, point.y - grid_size), Point(point.x - grid_size, point.y + grid_size),
                  Point(point.x + grid_size, point.y - grid_size), Point(point.x + grid_size, point.y + grid_size)}

    for cand in set(candidates):
        line = Line(point, cand)
        # if cand.x < 0 or cand.y < 0:
        #     candidates.remove(cand)
        #     continue
        if any(line.intersects(line2) for line2 in lines):
            candidates.remove(cand)
            continue

    return candidates


arena = [
    Rect((2, 1), (17, 6)),
    Shape((1, 9), (0, 14), (6, 19), (9, 15), (7, 8)),
    Shape((10, 8), (12, 15), (14, 8)),
    Shape((14, 13), (14, 19), (18, 20), (20, 17)),
    Shape((19, 3), (18, 10), (23, 6)),
    Rect((22, 19), (28, 9)),
    Shape((28, 1), (25, 2), (25, 6), (28.5, 8), (31, 6), (31, 2)),
    Shape((32, 8), (29, 17), (31, 19), (34, 16))
]

goal = Point(34, 19)
start = Point(1, 3)

arena_points = {}
for shape in arena:
    for i, line in enumerate(shape.lines):
        arena_points[line.point1] = (shape, shape.lines[i - 1].point1, line.point2)

arena_lines = [line for shape in arena for line in shape.lines]


def arena_neighbors(point: Point):
    candidates = {Point(*goal)}

    if point in arena_points:
        sha, p1, p2 = arena_points[point]
        candidates |= {p1, p2}
    else:
        sha = None

    for shape in arena:
        if shape == sha:
            continue
        candidates |= set(shape.points)

    for cand in list(candidates):
        l = Line(point, cand)
        if any(l.intersects(x) and l.point_of_intersection(x) != l.point1 and l.point_of_intersection(x) != l.point2 for x in arena_lines):
            candidates.remove(cand)

    return candidates


ui = UI(screen_dim=Rect((-1, -1), (36, 21)), bg_color="white")

ui.add(*arena, width=8)

ui_lines = list(ui.lines())


def cross(center: Coord, leg_len: Number):
    cen = conv_coord(center)
    hx = cen.x + leg_len
    hy = cen.y + leg_len
    lx = cen.x - leg_len
    ly = cen.y - leg_len

    return [
        Line((hx, hy), (lx, ly)),
        Line((hx, ly), (lx, hy))
    ]


ui.add(*cross(goal, 0.5), width=6, color="green")
ui.add(*cross(start, 0.5), width=6, color="red")
ui.render()
ui.add("goal", coord=goal + (1, 1), align="left")
ui.add("start", coord=start - (1, 1), align="right")

pathbuf = None


def draw_path(points: Iterable[Point]):
    global pathbuf

    if pathbuf is not None:
        ui.remove(*pathbuf, width=8, color="red")
        ui.add(*pathbuf, width=8, color="deep sky blue")
    tmp = list(points)
    lin = list(Line(x, y) for x, y in zip(tmp[:-1], tmp[1:]))
    pathbuf = lin
    ui.add(*pathbuf, width=8, color="red")
    time.sleep(0.25)


res = a_star(
    conv_coord(start),
    conv_coord(goal),
    arena_neighbors,
    # lambda point: neighbors_free_space(ui_lines, 0.5, point),
    distance,
    lambda point: distance(point, Point(*goal)),
    draw_path
)

if not res:
    print("no path")
    exit(0)

res_list = list(res)
res_lines = [Line(x, y) for x, y in zip(res_list[:-1], res_list[1:])]

ui.add(res_lines, width=10, color="green")

ui.remove(arena[0], width=8)

ui.done()
