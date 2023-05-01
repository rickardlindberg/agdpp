from gameloop import ExitGameLoop
from gameloop import GameLoop
from gameloop import KEY_LEFT
from gameloop import KEY_RIGHT
from gameloop import KEY_SPACE
from gameloop import XBOX_A
from geometry import Angle
from geometry import OutsideScreenSpace
from geometry import Point
from sprites import SpriteGroup

class BalloonShooter:

    """
    I am a balloon shooter game!

    Initial state
    =============

    We run the game for a few frames, then quit:

    >>> events = BalloonShooter.run_in_test_mode(
    ...     events=[
    ...         [],
    ...         [],
    ...         [],
    ...         [],
    ...         [],
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )

    The game loop is initialized and cleaned up:

    >>> events.filter("GAMELOOP_INIT", "GAMELOOP_QUIT")
    GAMELOOP_INIT =>
        resolution: (1280, 720)
        fps: 60
    GAMELOOP_QUIT =>

    The balloon is drawn animated:

    >>> set(events.filter("DRAW_CIRCLE", radius=40).collect("x", "y"))
    {(50, 50), (51, 50)}

    The arrow is drawn in a fixed position:

    >>> set(events.filter("DRAW_CIRCLE", radius=10).collect("x", "y"))
    {(600, 600)}
    >>> set(events.filter("DRAW_CIRCLE", radius=15).collect("x", "y"))
    {(600, 620)}
    >>> set(events.filter("DRAW_CIRCLE", radius=20).collect("x", "y"))
    {(600, 640)}

    The score is drawn:

    >>> set(events.filter("DRAW_TEXT").collect("text"))
    {('0',)}

    User presses space key
    ======================

    We run the game for a few frames, press the space key, let it run for a few
    frames, then quit:

    >>> events = BalloonShooter.run_in_test_mode(
    ...     events=[
    ...         [],
    ...         [],
    ...         [GameLoop.create_event_keydown(KEY_SPACE)],
    ...         [],
    ...         [],
    ...         [GameLoop.create_event_user_closed_window()],
    ...     ]
    ... )

    The arrow moves:

    >>> arrow_head_positions = events.filter("DRAW_CIRCLE", radius=10).collect("x", "y")
    >>> len(arrow_head_positions) > 1
    True
    >>> len(set(arrow_head_positions)) > 1
    True

    Creation
    ========

    The real BalloonShooter is not created anywhere but when we run the game.
    This test serves to prove that it at least can be instantiated without
    errors.

    >>> isinstance(BalloonShooter.create(), BalloonShooter)
    True
    """

    @staticmethod
    def create():
        return BalloonShooter(GameLoop.create())

    @staticmethod
    def run_in_test_mode(events=[]):
        loop = GameLoop.create_null(
            events=events+[
                [GameLoop.create_event_user_closed_window()],
            ]
        )
        events = loop.track_events()
        BalloonShooter(loop).run()
        return events

    def __init__(self, loop):
        self.loop = loop
        self.resolution = (1280, 720)
        self.game_scene = GameScene(OutsideScreenSpace(*self.resolution))

    def run(self):
        self.loop.run(self, resolution=self.resolution)

    def event(self, event):
        self.game_scene.event(event)

    def tick(self, dt):
        self.game_scene.update(dt)
        self.loop.clear_screen()
        self.game_scene.draw(self.loop)

