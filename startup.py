from events import Events
from events import Observable
from gameloop import ExitGameLoop
from gameloop import GameLoop
from geometry import Point

class StartupApplication:

    """
    I draw an application select screen:

    >>> StartupApplication.run_in_test_mode(
    ...     events=[
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    CLEAR_SCREEN =>
    DRAW_TEXT =>
        x: 100
        y: 100
        text: 'SuperTux'
    DRAW_TEXT =>
        x: 100
        y: 200
        text: 'Balloon Shooter'
    DRAW_CIRCLE =>
        x: 500
        y: 500
        radius: 20
        color: 'pink'
    GAMELOOP_QUIT =>
    COMMAND =>
        command: ['supertux2']
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    CLEAR_SCREEN =>
    DRAW_TEXT =>
        x: 100
        y: 100
        text: 'SuperTux'
    DRAW_TEXT =>
        x: 100
        y: 200
        text: 'Balloon Shooter'
    DRAW_CIRCLE =>
        x: 500
        y: 500
        radius: 20
        color: 'pink'
    GAMELOOP_QUIT =>
    COMMAND =>
        command: ['supertux2']
    """

    @staticmethod
    def create():
        """
        >>> isinstance(StartupApplication.create(), StartupApplication)
        True
        """
        return StartupApplication(
            loop=GameLoop.create(),
            loop_condition=InifiteLoopCondition(),
            command=Command.create()
        )

    @staticmethod
    def run_in_test_mode(events=[]):
        loop = GameLoop.create_null(
            events=events+[
                [GameLoop.create_event_user_closed_window()],
            ]
        )
        events = Events()
        StartupApplication(
            loop=events.track(loop),
            loop_condition=FiniteLoopCondition(2),
            command=events.track(Command.create_null())
        ).run()
        return events

    def __init__(self, loop, loop_condition, command):
        self.loop = loop
        self.loop_condition = loop_condition
        self.startup_scene = StartupScene()
        self.command = command

    def run(self):
        while self.loop_condition.active():
            self.loop.run(self)
            self.command.run(self.startup_scene.get_command())

    def event(self, event):
        self.startup_scene.event(event)

    def tick(self, dt):
        self.loop.clear_screen()
        self.startup_scene.draw(self.loop)

class Command(Observable):

    @staticmethod
    def create():
        return Command()

    @staticmethod
    def create_null():
        return Command()

    def run(self, command):
        self.notify("COMMAND", {"command": command})

class StartupScene:

    def get_command(self):
        return ["supertux2"]

    def event(self, event):
        if event.is_user_closed_window():
            raise ExitGameLoop()

    def draw(self, loop):
        loop.draw_text(Point(x=100, y=100), text="SuperTux")
        loop.draw_text(Point(x=100, y=200), text="Balloon Shooter")
        loop.draw_circle(Point(x=500, y=500), radius=20, color="pink")

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
