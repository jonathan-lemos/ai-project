from ui import Shape, Line, Point, UI

ui = UI(bg_color="red", debug=True)
patriotism = [
    Line(Point(5, 0), Point(5, 10)),
    Line(Point(0, 5), Point(10, 5)),
    Line(Point(5, 10), Point(0, 10)),
    Line(Point(0, 5), Point(0, 0)),
    Line(Point(5, 0), Point(10, 0)),
    Line(Point(10, 5), Point(10, 10))
]
ui.add(*patriotism, width=60)
ui.render()
