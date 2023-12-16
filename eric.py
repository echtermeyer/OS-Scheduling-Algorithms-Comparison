from manim import *

from src.components import CPU, Process


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
        process_6 = Process(arrival_time=6, burst_time=1)
        process_7 = Process(arrival_time=7, burst_time=4)

        # Group the processes and position them
        processes = VGroup(
            process_7, process_6, process_5, process_4, process_3, process_2, process_1
        ).arrange(RIGHT, buff=0.25)
        processes.to_edge(3 * LEFT)
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
            animations.append(
                AnimationGroup(move_animation, update_animation, lag_ratio=0)
            )

        # Play all animations simultaneously
        self.play(*animations)


# To run this, use:
# manim -pql script_name.py FCFS
