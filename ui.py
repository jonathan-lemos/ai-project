import numpy as np
from typing import Dict, Iterable, List, Optional, Tuple, Union
from math import sqrt
import pygame

Number = Union[int, float]


class Point:
    """Represents an (x, y) coordinate in 2D space.

    Attributes:
        x (Number): The x coordinate.
        y (Number): The y coordinate.
    """

    def __init__(self, x: Number, y: Number):
        """Creates a Point out of an x and y coordinate. These can be integers or floats.

        Args:
            x (Number): The x coordinate.
            y (Number): The y coordinate.
        """
        self.x = x
        self.y = y
        self.__hash = hash((self.x, self.y))

    def __add__(self, other: "Coord") -> "Point":
        """Does the vector addition of two points and returns their sum.

        Examples:
            Point(1, 2) + (3, 4) -> (4, 6)

        Args:
            other (Coord): A Point or (Number, Number) to add to this one.

        Returns:
            A new point containing the sum of the two points.
        """

        point = conv_coord(other)
        return Point(self.x + point.x, self.y + point.y)

    def __eq__(self, other) -> bool:
        """Returns True if this Point equals the argument, False if not
        The argument can be either a Point or a (Number, Number).

        Args:
            other (any): The argument to check against.

        Examples:
            Point(1, 2) == Point(1, 2) -> True
            Point(1, 2) == (1, 2)      -> True
            Point(1, 2) == Point(2, 1) -> False

        Returns:
            True if other is a Point or (Number, Number) with the same coordinates as this Point.
            False if the coordinates don't match or the argument is not a Point or (Number, Number)
        """

        if isinstance(other, Tuple):
            if len(other) != 2:
                return False
            if not (isinstance(other[0], int) or isinstance(other[0], float)) or \
                    not (isinstance(other[1], int) or isinstance(other[1], float)):
                return False
            other = conv_coord(other)
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __getitem__(self, index: int) -> Number:
        """Returns the x coordinate if the argument is 0, or the y coordinate if it is 1.
        In other words, this works the same way as indexing the equivalent (Number, Number)

        Args:
            index: An integer.

        Returns:
            The x or y coordinate if the argument is 0 or 1 respectively.
        """

        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise Exception(f"Points only have X (0) and Y (1) coordinates. You tried to index it with {index}.")

    def __hash__(self) -> int:
        """Returns a hash of this Point.
        This is the same hash as the equivalent (Number, Number).
        """

        return self.__hash

    def __iter__(self) -> Iterable[Number]:
        """
        Yields:
            The x coordinate, then the y coordinate.
            In other words, it is equivalent to iterating over the equivalent (Number, Number)

        Examples:
            [i for i in Point(1, 2)] -> [1, 2]
            x, y = Point(1, 2)       -> x is 1, y is 2.
            print(*Point(1, 2))      -> "1 2"
        """
        yield self.x
        yield self.y

    def __str__(self) -> str:
        """Returns a string representation of this point.
        This is the same string representation as the equivalent (Number, Number).
        """

        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        """Returns a string representation of this point.
        This is the same string representation as the equivalent (Number, Number).
        """

        return f"Point({self.x}, {self.y})"

    def __sub__(self, other: "Coord") -> "Point":
        """Does the vector subtraction of two points and returns their sum.

        Examples:
            Point(1, 2) - (3, 5) -> (-2, -3)

        Args:
            other (Coord): A Point or (Number, Number) to subtract from this one.

        Returns:
            A new point containing the subtraction of the two points.
        """
        point = conv_coord(other)
        return Point(self.x - point.x, self.y - point.y)


Coord = Union[Tuple[Number, Number], Point]


def conv_coord(c: Coord) -> Point:
    """Converts a (Number, Number) to the equivalent Point if necessary.

    Args:
         c (Coord): A Point or a (Number, Number).

    Returns:
        The input if it is a Point, otherwise a new Point out of the (Number, Number)'s coordinates.
    """
    if isinstance(c, Point):
        return c
    return Point(c[0], c[1])


