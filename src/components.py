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
