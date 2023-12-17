from manim import *


class Process(VGroup):
    def __init__(self, arrival_time: int, burst_time: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.arrival_time = arrival_time
        self.burst_time = burst_time

        self.create_process()

    def create_process(self) -> None:
        base_width = 0.5
        height = 0.5

        process_rect = Rectangle(
            width=self.burst_time * base_width, height=height, color=WHITE
        )
        process_rect.set_fill(WHITE, opacity=1)

        process_info = f"({self.arrival_time}, {self.burst_time})"
        process_text = Text(process_info, font_size=24).next_to(process_rect, UP)

        self.add(process_rect, process_text)


class CPU(VGroup):
    def __init__(self, title: str = "", **kwargs) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.create_cpu()

    def create_cpu(self) -> None:
        cpu = Square(side_length=3, color=WHITE)
        cpu.set_fill(WHITE, opacity=1)

        title = Text(self.title, font_size=24).next_to(cpu, UP)

        self.add(cpu, title)


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
        self.title = Text(title_text, font_size=65)
        self.add(self.title)

    def create_animation(self):
        fade_in = FadeIn(self.title)
        shrink_and_move = (
            self.title.animate.scale(0.5)
            .to_edge(UP, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
            .to_edge(LEFT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER)
        )
        return Succession(fade_in, Wait(1), shrink_and_move, Wait(1))


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


class MetricResponseTimeMobject(Mobject):
    """
    How to call:

    class ExampleScene(Scene):
        def construct(self):
            datasets = [
                np.array([1, 2, 3, 4]),
                np.array([4, 3, 2, 1])
            ]
            titles = ["Dataset 1", "Dataset 2"]
            metric_response_time = MetricResponseTimeMobject(datasets, titles)
            self.play(metric_response_time.create_animation())
    """

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
            y_range=[0, max_y_value + 1],
            x_axis_config={
                "numbers_to_include": np.arange(0, len(datasets[0]) + 1, 2),
                "numbers_with_elongated_ticks": np.arange(0, len(datasets[0]) + 1, 2),
            },
            y_axis_config={
                "numbers_to_include": np.arange(0, max_y_value + 1, 2),
                "numbers_with_elongated_ticks": np.arange(0, max_y_value + 1, 2),
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
        line_graphs = []
        for i, dataset in enumerate(datasets):
            color = colors[i]
            line_graph = VMobject(color=color)
            first_point = ax.c2p(1, dataset[0])
            line_graph.start_new_path(first_point)
            line_graphs.append(line_graph)
            first_dot = Dot(first_point, color=color).scale(0.7)
            self.add(first_dot)

        # Store axes, labels, legend, and line graphs as attributes
        self.ax = ax
        self.x_label = x_label
        self.y_label = y_label
        self.legend_group = legend_group
        self.line_graphs = line_graphs
        self.datasets = datasets
        self.colors = colors

        # Add axes, labels, and legend to the Mobject
        self.add(ax, x_label, y_label, legend_group)

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
        line_graph_animations = self._create_line_graph_animations()
        return Succession(*setup_animations, *line_graph_animations)

    def _create_line_graph_animations(self):
        line_graph_animations = []
        for x in range(2, len(self.datasets[0]) + 1):
            frame_animations = []
            for i, dataset in enumerate(self.datasets):
                new_point = self.ax.c2p(x, dataset[x - 1])
                dot = Dot(new_point, color=self.colors[i]).scale(0.7)
                new_line = Line(
                    self.line_graphs[i].get_last_point(),
                    new_point,
                    color=self.colors[i],
                    stroke_width=4,
                )
                self.line_graphs[i].add_line_to(new_point)
                frame_animations.extend([Create(new_line), FadeIn(dot, scale=0.7)])
            line_graph_animations.append(AnimationGroup(*frame_animations, run_time=1))
            line_graph_animations.append(Wait(0.25))
        return line_graph_animations