class Line:
    """Represents a line segment in 2D space constructed out of two Points.

    Attributes:
        point1 (Point): The first point in the line.
        point2 (Point): The second point in the line.
        points (List[Point]): A list of points in the line.
        slope (Number): The slope of the line segment. Infinity if the line goes straight up/down.
        y_intercept(Optional[Number]): The y-intercept of the line segment if it were extended to cross the y-axis. None if the slope is infinite.
        height (Number): The height of the line (the top - the bottom).
        width (Number): The width of the line (the right - the left).
        x_left (Number): The leftmost x coordinate the line reaches.
        x_right (Number): The rightmost x coordinate the line reaches.
        y_top (Number): The topmost y coordinate the line reaches.
        y_bottom (Number): The bottom-most y coordinate the line reaches.
    """

    def __init__(self, coord1: Coord, coord2: Coord):
        """ Constructs a Line.

        Args:
            coord1 (Coord): A Point or (Number, Number).
            coord2 (Coord): A Point or (Number, Number).
        """

        self.point1 = conv_coord(coord1)
        self.point2 = conv_coord(coord2)
        self.points = [self.point1, self.point2]

        self.slope = float("inf") if self.point1.x == self.point2.x else (self.point2.y - self.point1.y) / (
                self.point2.x - self.point1.x)
        self.y_intercept = self.point1.y - (self.slope * self.point1.x)

        self.height = abs(self.point1.y - self.point2.y)
        self.width = abs(self.point1.x - self.point2.x)

        self.x_left = min(self.point1.x, self.point2.x)
        self.x_right = max(self.point1.x, self.point2.x)
        self.y_top = max(self.point1.y, self.point2.y)
        self.y_bottom = min(self.point1.y, self.point2.y)

        self.__hash = hash(frozenset([self.point1, self.point2]))

    def __contains__(self, coord: Coord):
        """Returns True if a Point is on this line, False if not.

        Args:
            coord (Coord): A Point or a (Number, Number) representing a point in 2D space.

        Returns:
            True if the x and y coordinates of the argument are within 0.0005 of the line, False if not.
        """
        item = conv_coord(coord)
        if not (self.x_left - 0.0005 <= item.x <= self.x_right + 0.0005):
            return False
        if self.slope == float("inf"):
            return self.y_bottom <= item.y <= self.y_top
        diff = abs(self.x_to_y(item.x) - item.y)
        return diff < 0.0005

    def x_to_y(self, x: Number):
        """Plots an x coordinate to a y coordinate on this line (y = mx + b).

        Args:
            x (Number): A number. This does not have to be on the line segment.

        Returns:
            The y coordinate corresponding to the input x coordinate, or NaN if the line's slope is infinite.
        """
        return self.slope * x + self.y_intercept

    def point_of_intersection(self, line: "Line") -> Union[Point, None]:
        """Computes the Point where two lines intersect.
        This will be computed as if the lines extended infinitely.

        Args:
            line (Line): Another line to intersect with this one.

        Returns:
            The Point where the two lines intersect, or None if the lines are parallel.
            The returned Point does not have to be on either of the line segments.
            If not, it will be where the two lines would intersect if the line segments extended infinitely.
        """
        if self.slope == line.slope:
            return None

        if self.slope == float("inf"):
            return Point(self.point1.x, line.x_to_y(self.point1.x))

        if line.slope == float("inf"):
            return Point(line.point1.x, self.x_to_y(line.point1.x))

        x = (self.y_intercept - line.y_intercept) / (line.slope - self.slope)
        return Point(x, self.x_to_y(x))

    def intersects(self, line: "Line") -> bool:
        """Returns True if this line intersects another, False if not.
        The intersection point must lie on the line segments themselves.

        Args:
            line: The line to intersect with this one.

        Returns:
            True if the line segments intersect, False if not.
        """

        # poi = self.point_of_intersection(line)
        # if poi is None:
        #     return False
        # return poi in Rect(self.point1, self.point2) and poi in Rect(line.point1, line.point2)

        # line segment a given by endpoints a1, a2
        # line segment b given by endpoints b1, b2
        # return
        def seg_intersect(a1, a2, b1, b2):
            """
            Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
            a1: [x, y] a point on the first line
            a2: [x, y] another point on the first line
            b1: [x, y] a point on the second line
            b2: [x, y] another point on the second line
            """
            s = np.vstack([a1, a2, b1, b2])  # s for stacked
            h = np.hstack((s, np.ones((4, 1))))  # h for homogeneous
            l1 = np.cross(h[0], h[1])  # get first line
            l2 = np.cross(h[2], h[3])  # get second line
            x, y, z = np.cross(l1, l2)  # point of intersection
            if z == 0:  # lines are parallel
                return float('inf'), float('inf')
            return x / z, y / z

        tmp = seg_intersect(np.array([*self.point1]), np.array([*self.point2]), np.array([*line.point1]),
                            np.array([*line.point2]))
        return (max(self.x_left, line.x_left) - 0.005 <= tmp[0] <= min(self.x_right, line.x_right) + 0.005) and (
                max(self.y_bottom, line.y_bottom) - 0.005 <= tmp[1] <= min(self.y_top, line.y_top) + 0.005)

    def __eq__(self, other):
        """Returns True if this line equals another.
        The ordering of the points does not matter.

        Examples:
            Line((1, 2), (3, 4)) == Line((3, 4), (1, 2)) -> True
            Line((1, 2), (3, 4)) == Line((2, 1), (4, 3)) -> False

        Args:
            other (any): The argument.

        Returns:
            True if the argument is a Line and the points are the same, False if not.

        """

        if not isinstance(other, Line):
            return False
        return frozenset([self.point1, self.point2]) == frozenset([other.point1, other.point2])

    def __hash__(self):
        """Returns a hash of this line.
        The ordering of the points does not matter."""

        return self.__hash

    def length(self) -> Number:
        """Returns the euclidean distance of this Line (distance formula)."""

        return sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)

    def __str__(self) -> str:
        return f"{self.point1} -> {self.point2}"

    def __repr__(self) -> str:
        return f"Line(({self.point1}), ({self.point2}))"


