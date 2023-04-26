import math

class OutsideScreenSpace:

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def hits(self, x, y, margin):
        """
        >>> inside_x = 50
        >>> inside_y = 50
        >>> space = OutsideScreenSpace(100, 100)

        To the left:

        >>> space.hits(0, inside_y, 10)
        False
        >>> space.hits(-10, inside_y, 10)
        True

        To the right:

        >>> space.hits(100, inside_y, 10)
        False
        >>> space.hits(110, inside_y, 10)
        True

        To the top:

        >>> space.hits(inside_x, 0, 10)
        False
        >>> space.hits(inside_x, -10, 10)
        True

        To the bottom:

        >>> space.hits(inside_x, 100, 10)
        False
        >>> space.hits(inside_x, 110, 10)
        True
        """
        if x <= -margin:
            return True
        elif x >= self.width+margin:
            return True
        elif y <= -margin:
            return True
        elif y >= self.height+margin:
            return True
        else:
            return False

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

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
