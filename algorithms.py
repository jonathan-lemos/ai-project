from collections import defaultdict
from functools import reduce
from math import sqrt
from typing import Callable, Iterable, Union
from ui import Number, Point


def distance(p1: Point, p2: Point) -> Number:
    """
    Distance formula. Returns the straight-line distance between two points.
    :param p1: The first point.
    :param p2: The second point.
    :return: A Number representing the distance between these two points.
    """
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def a_star(start: Point, end: Point, get_neighbors: Callable[[Point], Iterable[Point]],
           get_distance: Callable[[Point, Point], Number] = distance,
           heuristic: Callable[[Point], Number] = lambda point: 0) -> Union[
    Iterable[Point], None]:
    """
    Returns a path between the start and end points.
    This will always be the shortest path as long as the heuristic does not overestimate the cost between two points.
    :param start: The point to start from.
    :param end: The destination.
    :param get_neighbors: A function that takes a Point and returns its neighbors.
    If a destination cannot be found and get_neighbors continually returns new points (the search space is infinite),
    this function will never return
    :param get_distance: A function that computes the cost to travel between two given Points
    By default this is the distance formula.
    :param heuristic: A function that estimates the cost from a point to the destination.
    A heuristic should never overestimate the actual cost if the optimal path is needed.
    Higher heuristics find a destination faster, but the path will be less optimal.
    By default this is a function that always returns 0.
    :return: An Iterable of points representing the path from start to end, or None if no path could be found.
    """

    to_search = {start}

    prev = {}
    cost = defaultdict(lambda: float("inf"))
    cost_with_heuristic = defaultdict(lambda: float("inf"))

    cost[start] = 0
    cost_with_heuristic[start] = heuristic(start)

    while len(to_search) > 0:
        current = reduce(lambda a, c: a if cost_with_heuristic[a] <= cost_with_heuristic[c] else c, to_search)
        to_search.remove(current)

        if current == end:
            path = []
            tmp = current
            while tmp != start:
                path.append(tmp)
                tmp = prev[tmp]
            path.append(start)
            return reversed(path)

        for neighbor in get_neighbors(current):
            calc = cost[current] + get_distance(current, neighbor)

            if calc < cost[neighbor]:
                prev[neighbor] = current
                cost[neighbor] = calc
                cost_with_heuristic[neighbor] = calc + heuristic(neighbor)
                to_search.add(neighbor)
    return None
