#!/usr/bin/env python3

from events import Observable
from events import Events

import pygame

class Game:

    """
    I draw an animated circle until the user closes the window.

    >>> loop = GameLoop.create_null(
    ...     events=[
    ...         [],
    ...         [pygame.event.Event(pygame.QUIT)],
    ...     ]
    ... )
    >>> events = loop.track_events()
    >>> Game(loop).run()
    >>> events
    PYGAME_INIT =>
    DRAW_CIRCLE =>
    PYGAME_QUIT =>
    """

    def __init__(self, loop):
        self.loop = loop

    def run(self):
        self.loop.run(self)

    def tick(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                return True
        self.loop.draw_circle()

class NullGame(Observable):

    def tick(self, events):
        self.notify("EVENTS", {"events": events})
        return True

class GameLoop(Observable):

    """
    I init and clean up pygame:

    >>> loop = GameLoop.create_null()
    >>> events = loop.track_events()
    >>> loop.run(NullGame())
    >>> events
    PYGAME_INIT =>
    PYGAME_QUIT =>

    I can simulate events:

    >>> game = NullGame()
    >>> events = game.track_events()
    >>> GameLoop.create_null(events=[[1], [2]]).run(game)
    >>> events
    EVENTS =>
        events: [1]

    * call tick method of game until we should exit
    * draw circles on current frame
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
            def quit(self):
                pass
        class NullDisplay:
            def set_mode(self, resolution):
                return NullScreen()
            def flip(self):
                pass
        class NullScreen:
            pass
        class NullDraw:
            def circle(self, screen, color, position, radius):
                pass
        class NullEvent:
            def get(self):
                if events:
                    return events.pop(0)
                return []
        return GameLoop(NullPygame())

    def __init__(self, pygame):
        Observable.__init__(self)
        self.pygame = pygame

    def run(self, game):
        self.notify("PYGAME_INIT", {})
        self.pygame.init()
        self.screen = self.pygame.display.set_mode((1280, 720))
        running = True
        while running:
            if game.tick(self.pygame.event.get()):
                running = False
            self.pygame.display.flip()
        self.notify("PYGAME_QUIT", {})
        self.pygame.quit()

    def draw_circle(self):
        self.notify("DRAW_CIRCLE", {})
        self.pygame.draw.circle(self.screen, "red", (50, 50), 40)

if __name__ == "__main__":
    Game(GameLoop.create()).run()
