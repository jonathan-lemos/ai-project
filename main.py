from ui import Shape, Line, Point, Rect, UI, Number, Coord, conv_coord
from algorithms import ara, distance
from typing import Iterable
import time
import sys


def neighbors_free_space(lines: Iterable[Line], grid_size: Number, point: Point):
    candidates = {Point(point.x - grid_size, point.y), Point(point.x + grid_size, point.y),
                  Point(point.x, point.y - grid_size),
                  Point(point.x, point.y + grid_size), Point(point.x - grid_size, point.y - grid_size),
                  Point(point.x - grid_size, point.y + grid_size),
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


ui = UI(screen_dim=Rect((-1, -1), (36, 21)), bg_color="white")


def do_thing(arena, goal, start):
    ui.add("blue lines = searched paths; red line = current path; green line = complete path;",
           coord=ui.dimensions().upper_left, align="left")

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
            if any(l.intersects(x) and l.point_of_intersection(x) != l.point1 and l.point_of_intersection(x) != l.point2
                   for
                   x in arena_lines):
                candidates.remove(cand)

        return candidates

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
        nonlocal pathbuf

        if pathbuf is not None:
            ui.remove(*pathbuf, width=8, color="red")
            ui.add(*pathbuf, width=8, color="deep sky blue")
        tmp = list(points)
        lin = list(Line(x, y) for x, y in zip(tmp[:-1], tmp[1:]))
        pathbuf = lin
        ui.add(*pathbuf, width=8, color="red")
        time.sleep(0.25)

    for path, color in zip(ara(
            conv_coord(start),
            conv_coord(goal),
            arena_neighbors,
            # lambda point: neighbors_free_space(ui_lines, 1, point),
            distance,
            [100, 50, 20, 1],
            lambda point: distance(point, Point(*goal)),
                    # draw_path,
            #        max_cost
    ), ["red", "green", "blue", "purple"]):
        res_list = list(path)
        res_lines = [Line(x, y) for x, y in zip(res_list[:-1], res_list[1:])]

        ui.add(res_lines, width=10, color=color)


arena1 = [
    Rect((2, 1), (17, 6)),
    Shape((1, 9), (0, 14), (6, 19), (9, 15), (7, 8)),
    Shape((10, 8), (12, 15), (14, 8)),
    Shape((14, 13), (14, 19), (18, 20), (20, 17)),
    Shape((19, 3), (18, 10), (23, 6)),
    Rect((22, 19), (28, 9)),
    Shape((28, 1), (25, 2), (25, 6), (28.5, 8), (31, 6), (31, 2)),
    Shape((32, 8), (29, 17), (31, 19), (34, 16))
]
goal1 = Point(34, 19)
start1 = Point(1, 3)

arena2 = [
    Rect((1, 0), (7, 12)),
    Rect((1, 14), (7, 19)),
    Shape((8, 4), (15, 11), (20, 1)),
    Shape((20, 8), (20, 19), (10, 19), (10, 15)),
    Shape((34, 15), (28, 15), (25, 13), (27, 11), (29, 9)),
    Rect((33, 19), (32, 17))
]

goal2 = Point(34, 17)
start2 = Point(0, 0)

do_thing(arena1, goal1, start1)

# ui.done()
# time.sleep(3)
