from ui import Shape, Line, Point, Rect, UI, Number, Coord, conv_coord
from algorithms import ara, distance
from typing import Iterable
import time
import sys
import random
import itertools


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

    for obj in arena:
        ui.add(obj, width=1, color=(0, 0, 0))

    # ui_lines = list(ui.lines())

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

    for line in cross(goal, 0.5):
        ui.add(line, width=6, color=(20, 130, 20))
    for line in cross(start, 0.5):
        ui.add(line, width=6, color=(130, 20, 20))
    ui.render()
    ui.print("goal", coord=goal + (-1, 1))
    ui.print("start", coord=start - (1, 1))

    def draw_path(p1: Point, p2: Point):
        ui.add(Line(p1, p2), width=3, color=(200, 150, 20))
        # time.sleep(0.25)

    for path, color in zip(ara(
            conv_coord(start),
            conv_coord(goal),
            # arena_neighbors,
            # lambda point: neighbors_free_space(ui_lines, 1, point, False),
            neighbors_grid,
            distance,
            [100, 20, 2, 1],
            # lambda point: abs(point.x - goal.x) + abs(point.y - goal.y),
            lambda point: distance(point, goal),
            draw_path,
            #        max_cost
    ), [(200, 20, 20), (20, 200, 20), (20, 20, 200), (200, 20, 255)]):
        res_list = list(path)
        res_lines = [Line(x, y) for x, y in zip(res_list[:-1], res_list[1:])]

        for line in res_lines:
            ui.add(line, width=6, color=color)
        time.sleep(1)


if len(sys.argv) < 3:
    print(f"Usage: {sys.argv[0]} [environment size - 100|200|300] [fill percent - 10|20|30]")
    sys.exit(0)

env_size = int(sys.argv[1])
env_fill = float(sys.argv[2]) / 100

ui = UI()

points = set(random.sample(list(itertools.product(range(env_size), repeat=2)), k=int(env_size ** 2 * env_fill)))
arena = [Rect(p, (p[0] + 1, p[1] + 1)) for p in points]


def neighbors_grid(p: Point):
    return {Point(int(p.x), int(p.y)), Point(int(p.x), int(p.y + 1)), Point(int(p.x + 1), int(p.y)), Point(int(p.x + 1), int(p.y + 1))} - points


do_thing(arena, Point(env_size, env_size), Point(0.5, 0.5))

ui.done()
# time.sleep(3)
