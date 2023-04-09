#!/usr/bin/env python3

class Game:

    """
    I draw an animated circle until the user closes the window.

    >>> game = Game(GameLoop())
    >>> game.run()
    DRAW_CIRCLE
    EXIT
    """

    def __init__(self, loop):
        self.loop = loop

    def run(self):
        self.loop.run(self)

    def tick(self):
        self.loop.draw_circle()

class GameLoop:

    def run(self, game):
        game.tick()
        print("EXIT")

    def draw_circle(self):
        print("DRAW_CIRCLE")

if __name__ == "__main__":
    Game().run()
