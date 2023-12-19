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
    def __init__(self, color=WHITE, size=1, title="", use_square=False, show_size=True, **kwargs):
        super().__init__(**kwargs)
        self.color = color
        self.size = size
        self.title = title
        self.use_square = use_square
        
        if show_size:
            title_text = f"{self.title}, {size}"
        else:
            title_text = self.title

        if self.use_square:
            square_size = 0.5 + 0.25 * max(0, size - 1)
            self.shape = Square(side_length=square_size).set_fill(self.color, opacity=1).set_stroke(self.color)
        else:
            self.shape = Rectangle(width=size/2, height=0.5).set_fill(self.color, opacity=1).set_stroke(self.color)
        
        self.title_text = Text(title_text, font_size=24).next_to(self.shape, UP)
        self.add(self.shape, self.title_text)

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
    def __init__(self, title: str = "", color=WHITE, size: float = 1, show_gear: bool = True, gear_pos=UR, **kwargs) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.color = color
        self.size = size
        self.show_gear = show_gear
        self.gear_pos = gear_pos
        self.create_cpu()
        if self.show_gear:
            self.add_gear()

    def create_cpu(self) -> None:
        self.cpu = SVGMobject("img/cpu.svg", fill_color=self.color).scale(self.size)
        title = Text(self.title, font_size=24).next_to(self.cpu, UP)
        self.add(self.cpu, title)

    def add_gear(self) -> None:
        self.gear = SVGMobject("img/gear.svg", fill_color=self.color).scale(0.25*self.size)
        self.gear.next_to(self.cpu, self.gear_pos, buff=-0.4)  
        self.add(self.gear)

    def rotate_gear(self, speed=1, duration=None, angle=None):
        if duration is not None:
            angle = TAU * speed/4 * duration
        elif angle is not None:
            pass
        return Rotate(self.gear, angle=angle, about_point=self.gear.get_center(), rate_func=linear, run_time=duration)


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