class Rect:
    """Represents a rectangle in 2D space.

    Attributes:
        width (Number): The width of the rectangle.
        height (Number): The height of the rectangle.
        lower_left (Point): The lower left coordinate of the Rect.
        upper_right (Point): The upper right coordinate of the Rect.
        lower_right (Point): The lower right coordinate of the Rect.
        upper_left (Point): The upper left coordinate of the Rect.
        points (List[Point]): A list of points in the Rect.
        lines (List[Line]): A list of lines in the Rect. These will plot a continuous shape when drawn in order.
    """

    def __init__(self, coord1: Coord, coord2: Coord):
        """Constructs the rectangle spanning two coordinates diagonally.

        Args:
            coord1 (Coord): The first coordinate.
            coord2 (Coord): The second coordinate.
        """

        point1, point2 = [conv_coord(c) for c in [coord1, coord2]]
        self.width = abs(point1.x - point2.x)
        self.height = abs(point1.y - point2.y)
        self.lower_left = Point(min(point1.x, point2.x), min(point1.y, point2.y))
        self.upper_right = Point(max(point1.x, point2.x), max(point1.y, point2.y))
        self.lower_right = Point(self.upper_right.x, self.lower_left.y)
        self.upper_left = Point(self.lower_left.x, self.upper_right.y)
        self.points = [self.upper_left, self.upper_right, self.lower_left, self.lower_right]
        self.lines = [
            Line(self.upper_left, self.upper_right),
            Line(self.upper_right, self.lower_right),
            Line(self.lower_right, self.lower_left),
            Line(self.lower_left, self.upper_left)
        ]
        self.__hash = hash((self.lower_left, self.upper_right, "rect"))

    def __contains__(self, coord: Coord) -> bool:
        """Returns True if a coordinate lies inside a Rectangle, False if not.
        The Point can also lie up to 0.0005 outside of the rectangle to account for floating point imprecision.

        Args:
            coord (Coord): A Point or (Number, Number).
        """

        point = conv_coord(coord)
        return self.lower_left.x - 0.0005 <= point.x <= self.upper_right.x + 0.0005 and self.lower_left.y - 0.0005 <= point.y <= self.upper_right.y + 0.0005

    def __eq__(self, o) -> bool:
        """Returns True if another Rect has the same lower-left and upper-right coordinates, False if not.

        Examples:
            Rect((1, 2), (3, 4)) == Rect((1, 4), (3, 2)) -> True
            Rect((1, 2), (3, 4)) == Rect((1, 3), (2, 4)) -> False

        Args:
            o (any): The argument.

        Returns:
            True if the argument is a Rect and has the same lower-left and upper-right coordinates, False if not.
        """

        if not isinstance(o, Rect):
            return False
        return self.lower_left == o.lower_left and self.upper_right == o.upper_right

    def __hash__(self) -> int:
        """Returns a hash of this Rect. Any two Rects with the same lower left and upper right will have the same hash.
        """
        return self.__hash

    def __str__(self) -> str:
        return f"[{self.lower_left}, {self.upper_right}]"

    def __repr__(self) -> str:
        return f"Rect({self.lower_left}, {self.upper_right})"


