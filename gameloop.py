from events import Observable

import pygame

KEY_SPACE = pygame.K_SPACE
KEY_LEFT = pygame.K_LEFT
KEY_RIGHT = pygame.K_RIGHT
XBOX_A = 0
XBOX_START = 7

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
            def __init__(self):
                self.display = NullDisplay()
                self.draw = NullDraw()
                self.event = NullEvent()
                self.time = NullTime()
                self.font = NullFontModule()
                self.mixer = NullMixerModule()
            def init(self):
                pass
            def quit(self):
                pass
        class NullMixerModule:
            def pre_init(self, freq):
                pass
            def init(self):
                pass
            class Sound:
                def __init__(self, path):
                    pass
                def play(self):
                    pass
        class NullFont:
            def __init__(self, size):
                pass
            def render(self, text, antialiased, color):
                pass
        class NullFontModule:
            Font = NullFont
            def get_default_font(self):
                return NullFont()
        class NullDisplay:
            def set_mode(self, resolution):
                return NullScreen()
            def flip(self):
                pass
        class NullScreen:
            def fill(self, color):
                pass
            def blit(self, surface, destination):
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
    def create_event_keydown(key):
        """
        >>> GameLoop.create_event_keydown(KEY_LEFT).is_keydown(KEY_LEFT)
        True
        """
        return Event(pygame.event.Event(pygame.KEYDOWN, key=key))

    @staticmethod
    def create_event_keyup(key):
        """
        >>> GameLoop.create_event_keyup(KEY_LEFT).is_keyup(KEY_LEFT)
        True
        """
        return Event(pygame.event.Event(pygame.KEYUP, key=key))

    @staticmethod
    def create_event_joystick_down(button, instance_id=5):
        """
        >>> event = GameLoop.create_event_joystick_down(button=5, instance_id=5)
        >>> event.is_joystick_down(5)
        True
        >>> event.is_joystick_down(4)
        False
        >>> event.get_instance_id()
        5
        """
        return Event(pygame.event.Event(pygame.JOYBUTTONDOWN, button=button, instance_id=instance_id))

    @staticmethod
    def create_event_joystick_motion(axis=0, value=0, instance_id=5):
        """
        >>> event = GameLoop.create_event_joystick_motion(axis=0, value=0.5)
        >>> event.is_joystick_motion()
        True
        >>> event.get_axis()
        0
        >>> event.get_value()
        0.5
        >>> event.get_instance_id()
        5
        """
        return Event(pygame.event.Event(pygame.JOYAXISMOTION, axis=axis, value=value, instance_id=instance_id))

    def __init__(self, pygame):
        Observable.__init__(self)
        self.pygame = pygame

    def run(self, game, resolution=(1280, 720), fps=60):
        self.notify("GAMELOOP_INIT", {"resolution": resolution, "fps": fps})
        self.pygame.mixer.pre_init(48000)
        self.pygame.init()
        self.pygame.mixer.init()
        self.screen = self.pygame.display.set_mode(resolution)
        clock = self.pygame.time.Clock()
        dt = 0
        joysticks = {}
        try:
            while True:
                for event in self.pygame.event.get():
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

    def load_sound(self, path):
        return Sound(self.pygame.mixer.Sound(path))

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
        if position.x >= 0:
            # https://github.com/pygame/pygame/issues/3778
            self.pygame.draw.circle(
                self.screen,
                color,
                (int(position.x), int(position.y)),
                radius
            )

    def draw_text(self, position, text, size=100, color="black"):
        self.notify("DRAW_TEXT", {
            "x": position.x,
            "y": position.y,
            "text": text,
            "color": color,
        })
        f = self.pygame.font.Font(size=size)
        surface = f.render(text, True, color)
        self.screen.blit(surface, (position.x, position.y))

class Sound:

    def __init__(self, pygame_sound):
        self.pygame_sound = pygame_sound

    def play(self):
        self.pygame_sound.play()

class Event:

    def __init__(self, pygame_event):
        self.pygame_event = pygame_event

    def is_user_closed_window(self):
        return self.pygame_event.type == pygame.QUIT

    def is_keydown(self, key):
        return self.pygame_event.type == pygame.KEYDOWN and self.pygame_event.key == key

    def is_keyup(self, key):
        return self.pygame_event.type == pygame.KEYUP and self.pygame_event.key == key

    def is_joystick_down(self, button):
        return (
            self.pygame_event.type == pygame.JOYBUTTONDOWN and
            self.pygame_event.button == button
        )

    def get_button(self):
        return self.pygame_event.button

    def is_joystick_motion(self):
        return self.pygame_event.type == pygame.JOYAXISMOTION

    def get_axis(self):
        return self.pygame_event.axis

    def get_value(self):
        return self.pygame_event.value

    def get_instance_id(self):
        return self.pygame_event.instance_id

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