class GameScene(SpriteGroup):

    """
    >>> space = OutsideScreenSpace(1280, 720)

    Initial state
    =============

    The balloon animates:

    >>> game = GameScene(space)
    >>> first_position = game.get_balloon_position()
    >>> game.update(10)
    >>> second_position = game.get_balloon_position()
    >>> first_position == second_position
    False

    The arrow stays still:

    >>> game = GameScene(space)
    >>> first_position = game.get_arrow_position()
    >>> game.update(10)
    >>> second_position = game.get_arrow_position()
    >>> first_position == second_position
    True

    It has no flying arrows:

    >>> game = GameScene(space)
    >>> game.get_flying_arrows()
    []

    Pressing space key
    ==================

    >>> game = GameScene(space)
    >>> initial_position = game.get_arrow_position()
    >>> game.event(GameLoop.create_event_keydown(KEY_SPACE))
    >>> game.update(10)

    It makes the arrow fire:

    >>> flying = game.get_flying_arrows()
    >>> len(flying)
    1
    >>> flying[0].get_position() == initial_position
    False

    The initial arrow stays the same:

    >>> game.get_arrow_position() == initial_position
    True

    Arrow colliding with balloon
    ============================

    >>> game = GameScene(space, balloons=[(100, 100)], arrows=[(500, 500)])
    >>> len(game.get_balloons())
    1
    >>> len(game.get_flying_arrows())
    1
    >>> game.update(0)
    >>> len(game.get_balloons())
    1
    >>> len(game.get_flying_arrows())
    1

    >>> game = GameScene(space, balloons=[(500, 500)], arrows=[(500, 500)])
    >>> balloons = game.get_balloons()
    >>> len(balloons)
    1
    >>> game.get_score()
    0
    >>> game.update(0)
    >>> new_balloons = game.get_balloons()
    >>> len(new_balloons)
    1
    >>> new_balloons == balloons
    False
    >>> game.get_score()
    1

    Changing arrow angle
    ====================

    >>> game = GameScene(space)
    >>> game.get_arrow_angle()
    Angle(-90)
    >>> game.event(GameLoop.create_event_keydown(KEY_LEFT))
    >>> game.get_arrow_angle()
    Angle(-95.0)
    >>> game.event(GameLoop.create_event_keydown(KEY_RIGHT))
    >>> game.get_arrow_angle()
    Angle(-90.0)

    Arrows flying outside screen
    ============================

    They are removed:

    >>> game = GameScene(space)
    >>> game.event(GameLoop.create_event_keydown(KEY_SPACE))
    >>> game.update(10000)
    >>> game.get_flying_arrows()
    []
    """

    def __init__(self, space, balloons=[(50, 50)], arrows=[]):
        SpriteGroup.__init__(self)
        self.input_handler = InputHandler()
        self.balloons = self.add(SpriteGroup([
            Balloon(Point(x=x, y=y)) for (x, y) in balloons
        ]))
        self.arrow = self.add(Arrow())
        self.flying_arrows = self.add(SpriteGroup([
            Arrow(position=Point(x=x, y=y)) for (x, y) in arrows
        ]))
        self.score = self.add(Score())
        self.space = space

    def event(self, event):
        if event.is_user_closed_window():
            raise ExitGameLoop()
        actions = {
            "set_arrow_angle": lambda angle: self.arrow.set_angle(angle),
        }
        action = self.input_handler.action(event)
        if action:
            actions[action[0]](*action[1:])

    def update(self, dt):
        actions = self.input_handler.pop()
        for shot in actions["shots"]:
            self.flying_arrows.add(self.arrow.clone_shooting())
        SpriteGroup.update(self, dt)
        for arrow in self.flying_arrows.get_sprites():
            if arrow.hits_space(self.space):
                self.flying_arrows.remove(arrow)
            for balloon in self.balloons.get_sprites():
                if arrow.hits_baloon(balloon):
                    self.balloons.remove(balloon)
                    self.balloons.add(Balloon(position=Point(x=50, y=50)))
                    self.score.add(1)

    def get_balloon_position(self):
        return self.balloons.get_sprites()[0].get_position()

    def get_arrow_position(self):
        return self.arrow.get_position()

    def get_flying_arrows(self):
        return self.flying_arrows.get_sprites()

    def get_balloons(self):
        return self.balloons.get_sprites()

    def get_score(self):
        return self.score.score

    def get_arrow_angle(self):
        return self.arrow.angle

