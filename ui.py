import turtle
from typing import Iterable, Tuple, Union
from math import sqrt

Number = Union[int, float]


class Point:
    def __init__(self, x: Number, y: Number):
        self.x = x
        self.y = y
        self.__hash = hash((self.x, self.y))

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __getitem__(self, index: int):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise Exception(f"Points only have X (0) and Y (1) coordinates. You tried to index it with {index}.")

    def __hash__(self):
        return self.__hash

    def __str__(self):
        return f"({self.x}, {self.y})"


Coord = Union[Tuple[int, int], Point]


def conv_coord(c: Coord) -> Point:
    if isinstance(c, Point):
        return c
    return Point(c[0], c[1])


class Line:
    def __init__(self, coord1: Coord, coord2: Coord):
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
        item = conv_coord(coord)
        if not (self.x_left <= item.x <= self.x_right):
            return False
        if self.slope == float("inf"):
            return self.y_bottom <= item.y <= self.y_top
        diff = abs(self.x_to_y(item.x) - item.y)
        return diff < 0.0005

    def x_to_y(self, x: Number):
        return self.slope * x + self.y_intercept

    def point_of_intersection(self, line: "Line") -> Union[Point, None]:
        if self.slope == line.slope:
            return None

        x = (self.y_intercept - line.y_intercept) / (self.slope - line.slope)
        return Point(x, self.x_to_y(x))

    def intersects(self, line: "Line") -> bool:
        poi = self.point_of_intersection(line)
        if poi is None:
            return False
        return poi in Rect(self.point1, self.point2) and poi in Rect(line.point1, line.point2)

    def __eq__(self, other):
        if not isinstance(other, Line):
            return False
        return frozenset([self.point1, self.point2]) == frozenset([other.point1, other.point2])

    def __hash__(self):
        return self.__hash

    def __len__(self):
        return sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)

    def __str__(self) -> str:
        return f"{self.point1} -> {self.point2}"


class Rect:
    def __init__(self, coord1: Coord, coord2: Coord):
        point1, point2 = [conv_coord(c) for c in [coord1, coord2]]
        self.width = abs(point1.x - point2.x)
        self.height = abs(point1.y - point2.y)
        self.upper_left = Point(min(point1.x, point2.x), min(point1.y, point2.y))
        self.lower_right = Point(max(point1.x, point2.x), max(point1.y, point2.y))
        self.upper_right = Point(self.lower_right.x, self.upper_left.y)
        self.lower_left = Point(self.upper_left.x, self.lower_right.y)
        self.points = [self.upper_left, self.upper_right, self.lower_left, self.lower_right]
        self.lines = [
            Line(self.upper_left, self.upper_right),
            Line(self.upper_right, self.lower_right),
            Line(self.lower_right, self.lower_left),
            Line(self.lower_left, self.upper_left)
        ]
        self.__hash = hash((self.lower_left, self.upper_right))

    def __contains__(self, coord: Coord) -> bool:
        point = conv_coord(coord)
        return self.upper_left.x <= point.x <= self.upper_right.x and self.upper_left.y <= point.y <= self.upper_right.y

    def __eq__(self, o):
        if not isinstance(o, Rect):
            return False
        return self.lower_left == o.lower_left and self.upper_right == o.upper_right

    def __hash__(self):
        return self.__hash

    def __str__(self) -> str:
        return f"[{self.upper_left}, {self.upper_right}]"


class Shape:
    def __init__(self, *coords: Coord):
        self.points = [conv_coord(c) for c in coords]
        self.lines = [Line(p1, p2) for p1, p2 in
                      list(zip(self.points[:-1], self.points[1:]))]
        if self.points[-1] != self.points[0]:
            self.lines += [Line(self.points[-1], self.points[0])]
        self.__hash = hash(tuple(self.points))

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return False
        return self.points == other.points

    def __hash__(self):
        return self.__hash

    def __str__(self) -> str:
        return " -> ".join(str(x) for x in self.points)


