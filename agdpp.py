from gameloop import ExitGameLoop
from gameloop import GameLoop
from sprites import SpriteGroup

class BalloonShooter:

    """
    I am a balloon shooter game!

    Initial state
    =============

    We run the game for a few frames, then quit:

    >>> events = BalloonShooter.run_in_test_mode(
    ...     events=[
    ...         [],
    ...         [],
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )

    The game loop is initialized and cleaned up:

    >>> events.filter("GAMELOOP_INIT", "GAMELOOP_QUIT")
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    GAMELOOP_QUIT =>

    The balloon is drawn animated:

    >>> events.filter("DRAW_CIRCLE", radius=40).collect("x", "y")
    [(50, 50), (51, 50), (52, 50)]

    The arrow is drawn in a fixed position:

    >>> set(events.filter("DRAW_CIRCLE", radius=10).collect("x", "y"))
    {(500, 500)}
    >>> set(events.filter("DRAW_CIRCLE", radius=15).collect("x", "y"))
    {(500, 520)}
    >>> set(events.filter("DRAW_CIRCLE", radius=20).collect("x", "y"))
    {(500, 540)}

    User presses space key
    ======================

    We run the game for a few frames, press the space key, let it run for a few
    frames, then quit:

    >>> events = BalloonShooter.run_in_test_mode(
    ...     events=[
    ...         [],
    ...         [],
    ...         [GameLoop.create_event_keydown_space()],
    ...         [],
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )

    The arrow moves:

    >>> arrow_head_positions = events.filter("DRAW_CIRCLE", radius=10).collect("x", "y")
    >>> len(arrow_head_positions) > 1
    True
    >>> len(set(arrow_head_positions)) > 1
    True

    Creation
    ========

    The real BalloonShooter is not created anywhere but when we run the game.
    This test serves to prove that it at least can be instantiated without
    errors.

    >>> isinstance(BalloonShooter.create(), BalloonShooter)
    True
    """

    @staticmethod
    def create():
        return BalloonShooter(GameLoop.create())

    @staticmethod
    def run_in_test_mode(events=[]):
        loop = GameLoop.create_null(
            events=events+[
                [GameLoop.create_event_user_closed_window()],
            ]
        )
        events = loop.track_events()
        BalloonShooter(loop).run()
        return events

    def __init__(self, loop):
        self.loop = loop
        self.game_scene = GameScene()

    def run(self):
        self.loop.run(self)

    def tick(self, dt, events):
        for event in events:
            self.game_scene.event(event)
        self.game_scene.update(dt)
        self.loop.clear_screen()
        self.game_scene.draw(self.loop)

class GameScene(SpriteGroup):

    def __init__(self):
        SpriteGroup.__init__(self)
        self.balloon = self.add(Balloon())
        self.arrow = self.add(Arrow())

    def event(self, event):
        if event.is_user_closed_window():
            raise ExitGameLoop()
        elif event.is_keydown_space():
            self.arrow.shoot()

class Arrow:

    def __init__(self):
        self.y = 500
        self.shooting = False

    def shoot(self):
        self.shooting = True

    def update(self, dt):
        if self.shooting:
            self.y -= dt

    def draw(self, loop):
        loop.draw_circle(x=500, y=self.y, color="blue", radius=10)
        loop.draw_circle(x=500, y=self.y+20, color="blue", radius=15)
        loop.draw_circle(x=500, y=self.y+40, color="blue", radius=20)

class Balloon:

    def __init__(self):
        self.x = 50

    def update(self, dt):
        if self.x > 500:
            self.x = 50
        else:
            self.x += dt

    def draw(self, loop):
        loop.draw_circle(self.x)

if __name__ == "__main__":
    BalloonShooter.create().run()
