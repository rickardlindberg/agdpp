#!/usr/bin/env python3

from events import Observable
from events import Events

import pygame

class Game:

    """
    I draw an animated circle until the user closes the window.

    >>> loop = GameLoop.create_null()
    >>> events = loop.track_events()
    >>> Game(loop).run()
    >>> events
    PYGAME_INIT =>
    DRAW_CIRCLE =>
    EXIT =>
    """

    def __init__(self, loop):
        self.loop = loop

    def run(self):
        self.loop.run(self)

    def tick(self):
        self.loop.draw_circle()

class NullGame:

    def tick(self):
        pass

class GameLoop(Observable):

    """
    I init and clean up pygame:

    >>> loop = GameLoop.create_null()
    >>> events = loop.track_events()
    >>> loop.run(NullGame())
    >>> events
    PYGAME_INIT =>
    EXIT =>

    >>> GameLoop.create().run(NullGame())

    * call tick method of game
    * draw circles on current frame
    """

    @staticmethod
    def create():
        return GameLoop(pygame)

    @staticmethod
    def create_null():
        class NullPygame:
            def init(self):
                pass
            def quit(self):
                pass
        return GameLoop(NullPygame())

    def __init__(self, pygame):
        Observable.__init__(self)
        self.pygame = pygame

    def run(self, game):
        self.notify("PYGAME_INIT", {})
        self.pygame.init()
        game.tick()
        self.notify("EXIT", {})
        self.pygame.quit()

    def draw_circle(self):
        self.notify("DRAW_CIRCLE", {})

if __name__ == "__main__":
    Game(GameLoop.create()).run()
