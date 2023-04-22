from gameloop import GameLoop

class BalloonShooter:

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
    >>> BalloonShooter(loop).run()
    >>> events
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    CLEAR_SCREEN =>
    DRAW_CIRCLE =>
        x: 50
        y: 50
        radius: 40
        color: 'red'
    DRAW_CIRCLE =>
        x: 500
        y: 500
        radius: 10
        color: 'blue'
    DRAW_CIRCLE =>
        x: 500
        y: 520
        radius: 15
        color: 'blue'
    DRAW_CIRCLE =>
        x: 500
        y: 540
        radius: 20
        color: 'blue'
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
        loop.draw_circle(x=500, y=500, color="blue", radius=10)
        loop.draw_circle(x=500, y=520, color="blue", radius=15)
        loop.draw_circle(x=500, y=540, color="blue", radius=20)

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
    BalloonShooter(GameLoop.create()).run()
