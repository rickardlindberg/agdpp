#!/usr/bin/env python3

from events import Observable
from events import Events

class Game:

    """
    I draw an animated circle until the user closes the window.

    >>> loop = GameLoop()
    >>> events = loop.track_events()
    >>> Game(loop).run()
    >>> events
    DRAW_CIRCLE =>
    EXIT =>
    """

    def __init__(self, loop):
        self.loop = loop

    def run(self):
        self.loop.run(self)

    def tick(self):
        self.loop.draw_circle()

class GameLoop(Observable):

    """
    * init pygame
    * cleanup pygame
    * call tick method of game
    * draw circles on current frame
    """

    def run(self, game):
        game.tick()
        self.notify("EXIT", {})

    def draw_circle(self):
        self.notify("DRAW_CIRCLE", {})

if __name__ == "__main__":
    Game().run()
