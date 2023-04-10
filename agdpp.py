#!/usr/bin/env python3

import pygame

from gameloop import GameLoop

class Game:

    """
    I draw an animated circle until the user closes the window.

    >>> loop = GameLoop.create_null(
    ...     events=[
    ...         [],
    ...         [],
    ...         [pygame.event.Event(pygame.QUIT)],
    ...     ]
    ... )
    >>> events = loop.track_events()
    >>> Game(loop).run()
    >>> events
    PYGAME_INIT =>
    CLEAR_SCREEN =>
    DRAW_CIRCLE =>
        x: 50
    CLEAR_SCREEN =>
    DRAW_CIRCLE =>
        x: 51
    PYGAME_QUIT =>
    """

    def __init__(self, loop):
        self.loop = loop
        self.x = 50

    def run(self):
        self.loop.run(self)

    def tick(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.loop.quit()
        if self.x > 500:
            self.x = 50
        else:
            self.x += dt
        self.loop.clear_screen()
        self.loop.draw_circle(self.x)

if __name__ == "__main__":
    Game(GameLoop.create()).run()
