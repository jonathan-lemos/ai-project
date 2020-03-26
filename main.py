from ui import Shape, Line, Point, Rect, UI, Number, Coord, conv_coord
from algorithms import ara, distance
from typing import Iterable
import time
import sys


def should_try_intersect(l1: Line, l2: Line):
    return l1.x_left - 0.0005 <= l2.x_right + 0.0005 and l1.x_right + 0.0005 >= l2.x_left - 0.0005 and l1.y_bottom - 0.0005 <= l2.y_top + 0.0005 and l1.y_top + 0.0005 >= l2.y_bottom - 0.0005


def neighbors_free_space(lines: Iterable[Line], grid_size: Number, point: Point, diagonals=True):
    if diagonals:
        candidates = {Point(point.x - grid_size, point.y), Point(point.x + grid_size, point.y),
                      Point(point.x, point.y - grid_size),
                      Point(point.x, point.y + grid_size), Point(point.x - grid_size, point.y - grid_size),
                      Point(point.x - grid_size, point.y + grid_size),
                      Point(point.x + grid_size, point.y - grid_size), Point(point.x + grid_size, point.y + grid_size)}
    else:
        candidates = {Point(point.x, point.y - grid_size),
                      Point(point.x, point.y + grid_size),
                      Point(point.x + grid_size, point.y),
                      Point(point.x - grid_size, point.y)}

    for cand in set(candidates):
        line = Line(point, cand)
        if not (0 <= cand.x <= 50 and 0 <= cand.y <= 50):
            candidates.remove(cand)
            continue
        if any(should_try_intersect(line, line2) and line.intersects(line2) for line2 in lines):
            candidates.remove(cand)
            continue

    return candidates


ui = UI(screen_dim=Rect((-1, -1), (51, 51)), bg_color="white")


def do_thing(arena, goal, start):
    # ui.add("blue lines = searched paths; red line = current path; green line = complete path;",
    #       coord=ui.dimensions().upper_left, align="left")

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
            if any(should_try_intersect(l, x) and l.intersects(x) and l.point_of_intersection(
                    x) != l.point1 and l.point_of_intersection(x) != l.point2
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

    def draw_path(p1: Point, p2: Point):
        ui.add(Line(p1, p2), width=8, color="orange")
        # time.sleep(0.25)

    for path, color in zip(ara(
            conv_coord(start),
            conv_coord(goal),
            # arena_neighbors,
            lambda point: neighbors_free_space(ui_lines, 1, point, True),
            distance,
            [100, 20, 2, 1],
            # lambda point: abs(point.x - goal.x) + abs(point.y - goal.y),
            lambda point: distance(point, goal),
            draw_path,
            #        max_cost
    ), ["red", "green", "blue", "purple"]):
        res_list = list(path)
        res_lines = [Line(x, y) for x, y in zip(res_list[:-1], res_list[1:])]

        ui.add(res_lines, width=10, color=color)


arena_blank = [
    [],
    Point(50, 50),
    Point(0, 0)
]

arena1 = [
    [
        Rect((0, 40), (40, 30)),
        Rect((8, 47), (3, 48)),
        Rect((6, 47), (7, 42)),
        Shape((10, 50), (17, 42), (25, 46), (20, 50)),
        Shape((40, 45), (40, 35), (48, 40)),
        Shape((10, 10), (15, 22), (20, 10)),
        Rect((21, 30), (27, 15)),
        Shape((25, 1), (30, 28), (42, 28), (48, 1))
    ],
    Point(1, 46),
    Point(1, 1)
]

do_thing(*arena1)

ui.done()
# time.sleep(3)
