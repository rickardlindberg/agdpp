from events import Observable

import pygame

class GameLoop(Observable):

    """
    I init and clean up pygame:

    >>> loop = GameLoop.create_null()
    >>> events = loop.track_events()
    >>> loop.run(TestGameThatNotifiesAndExitsImmediately())
    >>> events
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    GAMELOOP_QUIT =>

    I do the same thing when run for real:

    >>> loop = GameLoop.create()
    >>> events = loop.track_events()
    >>> loop.run(TestGameThatNotifiesAndExitsImmediately())
    >>> events
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    GAMELOOP_QUIT =>

    I pass simulated events to the game tick method:

    >>> game = TestGameThatNotifiesAndExitsImmediately()
    >>> events = game.track_events()
    >>> GameLoop.create_null(events=[[Event(pygame.event.Event(pygame.QUIT))]]).run(game)
    >>> events
    EVENT =>
        event: <Event(256-Quit {})>
    TICK =>
        dt: 0
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
                    return [x.pygame_event for x in events.pop(0)]
                return []
        class NullTime:
            class Clock:
                def tick(self, fps):
                    return 1
        return GameLoop(NullPygame())

    @staticmethod
    def create_event_user_closed_window():
        """
        >>> GameLoop.create_event_user_closed_window().is_user_closed_window()
        True
        """
        return Event(pygame.event.Event(pygame.QUIT))

    @staticmethod
    def create_event_keydown_space():
        """
        >>> GameLoop.create_event_keydown_space().is_keydown_space()
        True
        """
        return Event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))

    @staticmethod
    def create_event_keydown_left():
        """
        >>> GameLoop.create_event_keydown_left().is_keydown_left()
        True
        """
        return Event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))

    @staticmethod
    def create_event_keydown_right():
        """
        >>> GameLoop.create_event_keydown_right().is_keydown_right()
        True
        """
        return Event(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))

    @staticmethod
    def create_event_joystick_down(button):
        """
        >>> event = GameLoop.create_event_joystick_down(button=5)
        >>> event.is_joystick_down(5)
        True
        >>> event.is_joystick_down(4)
        False
        """
        return Event(pygame.event.Event(pygame.JOYBUTTONDOWN, button=button))

    def __init__(self, pygame):
        Observable.__init__(self)
        self.pygame = pygame

    def run(self, game, resolution=(1280, 720), fps=60):
        self.notify("GAMELOOP_INIT", {"resolution": resolution, "fps": fps})
        self.pygame.init()
        self.screen = self.pygame.display.set_mode(resolution)
        clock = self.pygame.time.Clock()
        dt = 0
        joysticks = {}
        try:
            while True:
                pygame_events = self.pygame.event.get()
                for event in pygame_events:
                    if event.type == pygame.JOYDEVICEADDED:
                        joy = self.pygame.joystick.Joystick(event.device_index)
                        joysticks[joy.get_instance_id()] = joy
                    else:
                        game.event(Event(event))
                game.tick(dt)
                self.pygame.display.flip()
                dt = clock.tick(fps)
        except ExitGameLoop:
            pass
        finally:
            self.notify("GAMELOOP_QUIT", {})
            self.pygame.quit()

    def clear_screen(self):
        self.notify("CLEAR_SCREEN", {})
        self.screen.fill("purple")

    def draw_circle(self, position, radius=40, color="red"):
        self.notify("DRAW_CIRCLE", {
            "x": int(position.x),
            "y": int(position.y),
            "radius": radius,
            "color": color,
        })
        self.pygame.draw.circle(
            self.screen,
            color,
            (int(position.x), int(position.y)),
            radius
        )

class Event:

    def __init__(self, pygame_event):
        self.pygame_event = pygame_event

    def is_user_closed_window(self):
        return self.pygame_event.type == pygame.QUIT

    def is_keydown_space(self):
        return self.is_keydown(pygame.K_SPACE)

    def is_keydown_left(self):
        return self.is_keydown(pygame.K_LEFT)

    def is_keydown_right(self):
        return self.is_keydown(pygame.K_RIGHT)

    def is_keydown(self, key):
        return self.pygame_event.type == pygame.KEYDOWN and self.pygame_event.key == key

    def is_joystick_down(self, button):
        return (
            self.pygame_event.type == pygame.JOYBUTTONDOWN and
            self.pygame_event.button == button
        )

    def get_button(self):
        return self.pygame_event.button

    def __repr__(self):
        return repr(self.pygame_event)

class ExitGameLoop(Exception):
    pass

class TestGameThatNotifiesAndExitsImmediately(Observable):

    def event(self, event):
        self.notify("EVENT", {"event": event})

    def tick(self, dt):
        self.notify("TICK", {"dt": dt})
        raise ExitGameLoop()
