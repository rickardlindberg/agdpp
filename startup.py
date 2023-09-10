from events import Events
from events import Observable
from gameloop import ExitGameLoop
from gameloop import GameLoop
from gameloop import XBOX_A
from geometry import Point

import subprocess

class StartupApplication:

    """
    I draw an application select screen:

    >>> StartupApplication.run_in_test_mode(
    ...     events=[
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ],
    ...     iterations=2
    ... )
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    CLEAR_SCREEN =>
    DRAW_TEXT =>
        x: 100
        y: 100
        text: 'SuperTux'
        color: 'black'
    DRAW_TEXT =>
        x: 100
        y: 200
        text: 'Balloon Shooter'
        color: 'lightblue'
    DRAW_CIRCLE =>
        x: 500
        y: 500
        radius: 20
        color: 'pink'
    GAMELOOP_QUIT =>
    COMMAND =>
        command: ['python', '/home/.../agdpp/agdpp.py']
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    CLEAR_SCREEN =>
    DRAW_TEXT =>
        x: 100
        y: 100
        text: 'SuperTux'
        color: 'black'
    DRAW_TEXT =>
        x: 100
        y: 200
        text: 'Balloon Shooter'
        color: 'lightblue'
    DRAW_CIRCLE =>
        x: 500
        y: 500
        radius: 20
        color: 'pink'
    GAMELOOP_QUIT =>
    COMMAND =>
        command: ['python', '/home/.../agdpp/agdpp.py']

    >>> StartupApplication.run_in_test_mode(
    ...     events=[
    ...         [],
    ...         [GameLoop.create_event_joystick_motion(axis=1, value=1.0)],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ],
    ...     iterations=1
    ... ).filter("DRAW_CIRCLE")
    DRAW_CIRCLE =>
        x: 500
        y: 500
        radius: 20
        color: 'pink'
    DRAW_CIRCLE =>
        x: 500
        y: 501
        radius: 20
        color: 'pink'
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
    def run_in_test_mode(events=[], iterations=2):
        loop = GameLoop.create_null(
            events=events+[
                [GameLoop.create_event_user_closed_window()],
            ]
        )
        events = Events()
        StartupApplication(
            loop=events.track(loop),
            loop_condition=FiniteLoopCondition(iterations),
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
        self.startup_scene.update(dt)
        self.startup_scene.draw(self.loop)

class Command(Observable):

    """
    >>> Command.create().run(["echo", "hello"])

    >>> Command.create().run(["command-that-does-not-exist"])
    Traceback (most recent call last):
      ...
    FileNotFoundError: [Errno 2] No such file or directory: 'command-that-does-not-exist'

    >>> Command.create_null().run(["command-that-does-not-exist"])
    """

    @staticmethod
    def create():
        return Command(subprocess=subprocess)

    @staticmethod
    def create_null():
        class NullSubprocess:
            def run(self, command):
                pass
        return Command(subprocess=NullSubprocess())

    def __init__(self, subprocess):
        Observable.__init__(self)
        self.subprocess = subprocess

    def run(self, command):
        self.notify("COMMAND", {"command": command})
        self.subprocess.run(command)

class StartupScene:

    def __init__(self):
        self.cursor = Point(x=500, y=500)
        self.games = [
            Game(
                name="SuperTux",
                position=Point(x=100, y=100),
                command=["supertux2"],
            ),
            Game(
                name="Balloon Shooter",
                position=Point(x=100, y=200),
                command=["python", "/home/.../agdpp/agdpp.py"],
            ),
        ]
        self.dx = 0
        self.dy = 0

    def move_cursor(self, x, y):
        self.cursor = Point(x=x, y=y)

    def get_command(self):
        """
        >>> scene = StartupScene()

        >>> scene.move_cursor(x=100, y=100)
        >>> scene.get_command()
        ['supertux2']

        >>> scene.move_cursor(x=100, y=200)
        >>> scene.get_command()
        ['python', '/home/.../agdpp/agdpp.py']
        """
        return self.game_closest_to_cursor().command

    def game_closest_to_cursor(self):
        return min(
            self.games,
            key=lambda game: game.distance_to(self.cursor)
        )

    def event(self, event):
        """
        >>> StartupScene().event(GameLoop.create_event_user_closed_window())
        Traceback (most recent call last):
          ...
        gameloop.ExitGameLoop

        >>> StartupScene().event(GameLoop.create_event_joystick_down(XBOX_A))
        Traceback (most recent call last):
          ...
        gameloop.ExitGameLoop
        """
        if event.is_user_closed_window() or event.is_joystick_down(XBOX_A):
            raise ExitGameLoop()
        elif event.is_joystick_motion():
            if event.get_axis() == 0:
                self.dx = event.get_value()
            elif event.get_axis() == 1:
                self.dy = event.get_value()

    def update(self, dt):
        delta = Point(x=self.dx, y=self.dy)
        if delta.length() > 0.05:
            self.cursor = self.cursor.add(delta.times(dt))

    def draw(self, loop):
        for game in self.games:
            game.draw(loop, self.game_closest_to_cursor())
        loop.draw_circle(self.cursor, radius=20, color="pink")

class Game:

    def __init__(self, name, position, command):
        self.name = name
        self.position = position
        self.command = command

    def draw(self, loop, closest):
        loop.draw_text(
            self.position,
            text=self.name,
            color="lightblue" if closest is self else "black"
        )

    def distance_to(self, point):
        return self.position.distance_to(point)

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