class Shape:
    """Represents a closed shape in 2D space.

    Attributes:
        points (List[Point]): A list of points making up the Shape.
        lines (List[Line]): A list of lines making up the Shape. This includes the line returning to the first point.
    """

    def __init__(self, *coords: Coord):
        """Constructs a Shape out of several coordinates.
        The shape will be constructed with lines moving from one coordinate to the next in order.
        If the last coordinate is not the same as the first, a line will also be drawn back to the first coordinate.

        Examples:
            Shape((1, 1), (3, 5), (7, -4))
            Shape(*list_of_points)

        Args:
            *coords (Coord): A varargs list of coordinates. There must be at least 3 points.
        """

        self.points = [conv_coord(c) for c in coords]
        self.lines = [Line(p1, p2) for p1, p2 in
                      list(zip(self.points[:-1], self.points[1:]))]
        if self.points[-1] != self.points[0]:
            self.lines += [Line(self.points[-1], self.points[0])]
        else:
            self.points = self.points[:-1]

        if len(self.lines) < 3:
            raise Exception("The shape does not have enough points.")

        self.__hash = hash(tuple(self.points))

    def __eq__(self, other):
        """Returns True if the argument is a Shape with the same points.
        The order of the points matters.

        Examples:
            Shape((1, 1), (3, 3), (7, 0)) == Shape((1, 1), (3, 3), (7, 0), (1, 1)) -> True
            Shape((1, 1), (3, 3), (7, 0)) == Shape((7, 0), (1, 1), (3, 3))         -> False
        """

        if not isinstance(other, Shape):
            return False
        return self.points == other.points

    def __hash__(self):
        """Returns a hash of the Shape.
        This is dependent on the ordering and contents of the points inside."""

        return self.__hash

    def __str__(self) -> str:
        return " -> ".join(str(x) for x in self.points)

    def __repr__(self) -> str:
        return "Shape(" + ", ".join(str(x) for x in self.points) + ")"


class hashabledict(dict):
    def __init__(self, other: Dict = None):
        super().__init__()
        if other is not None:
            for key, value in other.items():
                self[key] = value

    def __key(self):
        return tuple((k,self[k]) for k in sorted(self))
    def __hash__(self):
        return hash(self.__key())
    def __eq__(self, other):
        return self.__key() == other.__key()


