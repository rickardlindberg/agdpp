from gameloop import ExitGameLoop
from gameloop import GameLoop

class StartupApplication:

    """
    I draw an application select screen:

    >>> events = StartupApplication.run_in_test_mode(
    ...     events=[
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )
    """

    @staticmethod
    def run_in_test_mode(events=[]):
        loop = GameLoop.create_null(
            events=events+[
                [GameLoop.create_event_user_closed_window()],
            ]
        )
        events = loop.track_events()
        StartupApplication(loop).run()
        return events

    def __init__(self, loop):
        self.loop = loop

    def run(self):
        self.loop.run(self)

    def event(self, event):
        if event.is_user_closed_window():
            raise ExitGameLoop()

    def tick(self, dt):
        pass
