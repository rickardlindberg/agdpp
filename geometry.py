import math

class OutsideScreenSpace:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def hits(self, position, margin):
        """
        >>> inside_x = 50
        >>> inside_y = 50
        >>> space = OutsideScreenSpace(100, 100)

        To the left:

        >>> space.hits(Point(0, inside_y), 10)
        False
        >>> space.hits(Point(-10, inside_y), 10)
        True

        To the right:

        >>> space.hits(Point(100, inside_y), 10)
        False
        >>> space.hits(Point(110, inside_y), 10)
        True

        To the top:

        >>> space.hits(Point(inside_x, 0), 10)
        False
        >>> space.hits(Point(inside_x, -10), 10)
        True

        To the bottom:

        >>> space.hits(Point(inside_x, 100), 10)
        False
        >>> space.hits(Point(inside_x, 110), 10)
        True
        """
        if position.x <= -margin:
            return True
        elif position.x >= self.width+margin:
            return True
        elif position.y <= -margin:
            return True
        elif position.y >= self.height+margin:
            return True
        else:
            return False

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_angle(degrees):
        """
        >>> p = Point.from_angle(-90)
        >>> int(p.x)
        0
        >>> int(p.y)
        -1

        >>> p = Point.from_angle(0)
        >>> int(p.x)
        1
        >>> int(p.y)
        0
        """
        return Point(
            x=math.cos(math.radians(degrees)),
            y=math.sin(math.radians(degrees))
        )

    def distance_to(self, point):
        """
        >>> Point(0, 0).distance_to(Point(10, 0))
        10.0
        """
        return math.sqrt((point.x-self.x)**2+(point.y-self.y)**2)

    def move(self, dx=0, dy=0):
        """
        >>> Point(0, 0).move(10, 10)
        Point(10, 10)
        """
        return Point(x=self.x+dx, y=self.y+dy)

    def add(self, point):
        """
        >>> Point(0, 5).add(Point(1, 1))
        Point(1, 6)
        """
        return self.move(dx=point.x, dy=point.y)

    def times(self, magnification):
        """
        >>> Point(1, 5).times(2)
        Point(2, 10)
        """
        return Point(x=self.x*magnification, y=self.y*magnification)

    def set(self, x=None, y=None):
        """
        >>> Point(0, 0).set(10, 10)
        Point(10, 10)

        >>> Point(5, 5).set()
        Point(5, 5)
        """
        return Point(
            x=self.x if x is None else x,
            y=self.y if y is None else y
        )

    def __repr__(self):
        return f"Point({self.x}, {self.y})"