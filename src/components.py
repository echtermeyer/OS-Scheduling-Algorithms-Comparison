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
