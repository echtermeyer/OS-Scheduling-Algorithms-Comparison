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

        self.wait(1)
