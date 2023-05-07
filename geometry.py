from collections import namedtuple
import math
import random

class Rectangle(namedtuple("Rectangle", "topleft,bottomright")):

    @staticmethod
    def from_size(width, height):
        """
        >>> Rectangle.from_size(100, 200)
        Rectangle(topleft=Point(x=0, y=0), bottomright=Point(x=100, y=200))
        """
        return Rectangle(
            topleft=Point(x=0, y=0),
            bottomright=Point(x=width, y=height)
        )

    def get_random_x(self):
        return random.randint(self.topleft.x, self.bottomright.x)

    def deflate(self, amount):
        """
        >>> Rectangle.from_size(10, 10).deflate(1)
        Rectangle(topleft=Point(x=1, y=1), bottomright=Point(x=9, y=9))
        """
        return self.inflate(-amount)

    def inflate(self, amount):
        """
        >>> Rectangle.from_size(10, 10).inflate(1)
        Rectangle(topleft=Point(x=-1, y=-1), bottomright=Point(x=11, y=11))
        """
        return Rectangle(
            topleft=self.topleft.move(-amount, -amount),
            bottomright=self.bottomright.move(amount, amount),
        )

    def contains(self, point):
        """
        >>> r = Rectangle.from_size(200, 100)

        Inside top left:

        >>> r.contains(Point(x=0, y=0))
        True

        Inside bottom right:

        >>> r.contains(Point(x=200, y=100))
        True

        Outside left:

        >>> r.contains(Point(x=-1, y=0))
        False

        Outside Right:

        >>> r.contains(Point(x=201, y=0))
        False

        Outside top:

        >>> r.contains(Point(x=0, y=-1))
        False

        Outside bottom:

        >>> r.contains(Point(x=0, y=101))
        False
        """
        if point.x < self.topleft.x:
            return False
        elif point.x > self.bottomright.x:
            return False
        elif point.y < self.topleft.y:
            return False
        elif point.y > self.bottomright.y:
            return False
        else:
            return True

class Point(namedtuple("Point", "x,y")):

    def distance_to(self, point):
        """
        >>> Point(0, 0).distance_to(Point(10, 0))
        10.0
        """
        return math.sqrt((point.x-self.x)**2+(point.y-self.y)**2)

    def move(self, dx=0, dy=0):
        """
        >>> Point(0, 0).move(10, 10)
        Point(x=10, y=10)
        """
        return Point(x=self.x+dx, y=self.y+dy)

    def add(self, point):
        """
        >>> Point(0, 5).add(Point(1, 1))
        Point(x=1, y=6)
        """
        return self.move(dx=point.x, dy=point.y)

    def times(self, magnification):
        """
        >>> Point(1, 5).times(2)
        Point(x=2, y=10)
        """
        return Point(x=self.x*magnification, y=self.y*magnification)

    def set(self, x=None, y=None):
        """
        >>> Point(0, 0).set(10, 10)
        Point(x=10, y=10)

        >>> Point(5, 5).set()
        Point(x=5, y=5)
        """
        return Point(
            x=self.x if x is None else x,
            y=self.y if y is None else y
        )

    def to_angle(self):
        """
        >>> Point(0, -1).to_angle()
        Angle(degrees=-90.0)

        >>> Point(1, 0).to_angle()
        Angle(degrees=0.0)
        """
        return Angle(math.degrees(math.atan2(self.y, self.x)))

class Angle(namedtuple("Angle", "degrees")):

    @staticmethod
    def up():
        return Angle(-90)

    @staticmethod
    def zero():
        return Angle(0)

    @staticmethod
    def fraction_of_whole(fraction):
        return Angle(360 * fraction)

    def to_unit_point(self):
        """
        >>> Angle.up().to_unit_point()
        Point(x=6.123233995736766e-17, y=-1.0)
        """
        return Point(
            x=math.cos(math.radians(self.degrees)),
            y=math.sin(math.radians(self.degrees))
        )

    def add(self, other):
        return Angle(self.degrees + other.degrees)
