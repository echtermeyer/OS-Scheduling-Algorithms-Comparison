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


def MetricResponseTime(self, datasets: List[np.ndarray], titles: List[str]):
    if len(datasets) > 5:
        raise ValueError("LineChart only supports up to 5 datasets")
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
    x_label = Tex("Number of Processes").next_to(ax.x_axis, DOWN * 0.4).scale(0.7)
    y_label = (
        Tex("Average Response Time")
        .next_to(ax.y_axis.get_left(), LEFT * 0)
        .rotate(90 * DEGREES)
        .scale(0.7)
    )
    self.play(Create(ax.x_axis), Create(ax.y_axis), Write(x_label), Write(y_label))
    self.wait(1)

    # Initialize legend
    legend_start = UP * 3
    legend_group = VGroup()
    for i, title in enumerate(titles):
        color = colors[i]
        label_line = Line(LEFT, RIGHT, color=color, stroke_width=4).scale(
            0.3
        )  # Shorter line
        label_line.next_to(legend_start + DOWN * 0.25 * i, LEFT)  # Vertical stacking

        text = Tex(title, font_size=24).next_to(
            label_line, RIGHT, buff=0.1
        )  # Smaller font size
        legend_group.add(label_line, text)
    self.play(FadeIn(legend_group))
    self.wait(1)

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

    # Create the animation for all datasets simultaneously
    for x in range(2, len(datasets[0]) + 1):
        animations = []
        for i, dataset in enumerate(datasets):
            new_point = ax.c2p(x, dataset[x - 1])
            dot = Dot(new_point, color=colors[i]).scale(0.7)
            new_line = Line(
                line_graphs[i].get_last_point(),
                new_point,
                color=colors[i],
                stroke_width=4,
            )
            line_graphs[i].add_line_to(new_point)
            animations.extend([Create(new_line), FadeIn(dot, scale=0.7)])

        self.play(*animations, run_time=1)
        self.wait(0.5)


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
            sum([len(item) for item in negative]) + len("Negative")
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
