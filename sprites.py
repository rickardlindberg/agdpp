class SpriteGroup:

    """
    >>> class TestSprite:
    ...     def tick(self, dt):
    ...         print(f"TEST SPRITE tick {dt}")
    ...     def draw(self, loop):
    ...         print(f"TEST SPRITE draw {loop}")

    >>> group = SpriteGroup([TestSprite()])
    >>> group.add(TestSprite())

    >>> group.tick(4)
    TEST SPRITE tick 4
    TEST SPRITE tick 4

    >>> group.draw(None)
    TEST SPRITE draw None
    TEST SPRITE draw None
    """

    def __init__(self, sprites=[]):
        self.sprites = []
        for sprite in sprites:
            self.add(sprite)

    def add(self, sprite):
        self.sprites.append(sprite)

    def tick(self, *args, **kwargs):
        for sprite in self.sprites:
            sprite.tick(*args, **kwargs)

    def draw(self, *args, **kwargs):
        for sprite in self.sprites:
            sprite.draw(*args, **kwargs)
