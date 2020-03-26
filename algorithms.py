from collections import defaultdict
from math import sqrt
from prioritymap import prioritymap
from typing import Callable, Iterable, Optional
from ui import Coord, conv_coord, Number, Point


def distance(c1: Coord, c2: Coord) -> Number:
    """
    Distance formula. Returns the straight-line distance between two points.

    Args:
        c1 (Coord): The first coordinate.
        c2 (Coord): The second coordinate.

    Returns:
        A Number representing the euclidean distance between these two points.
    """

    p1 = conv_coord(c1)
    p2 = conv_coord(c2)
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def a_star(start: Coord,
           end: Coord,
           get_neighbors: Callable[[Point], Iterable[Point]],
           get_distance: Callable[[Point, Point], Number] = distance,
           heuristic: Callable[[Point], Number] = lambda point: 0,
           callback: Optional[Callable[[Iterable[Point]], None]] = None,
           max_cost: Optional[Number] = None) -> Optional[Iterable[Point]]:
    """
    Returns a path between the start and end points.
    This will always be the shortest path as long as the heuristic does not overestimate the cost between two points.

    Args:
        start (Coord): The point to start from.

        end (Coord): The destination.

        get_neighbors (Callable[[Point], Iterable[Point]]):
            A function that takes a Line and returns its neighbors.
            The line represents the search going from line.point1 to line.point2.
            Neighbors that have already been visited do not have to be removed from the result of this function.
            If a destination cannot be found and get_neighbors continually returns new points (the search space is infinite), this function will never return

        get_distance (Callable[[Point, Point], Number]):
            A function that computes the cost to travel between two given Points
            By default this is the distance formula.

        heuristic (Callable[[Point], Number]):
            A function that estimates the cost from a point to the destination.
            A heuristic should never overestimate the actual cost if the optimal path is needed.
            Higher heuristics find a destination faster, but the path will be less optimal.
            By default this is a function that always returns 0.

        callback (Optional[Callable[[Iterable[Point]], None]]:
            A callback that is called with every path this algorithm explores, or None to not use one.
            If this is not None, the algorithm will run slowly as the algorithm has to build

    Returns:
         An Iterable of points representing the path from start to end, or None if no path could be found.
    """

    start = conv_coord(start)
    end = conv_coord(end)

    to_search = prioritymap()
    searched = set()

    prev = {}
    cost = defaultdict(lambda: float("inf"))
    cost_with_heuristic = defaultdict(lambda: float("inf"))

    cost[start] = 0
    cost_with_heuristic[start] = heuristic(start)

    to_search[cost_with_heuristic[start]] = {start}

    def build_path(p: Point) -> Iterable[Point]:
        path = []
        tmp = p
        while tmp != start:
            path.append(tmp)
            tmp = prev[tmp]
        path.append(start)
        return reversed(path)

    while len(to_search) > 0:
        curr_cost, current_set = to_search.min()

        current = current_set.pop()
        if len(current_set) == 0:
            to_search.pop()
        if current in searched:
            continue

        if callback:
            callback(build_path(current))

        if current == end:
            return build_path(current)

        for neighbor in set(get_neighbors(current)) - searched:
            calc = cost[current] + get_distance(current, neighbor)

            if calc < cost[neighbor]:
                prev[neighbor] = current
                cost[neighbor] = calc

                cost_with_heuristic[neighbor] = calc + heuristic(neighbor)
                if max_cost and cost_with_heuristic[neighbor] > max_cost:
                    continue
                if cost_with_heuristic[neighbor] in to_search:
                    to_search[cost_with_heuristic[neighbor]].add(neighbor)
                else:
                    to_search[cost_with_heuristic[neighbor]] = {neighbor}

        searched.add(current)
    return None


def ara(start: Coord,
        end: Coord,
        get_neighbors: Callable[[Point], Iterable[Point]],
        get_distance: Callable[[Point, Point], Number] = distance,
        factors: Iterable[Number] = (10, 8, 6, 4, 2, 1),
        heuristic: Callable[[Point], Number] = lambda point: 0,
        callback: Optional[Callable[[Point, Point], None]] = None,
        ) -> Iterable[Iterable[Point]]:
    factors = list(factors)

    start = conv_coord(start)
    end = conv_coord(end)

    to_search = prioritymap()

    prev = {}
    prev[start] = start
    cost = defaultdict(lambda: float("inf"))
    cost_with_heuristic = defaultdict(lambda: float("inf"))

    cost[start] = 0
    cost_with_heuristic[start] = heuristic(start)

    to_search[cost_with_heuristic[start]] = {start}

    best_cost = float("inf")

    def build_path(p: Point) -> Iterable[Point]:
        path = []
        tmp = p
        while tmp != start:
            path.append(tmp)
            tmp = prev[tmp]
        path.append(start)
        return reversed(path)

    while len(to_search) > 0 and len(factors) > 0:
        curr_cost, current_set = to_search.min()

        current = current_set.pop()
        if len(current_set) == 0:
            to_search.pop()

        if callback:
            callback(prev[current], current)

        if current == end:
            # searched.remove(current)
            if cost[current] < best_cost:
                best_cost = cost[current]
                yield build_path(current)
            factors = factors[1:]

            if len(factors) == 0:
                break

            nodes = [x for s in to_search.values() for x in s]
            new_to_search = prioritymap()
            for node in nodes:
                ch = cost[node] + factors[0] * heuristic(node)
                cost_with_heuristic[node] = ch
                if ch in new_to_search:
                    new_to_search[ch].add(node)
                else:
                    new_to_search[ch] = {node}
            to_search = new_to_search

            continue

        for neighbor in set(get_neighbors(current)):
            calc = cost[current] + get_distance(current, neighbor)
            # hc = calc + factors[0] * heuristic(neighbor)

            if calc < cost[neighbor] and calc + heuristic(neighbor) < best_cost:
                prev[neighbor] = current
                cost[neighbor] = calc

                cost_with_heuristic[neighbor] = calc + factors[0] * heuristic(neighbor)
                if cost_with_heuristic[neighbor] in to_search:
                    to_search[cost_with_heuristic[neighbor]].add(neighbor)
                else:
                    to_search[cost_with_heuristic[neighbor]] = {neighbor}
    return None
