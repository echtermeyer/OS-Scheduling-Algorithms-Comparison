import math

from typing import List, Dict

import manim
from manim import *

from typing import Tuple


class ProcessAnimated(VGroup):
    """Represents a process in a visual format.

    This class creates a graphical representation of a process, typically depicted as a rectangle whose length indicates the process's size. Optionally, a square representation can be used. The process can also display a title and its size.

    Parameters:
        color (str, optional): Color of the process shape. Default is WHITE.
        size (float, optional): Size of the process, affects shape dimensions. Default is 1.
        title (str, optional): Text label for the process. Default is an empty string.
        use_square (bool, optional): Use a square instead of a rectangle if True. Default is False.
        show_size (bool, optional): Display the size with the title if True. Default is True.
        **kwargs: Additional arguments for VGroup superclass.

    Example usage:
        process_square = Process(color=WHITE, size=5, title="Process 1", use_square=False, show_size=True)
        self.add(process)
    """

    def __init__(
        self, color=WHITE, size=1, title="", use_square=False, show_size=True, **kwargs
    ):
        super().__init__(**kwargs)
        self.color = color
        self.size = size
        self.title = title
        self.use_square = use_square
        self.show_size = show_size

        if self.use_square:
            square_size = self._get_square_size()
            self.shape = (
                Square(side_length=square_size)
                .set_fill(self.color, opacity=1)
                .set_stroke(self.color)
            )
        else:
            self.shape = (
                Rectangle(width=size / 2, height=0.5)
                .set_fill(self.color, opacity=1)
                .set_stroke(self.color)
            )

        self.title_text = self._get_new_title()
        self.add(self.shape, self.title_text)

    def adjust_size_with_animation(self, delta: int = -1) -> AnimationGroup | None:
        """Adjusts the size of the shape object by the given delta returns an animationgroup object that can be used to animate this movement. The size reduction will not appear until using the animationgroup.

        Args:
            delta (int, optional): This is by how much the size should be adjusted in absolut units. Defaults to -1.

        Returns:
            AnimationGroup: This is the animation to be executed in order to see the changes.
        """
        self.size = self.size + delta

        if self.use_square:
            square_size = self._get_square_size()

            # animate the shape to adjust to the new size
            resize_animation = self.shape.animate.set_width(square_size)

            # animate the title to transform from the current to the new title which is set to the new location of the shape.
            # copy is needed to ensure nothing happens to the actual shape, we only need the location of the shape how it will be after the animation
            title_animation = Transform(
                self.title_text,
                self._get_new_title().next_to(
                    self.shape.copy().set_width(square_size), UP
                ),
            )

            return AnimationGroup(resize_animation, title_animation)

        else:
            # animate the shape to adjust to the new size
            resize_animation = self.shape.animate.stretch_to_fit_width(self.size / 2)

            # animate the title to transform from the current to the new title which is set to the new location of the shape.
            # copy is needed to ensure nothing happens to the actual shape, we only need the location of the shape how it will be after the animation
            title_animation = Transform(
                self.title_text,
                self._get_new_title().next_to(
                    self.shape.copy().stretch_to_fit_width(self.size / 2), UP
                ),
            )

            return AnimationGroup(resize_animation, title_animation)

    def _get_square_size(self) -> float:
        """Function to calculate the size of the square.

        Returns:
            float: the size of the square
        """
        return 0.5 + 0.25 * max(0, self.size - 1)

    def _get_new_title(self) -> Text:
        """Creates a new title object to be used to set the title for animation or initialization

        Returns:
            Text: This is the text object already placed next to the shape object
        """
        title_text = self.title
        if self.show_size:
            title_text = f"{title_text}, {self.size}"

        return Text(title_text, font_size=24).next_to(self.shape, UP)

    # def _get_new_title(self):


