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


class FCFS(Scene):
    def construct(self):
        # Show dashed seperator line
        x_coordinate = 3 / 4 * config.frame_width - config.frame_width / 2
        dashed_line = DashedLine(
            start=UP * config.frame_height / 2,
            end=DOWN * config.frame_height / 2,
            color=WHITE,
        ).move_to(x_coordinate * RIGHT)
        self.add(dashed_line)

        # Show CPU next to dashed line
        cpu = CPU(title="CPU")
        right_edge_x = config.frame_width / 2
        cpu_x_position = (x_coordinate + right_edge_x) / 2
        cpu.move_to(cpu_x_position * RIGHT)
        self.add(cpu)

        # Show processes
        process_1 = Process(arrival_time=1, burst_time=5)
        process_2 = Process(arrival_time=2, burst_time=3)
        process_3 = Process(arrival_time=3, burst_time=3)
        process_4 = Process(arrival_time=4, burst_time=1)
        process_5 = Process(arrival_time=5, burst_time=4)

        # Group the processes and position them
        processes = VGroup(process_1, process_2, process_3, process_4, process_5).arrange(RIGHT, buff=0.25)
        processes.to_edge(LEFT)
        self.add(processes)

        # Position of the left edge of the CPU
        cpu_left_edge = cpu.get_left()[0]

        # Determine uniform speed
        uniform_speed = 1

        animations = []

        for process in processes:
            process.target = process.copy().move_to(cpu.get_center())
            distance = np.linalg.norm(process.get_center() - cpu.get_center())
            run_time = distance / uniform_speed

            # Create an animation that dynamically reduces process width
            def make_update_process(process):
                def update_process(mob):
                    if mob.get_right()[0] > cpu_left_edge:
                        new_width = cpu_left_edge - mob.get_left()[0]
                        if new_width <= 0:
                            self.remove(mob)
                return update_process

            update_animation = UpdateFromFunc(process, make_update_process(process))
            move_animation = MoveToTarget(process, rate_func=linear, run_time=run_time)
            animations.append(AnimationGroup(move_animation, update_animation, lag_ratio=0))

        # Play all animations simultaneously
        self.play(*animations)


# To run this, use:
# manim -pql script_name.py FCFS
