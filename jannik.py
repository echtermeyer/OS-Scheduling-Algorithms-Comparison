from manim import *


from src.components import *
from typing import Tuple
from manim.typing import *


# class RR(Scene):  #
#     def construct(self):
#         # Einführungstext
#         title = Text("Round Robin Scheduling").scale(0.9)
#         self.play(Write(title))
#         self.wait(1)
#         self.play(FadeOut(title))

#         # Beschreibung des Round Robin Schedulings
#         description1 = Text(
#             "Round Robin ist ein präemptives Scheduling-Verfahren."
#         ).scale(0.6)
#         description2 = Text(
#             "Jeder Prozess erhält eine feste Zeitscheibe (Quantum)."
#         ).scale(0.6)
#         description3 = Text(
#             "Prozesse werden in einer zyklischen Reihenfolge ausgeführt."
#         ).scale(0.6)
#         description1.shift(UP)
#         description3.shift(DOWN)

#         # Anzeige der Beschreibung
#         self.play(Write(description1))
#         self.wait(1)
#         self.play(Write(description2))
#         self.wait(1)
#         self.play(Write(description3))
#         self.wait(2)

#         # Verblassen und Szene beenden
#         self.play(FadeOut(description1), FadeOut(description2), FadeOut(description3))
#         self.wait(1)


class RR(Scene):
    def construct(self):
        self.next_section(skip_animations=True)
        # create and animate title for RoundRobin
        title = AnimatedTitle("RoundRobin")
        self.play(title.create_animation())

        # create and animate CPU
        cpu = CPU(color=RED, show_gear=True, title="CPU")

        # Define all the points around the clock for later use
        faktor = 1.5

        cpu_top: np.ndarray = np.array(cpu.get_top() + UP * faktor)
        cpu_bottom = np.array(cpu.get_bottom() + DOWN * faktor)
        cpu_right = np.array(cpu.get_right() + RIGHT * faktor)
        cpu_left = np.array(cpu.get_left() + LEFT * faktor)

        cpu_right_upper_corner = np.array(
            (cpu_right * X_AXIS + cpu_top * Y_AXIS) * 0.75
        )
        cpu_left_upper_corner = np.array((cpu_left * X_AXIS + cpu_top * Y_AXIS) * 0.75)
        cpu_left_lower_corner = np.array(
            (cpu_left * X_AXIS + cpu_bottom * Y_AXIS) * 0.75
        )

        self.play(FadeIn(cpu))
        self.wait(2)

        # initialize the RoundRobin object
        quantum = 1
        rr = RoundRobinAnimation(quantum)
        # save where the process to be executed next moves (right to the cpu at the bottom edge)
        PROCESS_POLE_POSITION = Process().move_to(cpu_right).to_edge(DOWN).get_center()

        # Define all processes with it's lenghts
        process_sizes = [2,3]
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

        # Animate the process of RoundRobin
        self.next_section()
        while not rr.get_empty():
            arc_to_cpu = ArcBetweenPoints(
                rr.process_queue[0].get_center(), cpu_right, angle=TAU / 4
            )

            self.play(MoveAlongPath(rr.process_queue[0], arc_to_cpu))

            # animate queue
            animation = rr.move_queue(
                pole_position=PROCESS_POLE_POSITION,
                first_process_in_cpu=True,
                duration=1,
            )

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

                if end_point[0] > cpu_left[0]:
                    control_point = cpu_left_lower_corner
                else:
                    control_point = end_point + UP * 2

                points = [
                    cpu_right,
                    cpu_right_upper_corner,
                    cpu_top,
                    cpu_left_upper_corner,
                    cpu_left,
                    control_point,
                    end_point,
                ]
                path = VMobject().set_points_as_corners(points).make_smooth()  # type: ignore

                self.play(MoveAlongPath(rr.process_queue[-1], path), run_time=2)

        self.wait(1)


class RoundRobinAnimation:
    def __init__(self, quantum: int) -> None:
        self.quantum = quantum
        self.process_queue: List[Process] = []

    def get_current_length(self) -> int:
        length = 0
        for process in self.process_queue:
            length += process.size
        return length

    def get_empty(self) -> bool:
        return len(self.process_queue) == 0

    def add_process(self, process: Process):
        self.process_queue.append(process)

    def run(self) -> Tuple[bool, AnimationGroup | None]:
        if len(self.process_queue) == 0:
            return (True, None)
        current_process = self.process_queue.pop(0)
        animation = current_process.adjust_size_with_animation(-1)
        if current_process.size > 0:
            self.process_queue.append(current_process)
            return False, animation

        else:
            return True, AnimationGroup(
                FadeOut(current_process), current_process.animate.scale(0.1)
            )

    def move_queue(
        self,
        pole_position,
        first_process_in_cpu=False,
        duration=1,
    ) -> Succession | None:
        previous_process = Process()

        if first_process_in_cpu:
            if len(self.process_queue) <= 1:
                return None
        else:
            if len(self.process_queue) <= 0:
                return None

        # length = (
        #     len(self.process_queue)
        #     if first_process_in_cpu
        #     else  - 1
        # )
        # if length <= 0:
        #     return None

        animations = []
        for i, process in enumerate(
            self.process_queue[1 if first_process_in_cpu else 0 :]
        ):
            if i == 0:
                animations.append(process.animate.move_to(pole_position))
                previous_process = process.copy().move_to(pole_position)
            else:
                animations.append(
                    process.animate.next_to(previous_process, LEFT, buff=0.5)
                )
                previous_process = process.copy().next_to(
                    previous_process, LEFT, buff=0.5
                )
        # if not animations:
        #     return None
        return Succession(*animations, run_time=duration)


# class ExampleScene(Scene):
#     def construct(self):
#         datasets = [np.array([1, 2, 3, 4]), np.array([4, 3, 2, 1])]
#         titles = ["Dataset 1", "Dataset 2"]
#         metric_response_time = MetricResponseTime(datasets, titles)
#         self.play(metric_response_time.create_animation())