class UI:
    """A user interface that displays lines, shapes, and rectangles.
    """

    def __init__(self):
        self.__input_dim = None
        self.__scale = None
        self.__objects = set()

        pygame.init()
        pygame.font.init()
        info = pygame.display.Info()
        screen_x, screen_y = info.current_w, info.current_h
        self.__screen_dim = Rect((0, 0), (int(screen_x * 0.9), int(screen_y * 0.9)))
        self.__screen = pygame.display.set_mode((self.__screen_dim.upper_right.x, self.__screen_dim.upper_right.y), flags=pygame.HWACCEL | pygame.DOUBLEBUF | pygame.OPENGL)

        self.__rendered = False

    def add(self, obj: Union[Line, Shape, Rect], color: Tuple[int, int, int] = (0, 0, 0), width: int = 1):
        tmp = hashabledict({"obj": obj, "color": color, "width": width})
        self.__objects.add(hashabledict({"obj": obj, "color": color, "width": width}))
        if self.__rendered:
            self.__draw(tmp)
            self.update()

    def print(self, text: str, coord: Coord, color: Tuple[int, int, int] = (0, 0, 0), width: int = 1, font: str = "Comic Sans MS"):
        tmp = hashabledict({"obj": text, "coord": conv_coord(coord), "color": color, "width": width, "font": font})
        self.__objects.add(hashabledict({"obj": text, "coord": conv_coord(coord), "color": color, "width": width, "font": font}))
        if self.__rendered:
            self.__draw(tmp)
            self.update()

    def render(self):
        if self.__input_dim is None:
            coords = []
            for obj in self.__objects:
                o = obj["obj"]
                if isinstance(o, str):
                    coords.append(obj["coord"])
                elif isinstance(o, Line):
                    coords.append(o.point1)
                    coords.append(o.point2)
                else:
                    for point in o.points:
                        coords.append(point)
            min_x = min(a.x for a in coords)
            min_y = min(a.y for a in coords)
            max_x = max(a.x for a in coords)
            max_y = max(a.y for a in coords)
            self.__input_dim = Rect((min_x, min_y), (max_x, max_y))

        if self.__scale is None:
            idim = self.__input_dim
            sdim = self.__screen_dim

            sdim = Rect((sdim.width * 0.05, sdim.height * 0.05), (sdim.upper_right.x * 0.95, sdim.upper_right.y * 0.95))

            input_ratio = (idim.upper_right.x - idim.upper_left.x) / (idim.upper_right.y - idim.lower_right.y)
            screen_ratio = (sdim.upper_right.x - sdim.upper_left.x) / (sdim.upper_right.y - sdim.lower_right.y)

            if input_ratio > screen_ratio:
                factor = input_ratio / screen_ratio
                diff_y = idim.height * (factor - 1)
                ll = Point(idim.lower_left.x, idim.lower_left.y - diff_y / 2)
                ur = Point(idim.upper_right.x, idim.upper_right.y + diff_y / 2)
                idim = Rect(ll, ur)
            else:
                factor = screen_ratio / input_ratio
                diff_x = idim.width * (factor - 1)
                ll = Point(idim.lower_left.x - diff_x / 2, idim.lower_left.y)
                ur = Point(idim.upper_right.x + diff_x / 2, idim.upper_right.y)
                idim = Rect(ll, ur)

            idelta = idim.lower_left
            sdelta = sdim.lower_left

            ix, iy = idim.width, idim.height
            sx, sy = sdim.width, sdim.height

            def scale(point: Point):
                point -= idelta
                pt = Point(point.x, idim.height - point.y)
                ret = Point(pt.x / ix * sx, pt.y / iy * sy)
                ret += sdelta
                return int(ret.x), int(ret.y)

            self.__scale = scale

        if not self.__rendered:
            self.__screen = pygame.display.set_mode((self.__screen_dim.upper_right.x, self.__screen_dim.upper_right.y), flags=pygame.HWACCEL | pygame.DOUBLEBUF)

        self.__screen.fill((255, 255, 255))

        for obj in self.__objects:
            self.__draw(obj)

        self.__rendered = True
        self.update()

    def __draw(self, obj: Dict):
        o = obj["obj"]
        if isinstance(o, str):
            font = pygame.font.SysFont(obj["font"], obj["width"])
            surf = font.render(o, True, obj["color"])
            self.__screen.blit(surf, (obj["coord"].x, obj["coord"].y))
        elif isinstance(o, Line):
            pygame.draw.line(self.__screen, obj["color"], self.__scale(o.point1), self.__scale(o.point2), obj["width"])
        elif isinstance(o, Shape):
            pygame.draw.polygon(self.__screen, obj["color"], [self.__scale(x) for x in o.points], obj["width"])
        elif isinstance(o, Rect):
            sr = Rect(self.__scale(o.lower_left), self.__scale(o.upper_right))
            pygame.draw.rect(self.__screen, obj["color"], pygame.rect.Rect(*sr.lower_left, sr.width, sr.height))

    # noinspection PyMethodMayBeStatic
    def done(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            pygame.display.flip()

    def update(self):
        pygame.display.update()
        pygame.display.flip()

    def scale(self):
        return self.__scale
