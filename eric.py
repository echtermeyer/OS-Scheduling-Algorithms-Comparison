import numpy as np

np.random.seed(0)

from manim import *
from typing import List

from src.components import *
from src.algorithms import schedule_processes, FirstComeFirstServe, RoundRobin, MultiLevelQueue


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
        process_1 = ProcessAnimated(arrival_time=1, burst_time=5)
        process_2 = ProcessAnimated(arrival_time=2, burst_time=3)
        process_3 = ProcessAnimated(arrival_time=3, burst_time=3)
        process_4 = ProcessAnimated(arrival_time=4, burst_time=1)
        process_5 = ProcessAnimated(arrival_time=5, burst_time=4)
        process_6 = ProcessAnimated(arrival_time=6, burst_time=1)
        process_7 = ProcessAnimated(arrival_time=7, burst_time=4)

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


class Comparison(Scene):
    def construct(self):
        # Title page
        title = AnimatedTitle("Comparing Scheduling Algorithms")
        self.play(title.create_animation())
        self.play(title.animate.to_corner(UP + LEFT))

        # 2D LineChart metric
        datasets = [
            np.array([10, 12, 13, 7, 9, 10]),
            np.array([11, 12, 5, 15, 14, 12]),
            np.array([12, 13, 12, 10, 11, 13]),
        ]
        titles = ["FCFS", "RoundRobin", "MLQ"]
        metric_response_time = MetricResponseTime(datasets, titles).scale(0.9)
        self.play(metric_response_time.create_animation())
        self.play(metric_response_time.animate.scale(0.6).to_edge(LEFT))

        # 2D LineChart bullet points
        points = [
            "FCFS has the worst average response time",
            "Round Robin has the lowest average response time",
            "MLQ combines FCFS and Round Robin resulting in a middle ground",
        ]
        bulletpoints = AnimatedBulletpoints(points, width=40)
        self.play(bulletpoints.create_animation())
        self.play(FadeOut(bulletpoints))

        # 1st BarChart metric
        first_bar_chart = MetricBarChart(
            datasets=[5, 7, 3],
            titles=["FCFS", "SJF", "RR"],
            y_text="Turnaround Time",
        )
        first_bar_chart.scale(0.5).to_corner(
            UP + RIGHT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER
        )
        self.add(first_bar_chart)
        bar_grow_sequence = first_bar_chart.animate_bars()
        self.play(bar_grow_sequence)

        # 2nd BarChart metric
        second_bar_chart = MetricBarChart(
            datasets=[12, 5, 3],
            titles=["FCFS", "SJF", "RR"],
            y_text="Throughput",
        )
        second_bar_chart.scale(0.5).to_corner(
            DOWN + RIGHT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER
        )
        self.add(second_bar_chart)
        bar_grow_sequence = second_bar_chart.animate_bars()
        self.play(bar_grow_sequence)

        # Fade out the MetricResponseTime
        self.play(FadeOut(metric_response_time))

        # Move BarCharts to the left
        bar_charts_group = VGroup(first_bar_chart, second_bar_chart)
        self.play(
            bar_charts_group.animate.scale(0.8).to_edge(
                LEFT, buff=3 * DEFAULT_MOBJECT_TO_EDGE_BUFFER
            )
        )

        # BarChart metrics
        points = [
            "FCFS excels in average waiting time",
            "FCFS has the worst average response time",
            "Round Robin has the lowest average response time",
            "MLQ has very low average waiting time",
            "All algorithms have the same average turnaround time",
        ]
        bulletpoints = AnimatedBulletpoints(points, width=40)
        self.play(bulletpoints.create_animation())


class ExampleScene(Scene):
    def construct(self):
        fcfs = MultiLevelQueue(quantum=1)
        steps = schedule_processes(fcfs)

        sequence_diagram = SequenceDiagram("FCFS", steps=steps)
        self.play(sequence_diagram.create_animations())


# manim -pql script_name.py FCFS
