class SpriteGroup:

    """
    >>> class TestSprite:
    ...     def update(self, dt):
    ...         print(f"TEST SPRITE update {dt}")
    ...     def draw(self, loop):
    ...         print(f"TEST SPRITE draw {loop}")

    >>> group = SpriteGroup([TestSprite()])
    >>> x = TestSprite()
    >>> y = group.add(x)
    >>> x is y
    True

    >>> group.update(4)
    TEST SPRITE update 4
    TEST SPRITE update 4

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
        return sprite

    def update(self, *args, **kwargs):
        for sprite in self.sprites:
            sprite.update(*args, **kwargs)

    def draw(self, *args, **kwargs):
        for sprite in self.sprites:
            sprite.draw(*args, **kwargs)

    def get_sprites(self):
        return self.sprites
