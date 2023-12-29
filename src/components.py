import manim
from manim import *


class Process(VGroup):
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

    def adjust_size_with_animation(self, delta: int = -1) -> AnimationGroup:
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
                    self.shape.copy().stretch_to_fit_width(self.size / 2)
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
        alignment: str = "center",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.color = color
        self.size = size
        self.show_gear = show_gear
        self.gear_pos = gear_pos
        self.create_cpu(alignment)
        if self.show_gear:
            self.add_gear()

    def create_cpu(self, alignment) -> None:
        self.cpu = SVGMobject("img/cpu.svg", fill_color=self.color).scale(self.size)
        self.title_object = Paragraph(
            self.title, font_size=24, alignment=alignment
        ).next_to(self.cpu, UP)
        self.add(self.cpu, self.title_object)

    def add_gear(self) -> None:
        self.gear = SVGMobject("img/gear.svg", fill_color=self.color).scale(
            0.25 * self.size
        )
        self.gear.next_to(self.cpu, self.gear_pos, buff=-0.4)
        self.add(self.gear)

    def rotate_gear(self, speed=1, duration=None, angle=None):
        if duration is not None:
            angle = TAU * speed / 4 * duration
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

    def rotate(self, duration: float = 1, angle: int = PI * 2) -> manim.Rotate:
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

    def create_animation(self):
        fade_in = FadeIn(self.title)
        shrink_and_move = (
            self.title.animate.scale(0.5)
            .to_edge(UP, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
            .to_edge(LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
        )
        # run_time is needed because otherwise the animation breaks
        return Succession(fade_in, Wait(1), shrink_and_move, Wait(1), run_time=4)


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
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Calculate lengths for animation runtimes
        self.speed = speed
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
        self.arrange(DOWN, aligned_edge=LEFT, buff=MED_LARGE_BUFF)
        self.to_edge(RIGHT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)

    def create_animation(self):
        def proportional_write(idx: int, mobject: Mobject):
            run_time = self.speed * self.lengths[idx]
            return Write(mobject, run_time=run_time)

        animations = []
        for idx, section in enumerate(self.submobjects):
            animations.append(proportional_write(idx, section))
            animations.append(Wait(1))

        return Succession(*animations)


class AnimatedBulletpoints(Mobject):
    """
    How it works:

    class ExampleScene(Scene):
        def construct(self):
            points = [
                "This is the first point",
                "Here is the second, longer point which might need wrapping",
                "Third point",
            ]
            bulletpoints = AnimatedBulletpoints(points)
            self.play(bulletpoints.create_animation())
    """

    def __init__(self, bullet_points: List[str], width=25, speed=0.05, **kwargs):
        super().__init__(**kwargs)

        self.speed = speed
        self.length = sum(len(item) for item in bullet_points)

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
        for item in bullet_points:
            wrapped_item = wrap_text(f"• {item}", width)
            bullet_text = Text(wrapped_item, color=WHITE).scale(0.5)
            self.bullets.add(bullet_text)

        self.bullets.arrange(DOWN, aligned_edge=LEFT)
        self.add(self.bullets)
        self.to_edge(RIGHT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)

    def create_animation(self):
        animations = []
        for bullet in self.bullets:
            run_time = self.speed * len(bullet.text)
            animations.append(Write(bullet, run_time=run_time))
            animations.append(Wait(1))

        return Succession(*animations)


class MetricResponseTime(Mobject):
    def __init__(self, datasets: List[np.ndarray], titles: List[str], **kwargs):
        super().__init__(**kwargs)

        if len(datasets) > 5:
            raise ValueError("MetricResponseTimeMobject only supports up to 5 datasets")
        if len(datasets) != len(titles):
            raise ValueError("Number of datasets must equal number of titles")

        colors = [BLUE, RED, GREEN, ORANGE, PURPLE]
        max_y_value = max(dataset.max() for dataset in datasets)

        # Initialize axes
        ax = Axes(
            x_range=[0, len(datasets[0]) + 1],
            y_range=[0, max_y_value + 3],
            x_axis_config={
                "numbers_to_include": np.arange(0, len(datasets[0]) + 1, 2),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, max_y_value + 1, 2),
            },
            tips=True,
        )

        # Initialize labels
        x_label = Tex("Number of Processes").next_to(ax.x_axis, DOWN * 0.4).scale(0.7)
        y_label = (
            Tex("Average Response Time")
            .next_to(ax.y_axis.get_left(), LEFT * 0)
            .rotate(90 * DEGREES)
            .scale(0.7)
        )

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
            first_point = ax.c2p(1, dataset[0])
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
                new_point = self.ax.c2p(x, dataset[x - 1])
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

            line_graph_animations.append(AnimationGroup(*frame_animations, run_time=1))
            line_graph_animations.append(Wait(0.25))

        return line_graph_animations

    def create_animation(self):
        setup_animations = [
            Create(self.ax.x_axis, run_time=2),
            Wait(1),
            Create(self.ax.y_axis, run_time=2),
            Wait(1),
            Write(self.x_label, run_time=2),
            Wait(1),
            Write(self.y_label, run_time=2),
            Wait(1),
            FadeIn(self.legend_group, run_time=2),
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

        self.chart = BarChart(
            values=datasets,
            bar_names=titles,
            y_range=[0, max_y_value + 2, 2],
            y_length=6,
            x_length=10,
            x_axis_config={"font_size": 30},
            bar_colors=used_colors,
        )

        y_label = Text(y_text, font_size=24)
        y_label.rotate(PI / 2, about_point=y_label.get_center())
        y_label.next_to(self.chart.y_axis, LEFT)

        self.add(self.chart, y_label)

    def animate_bars(self):
        initial_heights = [bar.height for bar in self.chart.bars]
        animations = []

        for bar, init_height in zip(self.chart.bars, initial_heights):
            bar.stretch_to_fit_height(0.01, about_edge=DOWN)
            stretch_animation = bar.animate.stretch_to_fit_height(
                init_height, about_edge=DOWN
            )
            animations.append(stretch_animation)

        bar_grow_sequence = Succession(*animations, lag_ratio=1.0)
        return bar_grow_sequence
