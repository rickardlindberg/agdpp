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

    The arrow moves when it is shot by pressing the space key:

    >>> loop = GameLoop.create_null(
    ...     events=[
    ...         [],
    ...         [GameLoop.create_event_keydown_space()],
    ...         [],
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )
    >>> events = loop.track_events()
    >>> BalloonShooter(loop).run()
    >>> arrow_positions = events.filter("DRAW_CIRCLE", radius=10).collect("x", "y")
    >>> len(arrow_positions) > 1
    True
    >>> len(set(arrow_positions)) > 1
    True

    I can instantiate myself:

    >>> isinstance(BalloonShooter.create(), BalloonShooter)
    True
    """

    @staticmethod
    def create():
        return BalloonShooter(GameLoop.create())

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
            elif event.is_keydown_space():
                self.arrow.shoot()
        for sprite in self.sprites:
            sprite.tick(dt)
        self.loop.clear_screen()
        for sprite in self.sprites:
            sprite.draw(self.loop)

class Arrow:

    """
    I stay still if I've not been fired:

    >>> arrow = Arrow()
    >>> initial_y = arrow.y
    >>> arrow.tick(1)
    >>> arrow.tick(1)
    >>> arrow.tick(1)
    >>> initial_y == arrow.y
    True

    I move upwards when fired:

    >>> arrow = Arrow()
    >>> initial_y = arrow.y
    >>> arrow.shoot()
    >>> arrow.tick(1)
    >>> arrow.tick(1)
    >>> arrow.tick(1)
    >>> arrow.y < initial_y
    True
    """

    def __init__(self):
        self.y = 500
        self.shooting = False

    def shoot(self):
        self.shooting = True

    def tick(self, dt):
        if self.shooting:
            self.y -= dt

    def draw(self, loop):
        loop.draw_circle(x=500, y=self.y, color="blue", radius=10)
        loop.draw_circle(x=500, y=self.y+20, color="blue", radius=15)
        loop.draw_circle(x=500, y=self.y+40, color="blue", radius=20)

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
    BalloonShooter.create().run()