class UI:
    def __init__(self, screen_dim: Union[Rect, None], bg_color: str = "white", pad_pct: Number = 0.05,
                 debug: bool = False):
        self.__bg_color = bg_color
        self.__debug = debug
        self.__pad_pct = pad_pct
        self.objects = set()
        self.__turt = None
        self.__screen = None
        self.__screen_dim = screen_dim
        self.__rendered = False

    def add(self, *objs: Union[Line, Rect, Shape], width: Number = 10, color: str = "black") -> None:
        for obj in objs:
            self.objects.add((obj, width, color))
            if self.__rendered:
                self.__draw((obj, width, color))

    def done(self) -> None:
        turtle.done()

    def remove(self, *objs: Union[Line, Rect, Shape], width: Number = 10, color: str = "black") -> None:
        for obj in objs:
            self.objects.remove((obj, width, color))
            if self.__rendered:
                self.__draw((obj, width, self.__bg_color))

    def render(self) -> None:
        self.__rendered = True

        self.__turt = turtle.Turtle()
        self.__screen = turtle.Screen()

        self.__screen.bgcolor(self.__bg_color)

        if not self.__debug:
            self.__turt.speed('fastest')
            self.__screen.tracer(0, 0)
        else:
            self.__turt.speed('slowest')

        if self.__screen_dim:
            ymin = self.__screen_dim.lower_left.y
            ymax = self.__screen_dim.upper_right.y
            xmin = self.__screen_dim.lower_left.x
            xmax = self.__screen_dim.upper_right.x
        else:
            # get the maximum/minimum x, y to calculate the new coordinate system's bounds
            objs = [obj for obj, width, color in self.objects]
            lines = [y for x in [[obj] if type(obj) == Line else obj.lines for obj in objs] for y in x]
            points = [point for line in lines for point in [line.point1, line.point2]]

            ymin = min(point.y for point in points)
            ymax = max(point.y for point in points)
            xmin = min(point.x for point in points)
            xmax = max(point.x for point in points)

        # we need to adjust the coordinate system so objects look proportional and take up most of the window size

        width = xmax - xmin
        height = ymax - ymin

        # get the h/w ratios for the screen and our grid space
        screen_ratio = self.__screen.window_height() / self.__screen.window_width()
        grid_ratio = height / width

        # give extra space on one of the axes to make the adjusted coordinates proportional to the window size
        if screen_ratio > grid_ratio:
            height_diff = screen_ratio * width - height

            ymax += height_diff / 2
            ymin -= height_diff / 2
        else:
            width_diff = screen_ratio ** -1 * height - width

            xmax += width_diff / 2
            xmin -= width_diff / 2

        # add a slight bit of padding so objects don't render right on the edge
        xpad = (xmax - xmin) * self.__pad_pct
        ypad = (ymax - ymin) * self.__pad_pct

        self.__screen.setworldcoordinates(llx=xmin - xpad,
                                          lly=ymin - ypad,
                                          urx=xmax + xpad,
                                          ury=ymax + ypad)

        if not self.__debug:
            self.__turt.hideturtle()

        for obj in self.objects:
            self.__draw(obj)

        self.__screen.update()

    def points(self) -> Iterable[Point]:
        return (x.points for x in [x[0] for x in self.objects])

    def lines(self) -> Iterable[Line]:
        for obj in (x[0] for x in self.objects):
            if isinstance(obj, Line):
                yield obj
            else:
                for line in obj.lines:
                    yield line

    def __draw(self, obj: Tuple[Union[Line, Rect, Shape], Number, str]) -> None:
        if isinstance(obj[0], Line):
            self.__draw_line(*obj)
        else:
            for line in obj[0].lines:
                self.__draw_line(line, *obj[1:])
        if self.__rendered:
            self.__screen.update()

    def __draw_line(self, line: Line, width: Number, color: str) -> None:
        self.__turt.pencolor(color)
        self.__turt.width(width)

        self.__turt.penup()
        self.__turt.setpos(line.point1.x, line.point1.y)
        self.__turt.pendown()

        self.__turt.setpos(line.point2.x, line.point2.y)
