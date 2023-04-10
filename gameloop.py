from events import Observable

import pygame

class GameLoop(Observable):

    """
    I init and clean up pygame:

    >>> loop = GameLoop.create_null()
    >>> events = loop.track_events()
    >>> loop.run(TestGameThatNotifiesAndExitsImmediately())
    >>> events
    PYGAME_INIT =>
    PYGAME_QUIT =>

    I do the same thing when run for real:

    >>> loop = GameLoop.create()
    >>> events = loop.track_events()
    >>> loop.run(TestGameThatNotifiesAndExitsImmediately())
    >>> events
    PYGAME_INIT =>
    PYGAME_QUIT =>

    I can simulate events:

    >>> game = TestGameThatNotifiesAndExitsImmediately()
    >>> events = game.track_events()
    >>> GameLoop.create_null(events=[[1], [2]]).run(game)
    >>> events
    TICK =>
    EVENTS =>
        events: [1]
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
                    return events.pop(0)
                return []
        class NullTime:
            class Clock:
                def tick(self, fps):
                    return 1
        return GameLoop(NullPygame())

    def __init__(self, pygame):
        Observable.__init__(self)
        self.pygame = pygame

    def run(self, game):
        self.notify("PYGAME_INIT", {})
        self.pygame.init()
        self.screen = self.pygame.display.set_mode((1280, 720))
        clock = self.pygame.time.Clock()
        dt = 0
        try:
            while True:
                game.tick(dt, self.pygame.event.get())
                self.pygame.display.flip()
                dt = clock.tick(60)
        except ExitGameLoop:
            pass
        finally:
            self.notify("PYGAME_QUIT", {})
            self.pygame.quit()

    def clear_screen(self):
        self.notify("CLEAR_SCREEN", {})
        self.screen.fill("purple")

    def draw_circle(self, x):
        self.notify("DRAW_CIRCLE", {"x": x})
        self.pygame.draw.circle(self.screen, "red", (x, 50), 40)

    def quit(self):
        raise ExitGameLoop()

class ExitGameLoop(Exception):
    pass

class TestGameThatNotifiesAndExitsImmediately(Observable):

    def tick(self, dt, events):
        self.notify("TICK", {})
        self.notify("EVENTS", {"events": events})
        raise ExitGameLoop()
