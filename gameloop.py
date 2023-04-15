from events import Observable

import pygame

class GameLoop(Observable):

    """
    I init and clean up pygame:

    >>> loop = GameLoop.create_null()
    >>> events = loop.track_events()
    >>> loop.run(TestGameThatNotifiesAndExitsImmediately())
    >>> events
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    GAMELOOP_QUIT =>

    I do the same thing when run for real:

    >>> loop = GameLoop.create()
    >>> events = loop.track_events()
    >>> loop.run(TestGameThatNotifiesAndExitsImmediately())
    >>> events
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    GAMELOOP_QUIT =>

    I pass simulated events to the game tick method:

    >>> game = TestGameThatNotifiesAndExitsImmediately()
    >>> events = game.track_events()
    >>> GameLoop.create_null(events=[[Event("some event")]]).run(game)
    >>> events
    TICK =>
        dt: 0
        events: ['some event']
    """

    @staticmethod
    def create():
        return GameLoop(pygame)

    @staticmethod
    def create_null(events=[]):
        class NullPygame:
            def init(self):
                self.display = NullDisplay()
                self.draw = NullDraw()
                self.event = NullEvent()
                self.time = NullTime()
            def quit(self):
                pass
        class NullDisplay:
            def set_mode(self, resolution):
                return NullScreen()
            def flip(self):
                pass
        class NullScreen:
            def fill(self, color):
                pass
        class NullDraw:
            def circle(self, screen, color, position, radius):
                pass
        class NullEvent:
            def get(self):
                if events:
                    return [x.pygame_event for x in events.pop(0)]
                return []
        class NullTime:
            class Clock:
                def tick(self, fps):
                    return 1
        return GameLoop(NullPygame())

    @staticmethod
    def create_event_user_closed_window():
        """
        >>> GameLoop.create_event_user_closed_window().is_user_closed_window()
        True
        """
        return Event(pygame.event.Event(pygame.QUIT))

    def __init__(self, pygame):
        Observable.__init__(self)
        self.pygame = pygame

    def run(self, game, resolution=(1280, 720), fps=60):
        self.notify("GAMELOOP_INIT", {"resolution": resolution, "fps": fps})
        self.pygame.init()
        self.screen = self.pygame.display.set_mode(resolution)
        clock = self.pygame.time.Clock()
        dt = 0
        try:
            while True:
                game.tick(dt, [Event(x) for x in self.pygame.event.get()])
                self.pygame.display.flip()
                dt = clock.tick(fps)
        except ExitGameLoop:
            pass
        finally:
            self.notify("GAMELOOP_QUIT", {})
            self.pygame.quit()

    def clear_screen(self):
        self.notify("CLEAR_SCREEN", {})
        self.screen.fill("purple")

    def draw_circle(self, x):
        self.notify("DRAW_CIRCLE", {"x": x})
        self.pygame.draw.circle(self.screen, "red", (x, 50), 40)

    def quit(self):
        raise ExitGameLoop()

class Event:

    def __init__(self, pygame_event):
        self.pygame_event = pygame_event

    def is_user_closed_window(self):
        return self.pygame_event.type == pygame.QUIT

    def __repr__(self):
        return repr(self.pygame_event)

class ExitGameLoop(Exception):
    pass

class TestGameThatNotifiesAndExitsImmediately(Observable):

    def tick(self, dt, events):
        self.notify("TICK", {"dt": dt, "events": events})
        raise ExitGameLoop()
