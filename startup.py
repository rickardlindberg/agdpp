from gameloop import ExitGameLoop
from gameloop import GameLoop

class StartupApplication:

    """
    I draw an application select screen:
    >>> StartupApplication.run_in_test_mode(
    ...     events=[
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    GAMELOOP_QUIT =>
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    GAMELOOP_QUIT =>
    """

    @staticmethod
    def create():
        """
        >>> isinstance(StartupApplication.create(), StartupApplication)
        True
        """
        return StartupApplication(
            loop=GameLoop.create(),
            loop_condition=InifiteLoopCondition()
        )

    @staticmethod
    def run_in_test_mode(events=[]):
        loop = GameLoop.create_null(
            events=events+[
                [GameLoop.create_event_user_closed_window()],
            ]
        )
        events = loop.track_events()
        StartupApplication(
            loop=loop,
            loop_condition=FiniteLoopCondition(2)
        ).run()
        return events

    def __init__(self, loop, loop_condition):
        self.loop = loop
        self.loop_condition = loop_condition

    def run(self):
        while self.loop_condition.active():
            self.loop.run(self)

    def event(self, event):
        if event.is_user_closed_window():
            raise ExitGameLoop()

    def tick(self, dt):
        pass

class InifiteLoopCondition:

    def active(self):
        """
        >>> InifiteLoopCondition().active()
        True
        """
        return True

class FiniteLoopCondition:

    def __init__(self, iterations):
        self.iterations = iterations
        self.count = 0

    def active(self):
        """
        >>> condition = FiniteLoopCondition(iterations=2)
        >>> condition.active()
        True
        >>> condition.active()
        True
        >>> condition.active()
        False
        """
        flag = self.count < self.iterations
        self.count += 1
        return flag

if __name__ == "__main__":
    StartupApplication.create().run()