class CPU(VGroup):
    """
    A class representing a CPU (Central Processing Unit) with an optional gear icon.

    Parameters:
        title (str): The title or label for the CPU.
        color: The color of the CPU and gear (default is WHITE).
        size (float): The size scaling factor for the CPU and gear (default is 1).
        show_gear (bool): Whether to display a gear icon next to the CPU (default is True).
        gear_pos: The position of the gear icon relative to the CPU (default is UR).
        **kwargs: Additional keyword arguments for the VGroup constructor.

    Methods:
        rotate_gear(speed=1, duration=None, angle=None): Rotate the gear icon.

    Example usage:
        cpu = CPU(size=1, title="CPU", color=WHITE, show_gear=True)

        self.add(cpu)

        self.play(cpu.rotate_gear(speed=1, duration=4))
    """

    def __init__(
        self,
        title: str = "",
        color=WHITE,
        size: float = 1,
        show_gear: bool = True,
        gear_pos=UR,
        gear_color=RED,
        alignment: str = "center",
        center: np.ndarray = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.color = color
        self.gear_color = gear_color
        self.size = size
        self.show_gear = show_gear
        self.gear_pos = gear_pos
        self._create_cpu(alignment=alignment, center=center)
        if self.show_gear:
            self._add_gear()

    def _create_cpu(self, alignment, center: np.ndarray = None) -> None:
        self.cpu = SVGMobject("img/cpu.svg", fill_color=self.color).scale(self.size)
        if center is not None:
            self.cpu.move_to(center)
        self.title_object = Paragraph(
            self.title, font_size=24, alignment=alignment
        ).next_to(self.cpu, UP)
        self.add(self.cpu, self.title_object)

    def _add_gear(self) -> None:
        self.gear = SVGMobject("img/gear.svg", fill_color=self.gear_color).scale(
            0.25 * self.size
        )
        self.gear.next_to(self.cpu, self.gear_pos, buff=-0.4 * self.size)
        self.add(self.gear)

    def rotate_gear(self, speed=1, duration=1, angle=None):
        if duration is not None:
            angle = -TAU * speed / 4 * duration
        elif angle is not None:
            pass
        return Rotate(
            self.gear,
            angle=angle,
            about_point=self.gear.get_center(),
            rate_func=linear,
            run_time=duration,
        )


class Clock(Mobject):
    """Clock is an object that represents a clock.
    It has an outer circle as the clock face.
    A line with a tip represents the clock hand.


    Args:
        Mobject (_type_): Inherits from manim Mobject and can therefore be treated like any other object in manim. e.g. set_color()
    """

    def __init__(self, radius: float = 1.0, color=WHITE, **kwargs) -> None:
        """The init method creates a clock object. It creates a circle, a line with a tip and a dot.
        It groups them and adds them to the object in order to use the clock as like a normal manim object.

        Args:
            radius (float, optional): Radius sets the radius of the clock. Defaults to 1.0.
            stroke_width (float, optional): stroke_width sets the stroke_width for all elements.
            The tip of the clock hand also uses this with a scaling factor. Defaults to 10.0.
        """
        super().__init__(**kwargs)
        stroke_width = radius * 5
        self.circle = Circle(radius=radius, stroke_width=stroke_width, color=color)

        self.line = Line(
            start=self.circle.get_center(),
            end=UP * radius * 0.9,
            stroke_width=stroke_width,
            color=color,
        )
        factor = 35

        self.line.add_tip(
            tip_length=radius * 4 / factor,
            tip_width=radius * 3 / factor,
            at_start=False,
        )

        self.dot = Dot(
            self.circle.get_center(),
            stroke_width=stroke_width,
            radius=radius / 20,
            color=color,
        )

        self.clock = VGroup(self.circle, self.line, self.dot)

        self.add(self.clock)

    def rotate(self, duration: float = 1, angle: float = PI * 2) -> manim.Rotate | None:
        """Use this method to rotate the clock handle around the middle of the clock.

        Args:
            duration (float, optional): The duration of the animation in seconds. Defaults to 1.
            angle (int, optional): The angle how much the handle is moved. PI*2 is one full rotation. Defaults to PI*2.

        Returns:
            manim.Rotate: Returns an animation object, that can be used with self.play().
        """

        return Rotate(
            self.line,
            angle=-angle,
            about_point=self.clock.get_center(),
            axis=Z_AXIS,
            rate_func=linear,
            run_time=duration,
        )


class CustomTitle(VGroup):
    """A Custom Title that already sets font_size and position. It can be used to create a title for a scene.
    Example Usage:

    title = CustomTitle(
            title_text="Pros and Cons of FCFS", corner=self.get_to_corner(UL)
    )

    self.play(FadeIn(title))
    """

    def __init__(self, title_text: str, corner: np.ndarray, **kwargs) -> Text:
        """The init method that takes in the title_text and the corner of the screen where the title should be placed.

        Args:
            title_text (str): The string that should be displayed as the title.
            corner (np.ndarray): The left upper corner of the screen where the title should be placed.

        Returns:
            Text: The title element ready to be Faded in.
        """
        super().__init__(**kwargs)
        self.title = Text(title_text, font_size=36)
        self.add(self.title)
        self.title.next_to(corner, DR)


class AnimatedTitle(Mobject):
    """
    How to call:

    class ExampleScene(Scene):
        def construct(self):
            title = AnimatedTitle("Your Title Here")
            self.play(title.create_animation())
    """

    def __init__(self, title_text, **kwargs):
        super().__init__(**kwargs)

        # Split the title text into words
        words = title_text.split()

        # Create the title with differently colored words
        self.title = VGroup()  # Group to hold the words
        for i, word in enumerate(words):
            color = WHITE if i == 0 else BLUE
            word_text = Text(word, color=color, font_size=65)
            self.title.add(word_text)

        # Arrange the words in a row
        self.title.arrange(RIGHT, buff=0.2)

        self.add(self.title)

    def create_animation(
        self, center: np.ndarray = None, corner: np.ndarray = None
    ) -> Succession:
        """This method creates an animation for the title to fade in, shrink and optionally move to the specified position.
        It allows to specify both the center and the corner of the frame for dynamically positioning of the title animation based on the current camera frame.

        Args:
            center (np.ndarray, optional): current center position of the camera. Defaults to None.
            corner (np.ndarray, optional): current left upper corner position of the camera. Defaults to None.

        Returns:
            Succession: Returns the full animation to reveal and move the title
        """

        shrink_and_move = (
            self.title.animate.scale(0.5)
            .to_edge(UP, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
            .to_edge(LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
        )

        if center is not None and corner is not None:
            self.title.move_to(center)
            shrink_and_move = self.title.animate.scale(0.5).next_to(corner, DR, buff=0)

        # run_time is needed because otherwise the animation breaks
        return Succession(
            FadeIn(self.title), Wait(1), shrink_and_move, Wait(1), run_time=4
        )


class AnimatedLabel(Mobject):
    """
    Reference component for positioning required.
    How to call:

    class ExampleScene(Scene):
        def construct(self):
            square = Square()
            self.play(Create(square))

            label = AnimatedLabel("Your label", reference=square, offset=UP)
            self.play(label.create_animation())
    """

    def __init__(
        self, label: str, reference: Mobject, offset=DOWN, font_size=24, **kwargs
    ):
        super().__init__(**kwargs)
        self.label = Text(label, font_size=font_size)

        if reference is not None:
            self.label.next_to(
                reference, offset, buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
            )
        self.add(self.label)

    def create_animation(self):
        return FadeIn(self.label)


class AnimatedReview(Mobject):
    """
    Always on the right side.
    How to call:

    class ExampleScene(Scene):
        def construct(self):
            positive = [
                "Just awesome",
                "Great service",
            ]
            neutral = ["Average speed"]
            negative = ["Not good"]
            animated_review = AnimatedReview(positive, neutral, negative)
            self.play(animated_review.create_animation())
    """

    def __init__(
        self,
        positive: List[str],
        neutral: List[str],
        negative: List[str],
        width=25,
        speed=0.05,
        override_speed=False,
        center: np.ndarray = None,
        left_edge: np.ndarray = None,
        horizontal: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Calculate lengths for animation runtimes
        self.speed = speed
        self.override_speed = override_speed
        self.lengths = [
            sum([len(item) for item in positive]) + len("Positive"),
            sum([len(item) for item in neutral]) + len("Neutral"),
            sum([len(item) for item in negative]) + len("Negative"),
        ]

        # Function to split text if it is too long
        def wrap_text(text, width):
            wrapped_text = ""
            words = text.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= width:
                    current_line += word + " "
                else:
                    wrapped_text += current_line + "\n"
                    current_line = word + " "
            wrapped_text += current_line
            return wrapped_text.strip()

        # Function to create a section with bullet points
        def create_section(label_text, items, color):
            if not items:
                return None
            label = Text(label_text, color=color).scale(0.5)
            bullets = VGroup()
            for item in items:
                wrapped_item = wrap_text(f"• {item}", width)
                bullet_text = Text(wrapped_item, color=WHITE).scale(0.5)
                bullets.add(bullet_text)
            bullets.arrange(DOWN, aligned_edge=LEFT).next_to(
                label, DOWN, aligned_edge=LEFT
            )
            return VGroup(label, bullets)

        # Create sections with specified colors
        self.positive_section = create_section("Positive", positive, GREEN)
        self.neutral_section = create_section("Neutral", neutral, BLUE)
        self.negative_section = create_section("Negative", negative, RED)

        # Add sections to the Mobject and arrange
        sections = filter(
            None, [self.positive_section, self.neutral_section, self.negative_section]
        )
        self.add(*sections)
        # Allow for horizontal or vertical arrangement
        if horizontal:
            self.arrange(RIGHT, aligned_edge=UP, buff=MED_LARGE_BUFF)
        else:
            self.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)

        if center is not None:
            self.move_to(center)
        elif left_edge is not None:
            self.next_to(left_edge, RIGHT)
        else:
            self.to_edge(RIGHT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)

    def create_animation(self, return_list: bool = False):
        def proportional_write(idx: int, mobject: Mobject):
            run_time = self.speed * self.lengths[idx]

            if self.override_speed:
                run_time = 1

            return Write(mobject, run_time=run_time)

        animations = []
        for idx, section in enumerate(self.submobjects):
            animations.append(proportional_write(idx, section))
            animations.append(Wait(1))

        if return_list:
            return animations

        return Succession(*animations)


class AnimatedBulletpoints(Mobject):
    """
    How it works:
    (1) Create a list of tuples with the text and the wait time for each bullet point.
    (2) Create an instance of AnimatedBulletpointsWait with the list of tuples.
    (3) Call create_animation() to get the animation object.

    class ExampleScene(Scene):
        def construct(self):
            points = [
                ("This is the first point", 1),
                ("Here is the second, longer point which might need wrapping", 2),
                ("Third point", 1)
            ]
            bulletpoints = AnimatedBulletpoints(points)
            self.play(bulletpoints.create_animation())
    """

    def __init__(
        self,
        bullet_points: List[Tuple[str, float]],
        width=25,
        speed=0.05,
        edge: np.ndarray = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.speed = speed
        self.length = sum(len(item) for item in bullet_points)
        self.wait_times = [waittime for item, waittime in bullet_points]

        # Function to split text if it is too long
        def wrap_text(text, width):
            wrapped_text = ""
            words = text.split()
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 <= width:
                    current_line += word + " "
                else:
                    wrapped_text += current_line + "\n"
                    current_line = word + " "
            wrapped_text += current_line
            return wrapped_text.strip()

        # Create bullet points
        self.bullets = VGroup()
        for item, waittime in bullet_points:
            wrapped_item = wrap_text(f"• {item}", width)
            bullet_text = Text(wrapped_item, color=WHITE).scale(0.5)
            self.bullets.add(bullet_text)

        self.bullets.arrange(DOWN, aligned_edge=LEFT)
        self.add(self.bullets)
        if edge is None:
            self.to_edge(RIGHT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
        else:
            self.next_to(edge, LEFT)

    def create_animation(self, return_list: bool = False):
        animations = []
        for idx, bullet in enumerate(self.bullets):
            run_time = self.speed * len(str(bullet.text))
            animations.append(Write(bullet, run_time=run_time))
            animations.append(Wait(self.wait_times[idx]))

        if return_list:
            return animations

        return Succession(*animations)


class MetricResponseTime(Mobject):
    def __init__(
        self,
        datasets: List[np.ndarray],
        titles: List[str],
        x_stepsize: int = 1_000,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.x_stepsize = x_stepsize

        if len(datasets) > 5:
            raise ValueError("MetricResponseTimeMobject only supports up to 5 datasets")
        if len(datasets) != len(titles):
            raise ValueError("Number of datasets must equal number of titles")

        colors = [BLUE, RED, GREEN, ORANGE, PURPLE]
        max_y_value = int(max(dataset.max() for dataset in datasets))
        min_y_value = int(min(dataset.min() for dataset in datasets))
        scaled_max_y_value = max_y_value * 1.05
        scaled_min_y_value = min_y_value * 0.95
        y_stepsize = (int(scaled_max_y_value - scaled_min_y_value)) // 6

        # Initialize axes with exactly 5 y-axis ticks and corresponding labels
        ax = Axes(
            x_range=[0, len(datasets[0]) * (self.x_stepsize + 1), self.x_stepsize],
            y_range=[
                scaled_min_y_value + 5,
                scaled_max_y_value - 5,
                y_stepsize,
            ],
            tips=True,
            axis_config={"include_numbers": True},
        )

        # Initialize labels
        x_label = Tex("Number of Processes").next_to(ax.x_axis, DOWN * 0.4).scale(0.7)
        y_label = (
            Tex("Average Turnaround Time (ms)")
            .next_to(ax.y_axis.get_left(), LEFT * 0)
            .rotate(90 * DEGREES)
            .scale(0.7)
        )
        y_label.shift(LEFT * 0.25)

        # Initialize legend
        legend_start = UP * 3
        legend_group = VGroup()
        for i, title in enumerate(titles):
            color = colors[i]
            label_line = Line(LEFT, RIGHT, color=color, stroke_width=4).scale(0.3)
            label_line.next_to(legend_start + DOWN * 0.25 * i, LEFT)

            text = Tex(title, font_size=24).next_to(label_line, RIGHT, buff=0.1)
            legend_group.add(label_line, text)

        # Initialize line graphs for all datasets
        self.first_dots = []
        self.line_graphs = []
        for i, dataset in enumerate(datasets):
            color = colors[i]
            line_graph = VMobject(color=color)
            first_point = ax.c2p(self.x_stepsize, dataset[0])
            line_graph.start_new_path(first_point)

            first_dot = Dot(first_point, color=color).scale(0.7)
            self.first_dots.append(first_dot)

            line_graph.add(first_dot)
            self.line_graphs.append(line_graph)
            self.add(line_graph)

        self.ax = ax
        self.x_label = x_label
        self.y_label = y_label
        self.legend_group = legend_group
        self.datasets = datasets
        self.colors = colors

        self.add(ax, x_label, y_label, legend_group)

    def _create_line_graph_animations(self):
        line_graph_animations = []
        last_points = [
            self.line_graphs[i].get_points()[-1] for i in range(len(self.datasets))
        ]

        for x in range(2, len(self.datasets[0]) + 1):
            frame_animations = []
            for i, dataset in enumerate(self.datasets):
                new_point = self.ax.c2p(x * self.x_stepsize, dataset[x - 1])
                dot = Dot(new_point, color=self.colors[i]).scale(0.7)

                last_point = last_points[i]
                new_line = Line(
                    last_point, new_point, color=self.colors[i], stroke_width=4
                )

                last_points[i] = new_point
                self.line_graphs[i].add(new_line)
                self.line_graphs[i].add(dot)

                frame_animations.append(Create(new_line))
                frame_animations.append(FadeIn(dot, scale=0.7))

            line_graph_animations.append(
                AnimationGroup(*frame_animations, run_time=0.5)
            )
            line_graph_animations.append(Wait(0.15))

        return line_graph_animations

    def create_animation(self):
        setup_animations = [
            Create(self.ax.y_axis, run_time=2),
            Wait(1),
            Create(self.ax.x_axis, run_time=2),
            Wait(1),
            Write(self.y_label, run_time=2),
            Wait(1),
            Write(self.x_label, run_time=2),
            Wait(1),
            FadeIn(self.legend_group, run_time=2),
            Wait(2),
        ]

        # Create a group animation for all first dots
        first_dot_animations = [
            FadeIn(dot, scale=0.7, run_time=2) for dot in self.first_dots
        ]
        setup_animations.append(AnimationGroup(*first_dot_animations))

        line_graph_animations = self._create_line_graph_animations()
        all_animations = setup_animations + line_graph_animations

        return Succession(*all_animations)


class MetricBarChart(VMobject):
    def __init__(self, datasets: List[float], titles: List[str], y_text: str, **kwargs):
        super().__init__(**kwargs)

        if len(datasets) > 5:
            raise ValueError("MetricBarChart only supports up to 5 datasets")
        if len(datasets) != len(titles):
            raise ValueError("Number of datasets must equal number of titles")

        colors = [BLUE, RED, GREEN, ORANGE, PURPLE]
        used_colors = colors[: len(datasets)]

        max_y_value = max(datasets)

        def round_up_to_nearest_five(n):
            return math.ceil(n / 5) * 5

        adjusted_max_y_value = round_up_to_nearest_five(max_y_value)
        tick_interval = round_up_to_nearest_five(adjusted_max_y_value / 5)

        self.chart = BarChart(
            values=datasets,
            bar_names=titles,
            y_range=[0, adjusted_max_y_value, tick_interval],
            y_length=6,
            x_length=10,
            x_axis_config={"font_size": 30},
            bar_colors=used_colors,
        )

        y_label = Text(y_text, font_size=24)
        y_label.rotate(PI / 2, about_point=y_label.get_center())
        y_label.next_to(self.chart.y_axis, LEFT)

        self.add(self.chart, y_label)

    def animate_bars(self, wait_time: float = 1):
        initial_heights = [bar.height for bar in self.chart.bars]
        animations = [Wait(wait_time)]

        for bar, init_height in zip(self.chart.bars, initial_heights):
            bar.stretch_to_fit_height(0.01, about_edge=DOWN)
            stretch_animation = bar.animate.stretch_to_fit_height(
                init_height, about_edge=DOWN
            )
            animations.append(stretch_animation)

        bar_grow_sequence = Succession(*animations, lag_ratio=1.0)
        return bar_grow_sequence


class AlgorithmAnimation:
    """Class used to create and Algorithm Animation for Roundrobin or FCFS. It stores processes in a queue and allows to run the Algorithm for one quantum at a time."""

    def __init__(self, quantum: int, type: str) -> None:
        self.quantum = quantum
        self.process_queue: List[ProcessAnimated] = []
        if type not in ["rr", "fcfs"]:
            raise ValueError("Algorithm type must be either rr or fcfs")
        self.type = type

    def get_current_length(self) -> int:
        length = 0
        for process in self.process_queue:
            length += process.size
        return length

    def get_empty(self) -> bool:
        return len(self.process_queue) == 0

    def add_process(self, process: ProcessAnimated):
        self.process_queue.append(process)

    def run(self) -> Tuple[bool, AnimationGroup | None]:
        """Runs the algorithm for one quantum and returns the animation or None if the queue is empty.
        It also returns if the current process finished or not

        Returns:
            Tuple[bool, AnimationGroup | None]: Returns True if the current process finished and False if not. The second value is the animation to be played or None if the queue is empty.
        """
        if len(self.process_queue) == 0:
            return (True, None)

        if self.type == "rr":
            return self._run_rr()

        return self._run_fcfs()

    def _run_fcfs(self) -> Tuple[bool, AnimationGroup | None]:
        current_process = self.process_queue[0]
        animation = current_process.adjust_size_with_animation(-1)

        if current_process.size == 0:
            self.process_queue.pop(0)
            return True, AnimationGroup(
                FadeOut(current_process), current_process.animate.scale(0.1)
            )

        return False, animation

    def _run_rr(self) -> Tuple[bool, AnimationGroup | None]:
        current_process = self.process_queue.pop(0)
        animation = current_process.adjust_size_with_animation(-1)
        if current_process.size > 0:
            self.process_queue.append(current_process)
            return False, animation

        return True, AnimationGroup(
            FadeOut(current_process), current_process.animate.scale(0.1)
        )

    def move_queue(
        self,
        pole_position: np.ndarray,
        first_process_in_cpu: bool = False,
        duration: int = 1,
    ) -> Succession | None:
        """Moves the queue of processes to the given pole position. If the first process is in the CPU, it will be ignored.

        Args:
            pole_position (np.ndarray): The position where the queue should be moved to.
            first_process_in_cpu (bool, optional): If the first process should be ignored due to it beeing in the cpu. Defaults to False.
            duration (int, optional): How long the animation should be in seconds. Defaults to 1.

        Returns:
            Succession | None: This is the Animation object that can be played. If the queue is empty, None will be returned.
        """
        # If the length of the queue isn't long enough to move, return None
        # This occurs when either the length of the queue is 0
        # or if the first process is in the CPU essentially beeing outside of the queue
        # and the length of the queue is 1 because the actual queue is empty
        if (
            first_process_in_cpu
            and len(self.process_queue) <= 1
            or len(self.process_queue) <= 0
        ):
            return None

        previous_process = ProcessAnimated()
        animations = []
        for i, process in enumerate(
            self.process_queue[1 if first_process_in_cpu else 0 :]
        ):
            if i == 0:
                animations.append(process.animate.move_to(pole_position))
                previous_process = process.copy().move_to(pole_position)
            else:
                animations.append(
                    process.animate.next_to(previous_process, LEFT, buff=0.5)
                )
                previous_process = process.copy().next_to(
                    previous_process, LEFT, buff=0.5
                )
        # if not animations:
        #     return None
        return Succession(*animations, run_time=duration)


class SequenceDiagram(Mobject):
    """
    How to use:
    class ExampleScene(Scene):
        def construct(self):
            steps = [
                {"id": 1, "start": 0, "size": 4},
                {"id": 2, "start": 4, "size": 2},
                {"id": 3, "start": 6, "size": 1},
                {"id": 4, "start": 7, "size": 5},
                {"id": 2, "start": 12, "size": 2},
                {"id": 3, "start": 14, "size": 2},
                {"id": 4, "start": 16, "size": 5},
                {"id": 3, "start": 21, "size": 3},
            ]
            sequence_diagram = SequenceDiagram("FCFS", steps=steps)
            self.play(sequence_diagram.create_animations())
    """

    def __init__(
        self, algorithm: str, steps: List[Dict], upper_left_corner: np.ndarray, **kwargs
    ):
        super().__init__(**kwargs)

        self.title = CustomTitle(
            f"Sequence Diagram for {algorithm}", corner=upper_left_corner
        )
        self.steps = steps
        self.processes = [
            f"P{id} - {size}s" for id, size in self.__calculate_process_sizes().items()
        ]

    def __calculate_process_sizes(self):
        size_sum = {}
        for step in self.steps:
            size_sum[step["id"]] = size_sum.get(step["id"], 0) + step["size"]

        sorted_size_sum = dict(sorted(size_sum.items()))
        return sorted_size_sum

    def __create_process_diagram(
        self,
        left_edge: np.ndarray,
        top_edge: np.ndarray,
        frame_width: float,
        frame_height: float,
    ):
        # Displaying the labels for the processes
        process_texts = [Text(process, font_size=24) for process in self.processes]
        process_objects = VGroup(*process_texts)

        total_vertical_space = (
            frame_height - (top_edge[1] - self.title.get_bottom()[1]) - 1
        )
        space_per_process = total_vertical_space / len(self.processes)
        reduced_buff = (space_per_process - process_texts[0].get_height()) * 0.9

        process_objects.arrange(DOWN, aligned_edge=LEFT, buff=reduced_buff)
        process_objects.next_to(left_edge, RIGHT)
        # Need to shift the Y_Axis center in order to prevent the diagram being positioned over the title
        process_objects.move_to(
            process_objects.get_center()
            + (top_edge[1] - self.title.get_bottom()[1]) * DOWN
        )

        # Displaying the separator lines
        separator_lines = VGroup()
        line_length = frame_width - 2
        for i, process in enumerate(process_texts[:-1]):
            line = DashedLine(LEFT * 0.5, RIGHT * 0.5, dash_length=0.005).set_length(
                line_length
            )

            next_process = process_texts[i + 1]
            midpoint_y = (process.get_bottom()[1] + next_process.get_top()[1]) / 2

            line_x_position = process.get_left()[0]

            line.move_to(midpoint_y * UP + line_x_position * RIGHT, aligned_edge=LEFT)
            separator_lines.add(line)

        # Calculate scaling factor for process bars so they match the full width

        rightmost_object_x_position = (
            separator_lines[-1].get_right()[0] - DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        )
        leftmost_object_x_position = process_texts[0].get_right()[0]
        available_space = rightmost_object_x_position - leftmost_object_x_position
        total_size = sum(step["size"] / 2 for step in self.steps)
        scaling_factor = available_space / total_size if total_size != 0 else 1

        bars = []
        process = None
        for step in self.steps:
            process = self.create_processes(
                step["id"],
                step["size"] * scaling_factor,
                process_texts,
                process,
            )
            bars.append(process)

        return VGroup(process_objects, separator_lines, *bars)

    def create_processes(
        self,
        process_lane: int,
        size: int,
        process_texts,
        previous_process,
        process_color=ORANGE,
    ):
        lane_y_position = process_texts[process_lane - 1].get_center()[1]

        # y-axis positioning
        process_bar = ProcessAnimated(color=process_color, size=size, show_size=False)
        process_bar.move_to(lane_y_position * UP)

        # x-axis positioning
        if not previous_process:
            process_bar.next_to(
                process_texts[process_lane - 1],
                RIGHT,
                buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
            )
        else:
            new_x_position = previous_process.get_right()[0] + process_bar.width / 2
            process_bar.move_to(new_x_position * RIGHT + lane_y_position * UP)

        return process_bar

    def create_animations(
        self,
        left_edge: np.ndarray,
        top_edge: np.ndarray,
        frame_width: float,
        frame_height: float,
    ) -> Succession:
        process_diagram = self.__create_process_diagram(
            left_edge=left_edge,
            top_edge=top_edge,
            frame_width=frame_width,
            frame_height=frame_height,
        )
        process_texts = process_diagram[0]
        separator_lines = process_diagram[1]
        process_bars = process_diagram[2:]

        write_animations = [Write(text) for text in process_texts]

        line_animations = [GrowFromPoint(line, left_edge) for line in separator_lines]

        bar_animations = []
        for bar in process_bars:
            bar_animations.append(GrowFromEdge(bar, LEFT))
            bar_animations.append(Wait(0.5))

        line_animation_group = AnimationGroup(*line_animations, lag_ratio=0)

        process_text_animation = Succession(*write_animations)
        bar_animation_sequence = Succession(*bar_animations)

        return Succession(
            FadeIn(self.title),
            process_text_animation,
            line_animation_group,
            bar_animation_sequence,
        )
