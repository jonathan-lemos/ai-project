import turtle
from typing import Iterable, List, Optional, Tuple, Union
from math import sqrt

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

        poi = self.point_of_intersection(line)
        if poi is None:
            return False
        return poi in Rect(self.point1, self.point2) and poi in Rect(line.point1, line.point2)

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

    def __len__(self) -> Number:
        """Returns the euclidean distance of this Line (distance formula)."""

        return sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)

    def __str__(self) -> str:
        return f"{self.point1} -> {self.point2}"


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
        return f"[{self.upper_left}, {self.upper_right}]"


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


class UI:
    """A user interface that displays lines, shapes, and rectangles.
    """

    def __init__(self, screen_dim: Optional[Rect], bg_color: str = "white", pad_pct: Number = 0.05,
                 debug: bool = False):
        """Constructs a UI

        Args:
            screen_dim (Optional[Rect]): The dimensions of the coordinate system, or None to automatically determine this.
                                         For example, Rect((0, 0), (40, 40)) would display objects from (0, 0) to (40, 40).
                                         The actual rendered dimensions may be increased on one axis to prevent objects from being skewed.
                                         These can be changed using the dimensions() function.

            bg_color: The background color as a string. This is "white" by default.

            pad_pct: A percentage of the screen dimensions to use as padding.
                     By default this is 0.05, meaning 5% padding.

            debug: If this is True, objects will be drawn slowly and the cursor will be visible as the lines are drawn.
                   This is False by default.
        """

        self.__bg_color = bg_color
        self.__debug = debug
        self.__pad_pct = pad_pct
        self.__objects = {}

        self.__turt = turtle.Turtle()
        self.__screen = turtle.Screen()

        self.__screen.bgcolor(self.__bg_color)

        if not self.__debug:
            self.__turt.speed('fastest')
            self.__screen.tracer(0, 0)
        else:
            self.__turt.speed('slowest')

        self.__screen_dim = screen_dim
        self.__rendered = False

    def add(self,
            *objs: Union[str, Line, Rect, Shape, Iterable[Union[str, Line, Rect, Shape]]],
            width: Number = 10,
            color: str = "black",
            fillcolor: Optional[str] = None,
            coord: Optional[Coord] = (0, 0),
            align: str = "center",
            font_face: str = "Comic Sans MS",
            font_size: int = 10,
            font_type: str = "normal",
            font_color: str = "black") -> None:

        """Adds several lines, rectangles, or shapes to the UI.
        These are all drawn in one step unless debug mode is enabled (see constructor).
        If the UI has been rendered, these are displayed once this function returns (see render())

        Examples:
            ui.add(Line((1, 1), (2, 2)), Shape((3, 4), (8, -1), (-2, 2)),
            ui.add(*list_of_lines, width=40, color="red")

        Args:
            *objs (Union[Line, Rect, Shape, str]):
            A varargs sequence of zero or more lines, rectangles, shapes, and/or text to add to the UI.
            These can also be iterables of the above.


            width (Number): The width of the lines. By default this is 10. I'm not entirely sure what the unit is. This argument is not used for text.

            color (str): The color of the lines. By default this is "black". This argument is not used for text.

            fillcolor (Optional[str]): The optional fill color of the rectangles and shapes. By default this is None. This argument is only used for Rect and Shape.

            coord (Optional[Coord]): A Point or (Number, Number) to render text at. This argument is only used for text, and MUST BE GIVEN for text.

            align: (str): "left"   - Put the coord on the left edge of the text.
                          "center" - Put the coord in the middle of the text.
                          "right"  - Put the coord on the right edge of the text.
                          This argument is only used for text.

            font_face (str): The font to use. By default this is "Comic Sans MS". This argument is only used for text.

            font_size (int): The font size to use in pt. By default this is 10. This argument is only used for text.

            font_type (str): Used to denote "bold" or "italic" text. By default this is "normal". This argument is only used for text.

            font_color (str): The color of the text. By default this is "black". This argument is only used for text.
        """

        def do_add(ob):
            if isinstance(ob, str):
                if coord is None:
                    raise Exception(f"Text argument '{ob}' given to add() without corresponding coord argument.")
                tup = (ob, coord, align, font_face, font_size, font_type, font_color)
            elif isinstance(ob, Line):
                tup = (ob, width, color)
            else:
                tup = (ob, width, color, fillcolor)

            self.__objects[tup] = None
            if self.__rendered:
                self.__objects[tup] = self.__draw(tup)

        for obj in objs:
            try:
                if isinstance(obj, str):
                    raise TypeError
                tmp = iter(obj)
            except TypeError:
                do_add(obj)
                continue
            for o in tmp:
                do_add(o)

        if self.__rendered:
            self.__screen.update()

    # noinspection PyMethodMayBeStatic
    def done(self) -> None:
        """Must be the last call in any program using UI.
        This is a limitation of turtle.
        """
        turtle.done()

    def remove(self, *objs: Union[Line, Rect, Shape], width: Number = 10, color: str = "black",
               fillcolor: Optional[str] = None) -> bool:
        """Removes zero or more objects added through add()
        Text cannot be removed.

        Args:
            *objs (Union[Line, Rect, Shape]): The objects to remove.

            width (Number): The width of the objects.
                            This must be the same as the objects that were added.
                            This has the same default as add().

            color (str): The color of the objects.
                         This must be the same as the objects that were added.
                         This has the same default as add().

            fillcolor (Optional[str]): The fill color of the objects.
                                       This must be the same as the objects that were added.
                                       This has the same default as add().

        Returns:
            True if the objects were removed. False if at least one object was not previously added.
           """

        ret = True
        if self.__rendered:
            self.screen().update()
        for obj in objs:
            tup = (obj, width, color, fillcolor)
            if tup in self.__objects:
                if self.__rendered:
                    for identifier in self.__objects[tup]:
                        self.__screen.getcanvas().delete(identifier)
                        if identifier in self.__turt.items:
                            self.__turt.items.remove(identifier)
                self.__objects.pop((obj, width, color, fillcolor))
            else:
                ret = False
        if self.__rendered:
            self.__screen.update()
        return ret

    def render(self) -> None:
        """Displays the UI's window and all objects within.
        If the dimensions are not set, this method will automatically detemine them."""

        self.__rendered = True
        self.__turt.clear()

        if self.__screen_dim:
            ymin = self.__screen_dim.lower_left.y
            ymax = self.__screen_dim.upper_right.y
            xmin = self.__screen_dim.lower_left.x
            xmax = self.__screen_dim.upper_right.x
        else:
            # get the maximum/minimum x, y to calculate the new coordinate system's bounds
            objs = [obj for obj, width, color in self.__objects]
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

        self.__screen_dim = Rect((xmin, ymin), (xmax, ymax))

        self.__screen.setworldcoordinates(llx=xmin - xpad,
                                          lly=ymin - ypad,
                                          urx=xmax + xpad,
                                          ury=ymax + ypad)

        if not self.__debug:
            self.__turt.hideturtle()

        for obj in self.__objects:
            self.__objects[obj] = self.__draw(obj)

        self.__screen.update()

    def points(self) -> Iterable[Point]:
        """Returns an iterable of points in the UI."""

        return (x.points for x in [x[0] for x in self.__objects])

    def lines(self) -> Iterable[Line]:
        """Returns an iterable of lines in the UI."""

        for obj in (x[0] for x in self.__objects):
            if isinstance(obj, Line):
                yield obj
            else:
                for line in obj.lines:
                    yield line

    def dimensions(self, new_dim: Optional[Rect] = None) -> Optional[Rect]:
        """If no argument is given, returns the dimensions of the UI if they exist.
        Otherwise, sets the dimensions according to the argument.
        The actual rendered dimensions might be extended on one axis to prevent rendered objects from being skewed."""

        if new_dim is None:
            return self.__screen_dim
        self.__screen_dim = new_dim
        if self.__rendered:
            self.render()

    def rendered(self) -> bool:
        """Returns True if render() was called, False if not."""
        return self.__rendered

    def __draw(self, obj: Tuple) -> List[int]:
        if isinstance(obj[0], Line):
            return self.__draw_line(*obj)
        elif isinstance(obj[0], str):
            self.__draw_text(*obj)
            return [0]
        else:
            return self.__draw_shape(obj[0].lines, *obj[1:])

    def __draw_shape(self, lines: Iterable[Line], width: Number, color: str, fillcolor: Optional[str]) -> List[int]:
        lin = list(lines)

        if len(lin) == 0:
            return []

        self.__turt.pencolor(color)
        self.__turt.width(width)

        self.__turt.penup()
        self.__turt.setpos(lin[0].point1.x, lin[0].point1.y)

        if fillcolor:
            self.__turt.fillcolor(fillcolor)
            self.__turt.begin_fill()
            res = [[self.__undo_buf()[-1][1]]]
        else:
            res = []

        res += [self.__draw_line(line, width, color) for line in lin]

        if fillcolor:
            self.__turt.end_fill()

        return [y for x in res for y in x]

    def __draw_line(self, line: Line, width: Number, color: str) -> List[int]:
        self.__turt.pencolor(color)
        self.__turt.width(width)

        self.__turt.penup()
        self.__turt.setpos(line.point1.x, line.point1.y)
        self.__turt.pendown()

        self.__turt.setpos(line.point2.x, line.point2.y)

        # this horseshit gets the correct item id from the undo buffer since sometimes it doesn't show up in turt.items
        return [self.__undo_buf()[-1][4][0]]

    def __draw_text(self, text: str, coord: Coord, align: str = "center", font_face: str = "Comic Sans MS",
                    font_size: int = 10, font_type: str = "normal", font_color: str = "black") -> List[int]:
        """Prints text on the UI.

        Args:
            coord (Coord): The Point/(Number, Number) to put the text on.
            text (str): The text to print.
            align: (str): "left"   - Put the coord on the left edge of the text.
                          "center" - Put the coord in the middle of the text.
                          "right"  - Put the coord on the right edge of the text.
            font_face (str): The font to use. By default this is "Comic Sans MS".
            font_size (int): The font size to use in pt. By default this is 10.
            font_type (str): Used to denote "bold" or "italic" text. By default this is "normal".
            font_color (str): The color of the text. By default this is "black".
        """

        self.__turt.penup()
        self.__turt.setpos(*coord)
        self.__turt.color(font_color)
        self.__turt.write(text, align=align, font=(font_face, font_size, font_type))

        return [self.__undo_buf()[-1][1][1]]

    def __undo_buf(self) -> List:
        return list(filter(lambda x: x != [None], self.__turt.undobuffer.buffer))

    def turt(self):
        return self.__turt

    def screen(self):
        return self.__screen
