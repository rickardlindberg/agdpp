from gameloop import GameLoop

class Game:

    """
    I draw the initial scene of the game which consists of a balloon and an
    arrow and quit when the user closes the window.

    >>> loop = GameLoop.create_null(
    ...     events=[
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )
    >>> events = loop.track_events()
    >>> Game(loop).run()
    >>> events
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    CLEAR_SCREEN =>
    DRAW_CIRCLE =>
        x: 50
    DRAW_CIRCLE =>
        x: 10
    GAMELOOP_QUIT =>
    """

    def __init__(self, loop):
        self.loop = loop
        self.balloon = Balloon()
        self.arrow = Arrow()
        self.sprites = [self.balloon, self.arrow]

    def run(self):
        self.loop.run(self)

    def tick(self, dt, events):
        for event in events:
            if event.is_user_closed_window():
                self.loop.quit()
        for sprite in self.sprites:
            sprite.tick(dt)
        self.loop.clear_screen()
        for sprite in self.sprites:
            sprite.draw(self.loop)

class Arrow:

    def tick(self, dt):
        pass

    def draw(self, loop):
        loop.draw_circle(10)

class Balloon:

    def __init__(self):
        self.x = 50

    def tick(self, dt):
        if self.x > 500:
            self.x = 50
        else:
            self.x += dt

    def draw(self, loop):
        loop.draw_circle(self.x)

if __name__ == "__main__":
    Game(GameLoop.create()).run()