class InputHandler:

    def __init__(self):
        self.arrow_angle = Angle.up()
        self.joy_point = Point(x=0, y=0)
        self.empty_actions()

    def empty_actions(self):
        self.actions = {"shots": []}

    def pop(self):
        actions = self.actions
        self.empty_actions()
        return actions

    def action(self, event):
        """
        Space and Xbox A adds a shot:

        >>> i = InputHandler()
        >>> i.action(GameLoop.create_event_keydown(KEY_SPACE))
        >>> i.action(GameLoop.create_event_joystick_down(XBOX_A))
        >>> i.pop()["shots"]
        [1, 1]
        >>> i.pop()["shots"]
        []

        >>> InputHandler().action(GameLoop.create_event_keydown(KEY_LEFT))
        ('set_arrow_angle', Angle(-95.0))

        >>> InputHandler().action(GameLoop.create_event_keydown(KEY_RIGHT))
        ('set_arrow_angle', Angle(-85.0))

        >>> i = InputHandler()
        >>> i.action(GameLoop.create_event_joystick_motion(axis=0, value=0.5))
        ('set_arrow_angle', Angle(0.0))
        >>> i.action(GameLoop.create_event_joystick_motion(axis=1, value=-0.5))
        ('set_arrow_angle', Angle(-45.0))
        """
        if event.is_keydown_space() or event.is_joystick_down(XBOX_A):
            self.actions["shots"].append(1)
            return None
        elif event.is_keydown_left():
            self.arrow_angle = self.arrow_angle.add(-5/360)
            return ('set_arrow_angle', self.arrow_angle)
        elif event.is_keydown_right():
            self.arrow_angle = self.arrow_angle.add(5/360)
            return ('set_arrow_angle', self.arrow_angle)
        elif event.is_joystick_motion():
            if event.get_axis() == 0 and abs(event.get_value()) > 0.1:
                self.joy_point = self.joy_point.set(x=event.get_value())
            elif event.get_axis() == 1 and abs(event.get_value()) > 0.1:
                self.joy_point = self.joy_point.set(y=event.get_value())
            self.arrow_angle = self.joy_point.to_angle()
            return ('set_arrow_angle', self.arrow_angle)

class Arrow:

    def __init__(self, shooting=False, position=Point(x=600, y=600), angle=Angle.up()):
        self.position = position
        self.shooting = shooting
        self.angle = angle

    def set_angle(self, angle):
        self.angle = angle

    def clone_shooting(self):
        """
        It preserves position and angle and set it to shooting:

        >>> arrow = Arrow(position=Point(x=5, y=5), angle=-45)
        >>> new_arrow = arrow.clone_shooting()
        >>> new_arrow.get_position()
        (5, 5)
        >>> new_arrow.angle
        -45
        >>> new_arrow.shooting
        True
        """
        return Arrow(shooting=True, position=self.position, angle=self.angle)

    def hits_space(self, space):
        return space.hits(self.position, 20)

    def hits_baloon(self, balloon):
        return balloon.inside(self.position)

    def update(self, dt):
        if self.shooting:
            self.position = self.position.add(self.angle.to_unit_point().times(dt))

    def draw(self, loop):
        v = self.angle.add(180/360).to_unit_point()
        loop.draw_circle(self.position, color="blue", radius=10)
        loop.draw_circle(self.position.add(v.times(20)), color="blue", radius=15)
        loop.draw_circle(self.position.add(v.times(40)), color="blue", radius=20)

    def get_position(self):
        return (self.position.x, self.position.y)

class Balloon:

    def __init__(self, position, radius=40):
        self.position = position
        self.radius = radius

    def inside(self, position):
        """
        >>> balloon = Balloon(Point(x=50, y=50), radius=20)
        >>> balloon.inside(Point(50, 50))
        True
        >>> balloon.inside(Point(100, 100))
        False
        """
        return self.position.distance_to(position) <= self.radius

    def update(self, dt):
        if self.position.x > 1200:
            self.position = self.position.set(x=50)
        else:
            self.position = self.position.move(dx=dt*0.3)

    def draw(self, loop):
        loop.draw_circle(position=self.position, radius=self.radius)

    def get_position(self):
        return (self.position.x, self.position.y)

class Score:

    def __init__(self):
        self.score = 0

    def add(self, points):
        self.score += points

    def update(self, dt):
        pass

    def draw(self, loop):
        loop.draw_text(position=Point(x=1100, y=20), text=str(self.score))

if __name__ == "__main__":
    BalloonShooter.create().run()
