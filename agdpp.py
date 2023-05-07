from gameloop import ExitGameLoop
from gameloop import GameLoop
from gameloop import KEY_LEFT
from gameloop import KEY_RIGHT
from gameloop import KEY_SPACE
from gameloop import XBOX_A
from geometry import Angle
from geometry import Point
from geometry import Rectangle
from sprites import SpriteGroup
from state import ResettableValue

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

    >>> len(set(events.filter("DRAW_CIRCLE", radius=40).collect("x", "y"))) > 1
    True

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
        self.game_scene = GameScene(Rectangle.from_size(*self.resolution))

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
    Initial state
    =============

    The arrow stays still:

    >>> game = GameScene(Rectangle.from_size(1280, 720))
    >>> first_position = game.get_arrow_position()
    >>> game.update(10)
    >>> second_position = game.get_arrow_position()
    >>> first_position == second_position
    True

    It has no flying arrows:

    >>> game = GameScene(Rectangle.from_size(1280, 720))
    >>> game.get_flying_arrows()
    []

    The score is zero:

    >>> game.get_score()
    0

    Pressing space key
    ==================

    >>> game = GameScene(Rectangle.from_size(1280, 720))
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

    Shooting arrow
    ==============

    Misses balloon
    --------------

    >>> game = GameScene(
    ...     screen_area=Rectangle.from_size(1280, 720),
    ...     balloons=[Point(x=100, y=100)],
    ...     arrows=[Point(x=500, y=500)]
    ... )
    >>> (balloon_being_missed,) = game.get_balloons()
    >>> (shooting_arrow,) = game.get_flying_arrows()
    >>> game.update(0)

    The balloon is still there:

    >>> balloon_being_missed in game.get_balloons()
    True

    The shooting arrow is still there:

    >>> shooting_arrow in game.get_flying_arrows()
    True

    No points are scored:

    >>> game.get_score()
    0

    Hits balloon
    ------------

    >>> game = GameScene(
    ...     screen_area=Rectangle.from_size(1280, 720),
    ...     balloons=[Point(x=500, y=500)],
    ...     arrows=[Point(x=500, y=500)]
    ... )
    >>> (balloon_being_hit,) = game.get_balloons()
    >>> (shooting_arrow,) = game.get_flying_arrows()
    >>> game.update(0)

    The balloon disappears:

    >>> balloon_being_hit in game.get_balloons()
    False

    The flying arrow disappears:

    >>> shooting_arrow in game.get_flying_arrows()
    False

    One point is scored:

    >>> game.get_score()
    1

    Changing arrow angle
    ====================

    >>> game = GameScene(Rectangle.from_size(1280, 720))
    >>> initial_angle = game.get_arrow_angle()
    >>> game.event(GameLoop.create_event_keydown(KEY_LEFT))
    >>> game.update(1)
    >>> game.get_arrow_angle() < initial_angle
    True

    Arrows flying outside screen
    ============================

    They are removed:

    >>> game = GameScene(Rectangle.from_size(1280, 720))
    >>> game.event(GameLoop.create_event_keydown(KEY_SPACE))
    >>> game.update(10000)
    >>> game.get_flying_arrows()
    []
    """

    def __init__(self, screen_area, balloons=[], arrows=[]):
        SpriteGroup.__init__(self)
        self.input_handler = InputHandler()
        self.balloons = self.add(Balloons(positions=balloons, screen_area=screen_area))
        self.bow = self.add(Bow())
        self.flying_arrows = self.add(SpriteGroup([
            Arrow(position=position) for position in arrows
        ]))
        self.score = self.add(Score())
        self.screen_area = screen_area

    def event(self, event):
        if event.is_user_closed_window():
            raise ExitGameLoop()
        self.input_handler.action(event)

    def update(self, dt):
        self.input_handler.update(dt)
        if self.input_handler.get_shoot():
            self.flying_arrows.add(self.bow.shoot())
        self.bow.turn(self.input_handler.get_turn_angle())
        SpriteGroup.update(self, dt)
        for arrow in self.flying_arrows.get_sprites():
            hit_balloon = self.balloons.get_balloon_hit_by_arrow(arrow)
            if hit_balloon or arrow.is_outside_of(self.screen_area):
                self.flying_arrows.remove(arrow)
            if hit_balloon:
                self.balloons.remove(hit_balloon)
                self.score.add(1)

    def get_arrow_position(self):
        return self.bow.get_position()

    def get_flying_arrows(self):
        return self.flying_arrows.get_sprites()

    def get_balloons(self):
        return self.balloons.get_sprites()

    def get_score(self):
        return self.score.score

    def get_arrow_angle(self):
        return self.bow.get_angle()

class Balloons(SpriteGroup):

    """
    I maintain a list of active balloons.

    Initially I contain balloons at the given positions:

    >>> Balloons().get_sprites()
    []

    >>> balloons = Balloons(positions=[Point(x=10, y=10)])
    >>> [x.get_position() for x in balloons.get_sprites()]
    [Point(x=10, y=10)]

    When updated, I spawn new balloons up the count of 3:

    >>> balloons = Balloons()
    >>> balloons.update(0)
    >>> spawned_balloons = balloons.get_sprites()
    >>> len(spawned_balloons)
    3

    When updated, I move the balloons:

    >>> spawned_positions = [x.get_position() for x in spawned_balloons]
    >>> balloons.update(1)
    >>> spawned_positions == [x.get_position() for x in balloons.get_sprites()]
    False

    When updated, I remove balloons that are outside the screen area:

    >>> balloons = Balloons(
    ...     positions=[Point(x=1000, y=1000)],
    ...     screen_area=Rectangle.from_size(500, 500)
    ... )
    >>> (balloon,) = balloons.get_sprites()
    >>> balloons.update(0)
    >>> balloon in balloons.get_sprites()
    False
    """

    def __init__(self, positions=[], screen_area=Rectangle.from_size(500, 500)):
        SpriteGroup.__init__(self, [
            Balloon(position=position) for position in positions
        ])
        self.screen_area = screen_area

    def update(self, dt):
        SpriteGroup.update(self, dt)
        for balloon in self.get_sprites():
            if balloon.is_outside_of(self.screen_area):
                self.remove(balloon)
        while len(self.get_sprites()) < 3:
            self.spawn_new()

    def get_balloon_hit_by_arrow(self, arrow):
        for balloon in self.get_sprites():
            if arrow.hits_baloon(balloon):
                return balloon

    def spawn_new(self):
        x = self.screen_area.deflate(50).get_random_x()
        self.add(Balloon(position=self.screen_area.topleft.set(x=x)))

class InputHandler:

    """
    Space shoots and resets:

    >>> i = InputHandler()
    >>> i.action(GameLoop.create_event_keydown(KEY_SPACE))
    >>> i.update(1)
    >>> i.get_shoot()
    True
    >>> i.update(1)
    >>> i.get_shoot()
    False

    Xbox A shoots and resets:

    >>> i = InputHandler()
    >>> i.action(GameLoop.create_event_joystick_down(XBOX_A))
    >>> i.update(1)
    >>> i.get_shoot()
    True
    >>> i.update(1)
    >>> i.get_shoot()
    False

    Left keeps turning arrow left:

    >>> i = InputHandler()
    >>> i.action(GameLoop.create_event_keydown(KEY_LEFT))
    >>> i.update(1)
    >>> first_turn_angle = i.get_turn_angle()
    >>> first_turn_angle < Angle.zero()
    True
    >>> i.update(1)
    >>> i.get_turn_angle() == first_turn_angle
    True
    >>> i.action(GameLoop.create_event_keyup(KEY_LEFT))
    >>> i.update(1)
    >>> i.get_turn_angle() == Angle.zero()
    True

    Right keeps turning arrow right:

    >>> i = InputHandler()
    >>> i.action(GameLoop.create_event_keydown(KEY_RIGHT))
    >>> i.update(1)
    >>> first_turn_angle = i.get_turn_angle()
    >>> first_turn_angle > Angle.zero()
    True
    >>> i.update(1)
    >>> i.get_turn_angle() == first_turn_angle
    True
    >>> i.action(GameLoop.create_event_keyup(KEY_RIGHT))
    >>> i.update(1)
    >>> i.get_turn_angle() == Angle.zero()
    True

    Joystick x-axis motion keeps turning arrow.

    >>> i = InputHandler()
    >>> i.action(GameLoop.create_event_joystick_motion(axis=0, value=1))
    >>> i.update(1)
    >>> first_turn_angle = i.get_turn_angle()
    >>> first_turn_angle > Angle.zero()
    True
    >>> i.update(1)
    >>> i.get_turn_angle() == first_turn_angle
    True
    """

    def __init__(self):
        self.arrow_turn_factor = ResettableValue(0)
        self.shoot_down = ResettableValue(False)
        self.turn_speed = 1/2500

    def get_shoot(self):
        return self.shoot

    def get_turn_angle(self):
        return self.turn_angle

    def update(self, dt):
        self.shoot = self.shoot_down.get_and_reset()
        self.turn_angle = Angle.fraction_of_whole(self.arrow_turn_factor.get()*dt*self.turn_speed)

    def action(self, event):
        if event.is_keydown(KEY_SPACE) or event.is_joystick_down(XBOX_A):
            self.shoot_down.set(True)
        elif event.is_keydown(KEY_LEFT):
            self.arrow_turn_factor.set(-1)
        elif event.is_keyup(KEY_LEFT):
            self.arrow_turn_factor.reset()
        elif event.is_keydown(KEY_RIGHT):
            self.arrow_turn_factor.set(1)
        elif event.is_keyup(KEY_RIGHT):
            self.arrow_turn_factor.reset()
        elif event.is_joystick_motion() and event.get_axis() == 0:
            if abs(event.get_value()) > 0.01:
                self.arrow_turn_factor.set(event.get_value())
            else:
                self.arrow_turn_factor.reset()

class Bow(SpriteGroup):

    def __init__(self):
        SpriteGroup.__init__(self)
        self.arrow = self.add(Arrow(angle=Angle.up()))

    def turn(self, angle):
        """
        >>> bow = Bow()
        >>> bow.get_angle()
        Angle(degrees=-90)
        >>> bow.turn(Angle.fraction_of_whole(0.5))
        >>> bow.get_angle()
        Angle(degrees=-90)
        """
        new_angle = self.get_angle().add(angle)
        if new_angle.to_unit_point().y < 0:
            self.arrow.set_angle(new_angle)

    def get_angle(self):
        return self.arrow.get_angle()

    def get_position(self):
        return self.arrow.get_position()

    def shoot(self):
        return self.arrow.clone_shooting()

class Arrow:

    def __init__(self, shooting=False, position=Point(x=600, y=600), angle=Angle.up()):
        self.position = position
        self.shooting = shooting
        self.angle = angle

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle

    def clone_shooting(self):
        """
        It preserves position and angle and set it to shooting:

        >>> arrow = Arrow(position=Point(x=5, y=5), angle=-45)
        >>> new_arrow = arrow.clone_shooting()
        >>> new_arrow.get_position()
        Point(x=5, y=5)
        >>> new_arrow.angle
        -45
        >>> new_arrow.shooting
        True
        """
        return Arrow(shooting=True, position=self.position, angle=self.angle)

    def is_outside_of(self, screen_area):
        return not screen_area.inflate(20).contains(self.position)

    def hits_baloon(self, balloon):
        return balloon.contains(self.position)

    def update(self, dt):
        if self.shooting:
            self.position = self.position.add(self.angle.to_unit_point().times(dt))

    def draw(self, loop):
        v = self.angle.add(Angle.fraction_of_whole(0.5)).to_unit_point()
        loop.draw_circle(self.position, color="blue", radius=10)
        loop.draw_circle(self.position.add(v.times(20)), color="blue", radius=15)
        loop.draw_circle(self.position.add(v.times(40)), color="blue", radius=20)

    def get_position(self):
        return self.position

class Balloon:

    def __init__(self, position, radius=40):
        self.position = position
        self.radius = radius
        self.speed = 0.1

    def is_outside_of(self, screen_area):
        return not screen_area.inflate(self.radius*2).contains(self.position)

    def contains(self, position):
        """
        >>> balloon = Balloon(Point(x=50, y=50), radius=20)
        >>> balloon.contains(Point(50, 50))
        True
        >>> balloon.contains(Point(100, 100))
        False
        """
        return self.position.distance_to(position) <= self.radius

    def update(self, dt):
        """
        I move downwards:

        >>> balloon = Balloon(position=Point(x=50, y=50))
        >>> balloon.get_position()
        Point(x=50, y=50)
        >>> balloon.update(5)
        >>> new_position = balloon.get_position()
        >>> new_position.x
        50
        >>> new_position.y > 50
        True
        """
        self.position = self.position.move(dy=dt*self.speed)

    def draw(self, loop):
        loop.draw_circle(position=self.position, radius=self.radius)

    def get_position(self):
        return self.position

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
