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
