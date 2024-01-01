from manim import *
from src.components import *


class OS(Scene):
    def construct(self):
        # creative introduction
        # 2 min
        self.introduction()
        # 2 min
        self.fcfs()
        # In der ÜBerleitung Preemptive verwenden und erklären was das bedeutet
        # 3 min
        self.rr()
        # 3 min
        self.mqs()
        # 3 min
        self.metrics()
        # reallife examples
        # 2 min
        self.outro()

    def introduction(self):
        pass

    def fcfs(self):
        # Your code: ...

        # After animation of algorithm (at the moment just dummy data)
        self.clear()
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
        self.wait(2)
        self.clear()

    def rr(self):
        self.next_section(skip_animations=True)
        self.next_section()

        # create and animate title for RoundRobin
        title = AnimatedTitle("RoundRobin")
        self.play(title.create_animation())

        # create and animate CPU
        cpu = CPU(show_gear=True, title="CPU")

        # Define all the points around the clock for later use
        faktor = 1.5

        CPU_TOP: np.ndarray = np.array(cpu.get_top() + UP * faktor)
        CPU_BOTTOM = np.array(cpu.get_bottom() + DOWN * faktor)
        CPU_RIGHT = np.array(cpu.get_right() + RIGHT * faktor)
        CPU_LEFT = np.array(cpu.get_left() + LEFT * faktor)

        CPU_RIGHT_UPPER_CORNER = np.array(
            (CPU_RIGHT * X_AXIS + CPU_TOP * Y_AXIS) * 0.75
        )
        CPU_LEFT_UPPER_CORNER = np.array((CPU_LEFT * X_AXIS + CPU_TOP * Y_AXIS) * 0.75)
        CPU_LEFT_LOWER_CORNER = np.array(
            (CPU_LEFT * X_AXIS + CPU_BOTTOM * Y_AXIS) * 0.75
        )

        # save where the process to be executed next moves (right to the cpu at the bottom edge)
        PROCESS_POLE_POSITION = Process().move_to(CPU_RIGHT).to_edge(DOWN).get_center()

        self.play(FadeIn(cpu))
        self.wait(2)

        # initialize the RoundRobin object
        quantum = 1
        rr = RoundRobinAnimation(quantum)

        # Define all processes with it's lenghts
        process_sizes = [2, 3, 5, 1, 1, 2]

        # create processes and place them just outside the left edge
        for i, size in enumerate(process_sizes):
            process = (
                Process(title=f"P{i+1}", size=size)
                .to_edge(LEFT)
                .to_edge(DOWN)
                .shift(LEFT * 2)
            )
            rr.add_process(process)

        # animate processes into cpu queue position
        self.play(
            rr.move_queue(
                pole_position=PROCESS_POLE_POSITION,
                first_process_in_cpu=False,
                duration=5,
            )
        )

        # create and animate clock
        clock = Clock(radius=0.75)

        clock.to_edge(RIGHT).to_edge(UP)
        self.play(FadeIn(clock))

        # animate the process of RoundRobin
        while not rr.get_empty():
            # calculate the arc from current process next to cpu
            arc_to_cpu = ArcBetweenPoints(
                rr.process_queue[0].get_center(), CPU_RIGHT, angle=TAU / 4
            )
            # move current process next to cpu
            self.play(MoveAlongPath(rr.process_queue[0], arc_to_cpu))

            # animate queue
            animation = rr.move_queue(
                pole_position=PROCESS_POLE_POSITION,
                first_process_in_cpu=True,
                duration=1,
            )
            # the animation might return
            if animation is not None:
                self.play(animation)

            # process
            process_finished, animation = rr.run()
            self.play(AnimationGroup(animation, clock.rotate(), cpu.rotate_gear()))

            if not process_finished:
                end_point = PROCESS_POLE_POSITION

                if not len(rr.process_queue) <= 1:
                    end_point = (
                        rr.process_queue[-1]
                        .copy()
                        .next_to(rr.process_queue[-2], LEFT, buff=0.5)
                        .get_center()
                    )

                if end_point[0] > CPU_LEFT[0]:
                    control_point = CPU_LEFT_LOWER_CORNER
                else:
                    control_point = end_point + UP * 2

                points = [
                    CPU_RIGHT,
                    CPU_RIGHT_UPPER_CORNER,
                    CPU_TOP,
                    CPU_LEFT_UPPER_CORNER,
                    CPU_LEFT,
                    control_point,
                    end_point,
                ]
                path = VMobject().set_points_as_corners(points).make_smooth()  # type: ignore

                self.play(MoveAlongPath(rr.process_queue[-1], path), run_time=2)

        self.wait(2)

        # After animation of algorithm (at the moment just dummy data)
        self.clear()
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
        sequence_diagram = SequenceDiagram("RoundRobin", steps=steps)
        self.play(sequence_diagram.create_animations())
        self.wait(2)
        self.clear()

    def mqs(self):
        # Your code: ...

        # After animation of algorithm (at the moment just dummy data)
        self.clear()
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
        sequence_diagram = SequenceDiagram("MQS", steps=steps)
        self.play(sequence_diagram.create_animations())
        self.wait(2)
        self.clear()

    def metrics(self):
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
        self.wait(2)
        self.clear()

    def outro(self):
        pass
