import manim
from manim import *


class Clock(Mobject):
    """Clock is an object that represents a clock.
    It has an outer circle as the clock face.
    A line with a tip represents the clock hand.


    Args:
        Mobject (_type_): _description_
    """

    def __init__(self, radius: float = 1.0, **kwargs) -> None:
        """The init method creates a clock object. It creates a circle, a line with a tip and a dot.
         It groups them and adds them to the object in order to use the clock as like a normal manim object.

        Args:
            radius (float, optional): Radius sets the radius of the clock. Defaults to 1.0.
            stroke_width (float, optional): stroke_width sets the stroke_width for all elements.
            The tip of the clock hand also uses this with a scaling factor. Defaults to 10.0.
        """
        stroke_width = radius * 5
        super().__init__(**kwargs)
        self.circle = Circle(radius=radius, stroke_width=stroke_width)

        self.line = Line(
            start=self.circle.get_center(),
            end=UP * radius * 0.9,
            stroke_width=stroke_width,
        )
        factor = 35

        self.line.add_tip(
            tip_length=radius * 4 / factor,
            tip_width=radius * 3 / factor,
            at_start=False,
        )

        self.dot = Dot(
            self.circle.get_center(), stroke_width=stroke_width, radius=radius / 20
        )
        

        self.clock = VGroup(self.circle, self.line, self.dot)

        self.add(self.clock)

    def rotate(self, scene: manim.Scene, duration: float = 1, angle: int = PI * 2):
        """Use this method to rotate the clock handle around the middle of the clock.

        Args:
            scene (manim.Scene): This must be the scene in which you want the rotation animation to be played.
            duration (float, optional): The duration of the animation in seconds. Defaults to 1.
            angle (int, optional): The angle how much the handle is moved. PI*2 is one full rotation. Defaults to PI*2.
        """
        scene.play(
            Rotate(
                self.line,
                angle=angle,
                about_point=self.clock.get_center(),
                axis=Z_AXIS,
                rate_func=linear,
            ),
            run_time=duration,
        )
