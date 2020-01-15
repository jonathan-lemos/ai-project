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

    def __hash__(self):
        return self.__hash

    def __str__(self):
        return f"({self.x}, {self.y})"


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2
        self.points = [self.point1, self.point2]

        self.slope = float("inf") if point1.x == point2.x else (point2.y - point1.y) / (point2.x - point1.x)
        self.y_intercept = point1.y - (self.slope * point1.x)

        self.height = abs(point1.y - point2.y)
        self.width = abs(point1.x - point2.x)

        self.x_left = min(point1.x, point2.x)
        self.x_right = max(point1.x, point2.x)
        self.y_top = max(point1.y, point2.y)
        self.y_bottom = min(point1.y, point2.y)

        self.__hash = hash(frozenset([self.point1, self.point2]))

    def __contains__(self, item: Point):
        if not (self.x_left <= item.x <= self.x_right):
            return False
        if self.slope == float("inf"):
            return self.y_bottom <= item.y <= self.y_top
        diff = abs(self.x_to_y(item.x) - item.y)
        return diff < 0.0005

    def x_to_y(self, x):
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
    def __init__(self, point1: Point, point2: Point):
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

    def __contains__(self, point: Point) -> bool:
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
    def __init__(self, *points: Point):
        self.points = list(points)
        self.lines = [Line(p1, p2) for p1, p2 in
                      list(zip(self.points[:-1], self.points[1:]))]
        if self.points[-1] != self.points[0]:
            self.lines += [(self.points[-1], self.points[0])]
        self.__hash = hash(tuple(self.points))

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return False
        return self.points == other.points

    def __hash__(self):
        return self.__hash

    def __str__(self) -> str:
        return str(self.lines)


class UI:
    def __init__(self, bg_color: str = "white", pad_pct: Number = 0.05, debug: bool = False):
        self.__bg_color = bg_color
        self.__debug = debug
        self.__pad_pct = pad_pct
        self.objects = []

    def add(self, *objs: Union[Line, Rect, Shape], width: Number = 10, color: str = "black") -> None:
        for obj in objs:
            self.objects.append((obj, width, color))

    def render(self) -> None:
        turt = turtle.Turtle()
        screen = turtle.Screen()

        screen.bgcolor(self.__bg_color)

        if not self.__debug:
            turt.speed('fastest')
            screen.tracer(0, 0)
        else:
            turt.speed('slowest')

        objs = [obj for obj, width, color in self.objects]
        lines = [y for x in [[obj] if type(obj) == Line else obj.lines for obj in objs] for y in x]
        points = [point for line in lines for point in [line.point1, line.point2]]

        ymin = min(point.y for point in points)
        ymax = max(point.y for point in points)
        xmin = min(point.x for point in points)
        xmax = max(point.x for point in points)

        width = xmax - xmin
        height = ymax - ymin

        screen_ratio = screen.window_height() / screen.window_width()
        grid_ratio = height / width

        if screen_ratio > grid_ratio:
            height_diff = screen_ratio * width - height

            ymax += height_diff / 2
            ymin -= height_diff / 2
        else:
            width_diff = screen_ratio ** -1 * height - width

            xmax += width_diff / 2
            xmin -= width_diff / 2

        xpad = (xmax - xmin) * self.__pad_pct
        ypad = (ymax - ymin) * self.__pad_pct

        screen.setworldcoordinates(llx=xmin - xpad,
                                   lly=ymin - ypad,
                                   urx=xmax + xpad,
                                   ury=ymax + ypad)

        if not self.__debug:
            turt.hideturtle()

        for obj in self.objects:
            self.__draw(turt, obj)

        screen.update()
        turtle.done()

    def points(self) -> Iterable[Point]:
        return (x.points for x in [x[0] for x in self.objects])

    def lines(self) -> Iterable[Line]:
        for obj in (x[0] for x in self.objects):
            if isinstance(obj, Line):
                yield obj
            else:
                for line in obj.lines:
                    yield line

    def __draw(self, turt: turtle.Turtle, obj: Tuple[Union[Line, Rect, Shape], Number, str]) -> None:
        if isinstance(obj[0], Line):
            self.__draw_line(turt, *obj)
        else:
            for line in obj[0].lines:
                self.__draw_line(turt, line, *obj[1:])

    def __draw_line(self, turt: turtle.Turtle, line: Line, width: Number, color: str) -> None:
        turt.pencolor(color)
        turt.width(width)

        turt.penup()
        turt.setpos(line.point1.x, line.point1.y)
        turt.pendown()

        turt.setpos(line.point2.x, line.point2.y)
