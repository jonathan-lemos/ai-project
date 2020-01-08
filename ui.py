import turtle
from typing import Tuple, Union

Number = Union[int, float]


class Point:
    def __init__(self, x: Number, y: Number):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

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
        return Rect(self.point1, self.point2).contains(poi) and Rect(line.point1, line.point2).contains(poi)

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

    def contains(self, point: Point) -> bool:
        return self.upper_left.x <= point.x <= self.upper_right.x and self.upper_left.y <= point.y <= self.upper_right.y

    def __str__(self) -> str:
        return f"[{self.upper_left}, {self.upper_right}]"


class Shape:
    def __init__(self, *points: Point):
        self.points = list(points)
        self.lines = [Line(p1, p2) for p1, p2 in
                      list(zip(self.points[:-1], self.points[1:])) + [(self.points[-1], self.points[0])]]

    def __str__(self) -> str:
        return str(self.lines)


class UI:
    def __init__(self, bg_color: str = "white", pad_pct: Number = 0.05, debug: bool = False):
        self.turt = turtle.Turtle()
        self.screen = turtle.Screen()
        self.debug = debug
        self.pad_pct = pad_pct

        self.screen.bgcolor(bg_color)

        if not debug:
            self.turt.speed('fastest')
            self.screen.tracer(0, 0)
        else:
            self.turt.speed('slowest')

        self.objects = []

    def add(self, *objs: Union[Line, Rect, Shape], width: Number = 10, color: str = "black") -> None:
        for obj in objs:
            self.objects.append((obj, width, color))

    def render(self) -> None:
        objs = [obj for obj, width, color in self.objects]
        lines = [y for x in [[obj] if type(obj) == Line else obj.lines for obj in objs] for y in x]
        points = [point for line in lines for point in [line.point1, line.point2]]

        ymin = min(point.y for point in points)
        ymax = max(point.y for point in points)
        xmin = min(point.x for point in points)
        xmax = max(point.x for point in points)

        width = xmax - xmin
        height = ymax - ymin

        screen_ratio = self.screen.window_height() / self.screen.window_width()
        grid_ratio = height / width

        if screen_ratio > grid_ratio:
            height_diff = screen_ratio * width - height

            ymax += height_diff / 2
            ymin -= height_diff / 2
        else:
            width_diff = screen_ratio ** -1 * height - width

            xmax += width_diff / 2
            xmin -= width_diff / 2

        xpad = (xmax - xmin) * self.pad_pct
        ypad = (ymax - ymin) * self.pad_pct

        self.screen.setworldcoordinates(llx=xmin - xpad,
                                        lly=ymin - ypad,
                                        urx=xmax + xpad,
                                        ury=ymax + ypad)

        if not self.debug:
            self.turt.hideturtle()

        for obj in self.objects:
            self.__draw(obj)

        self.screen.update()
        turtle.done()

    def __draw(self, obj: Tuple[Union[Line, Rect, Shape], Number, str]) -> None:
        if isinstance(obj[0], Line):
            self.__draw_line(*obj)
        else:
            for line in obj[0].lines:
                self.__draw_line(line, *obj[1:])

    def __draw_line(self, line: Line, width: Number, color: str) -> None:
        self.turt.pencolor(color)
        self.turt.width(width)

        self.turt.penup()
        self.turt.setpos(line.point1.x, line.point1.y)
        self.turt.pendown()

        self.turt.setpos(line.point2.x, line.point2.y)
