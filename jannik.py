from manim import *


class RR(Scene):  #
    def construct(self):
        # Einführungstext
        title = Text("Round Robin Scheduling").scale(0.9)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Beschreibung des Round Robin Schedulings
        description1 = Text(
            "Round Robin ist ein präemptives Scheduling-Verfahren."
        ).scale(0.6)
        description2 = Text(
            "Jeder Prozess erhält eine feste Zeitscheibe (Quantum)."
        ).scale(0.6)
        description3 = Text(
            "Prozesse werden in einer zyklischen Reihenfolge ausgeführt."
        ).scale(0.6)
        description1.shift(UP)
        description3.shift(DOWN)

        # Anzeige der Beschreibung
        self.play(Write(description1))
        self.wait(1)
        self.play(Write(description2))
        self.wait(1)
        self.play(Write(description3))
        self.wait(2)

        # Verblassen und Szene beenden
        self.play(FadeOut(description1), FadeOut(description2), FadeOut(description3))
        self.wait(1)


class CompactCircleScene(Scene):
    def construct(self):
        cpu = SVGMobject("img/cpu.svg", fill_color=WHITE, color=WHITE).move_to(ORIGIN)
        # Adjust the path to your SVG file

        self.add(cpu)
        self.wait(2)

        # Number of circles
        num_circles = 4

        # Create groups for circles and labels
        circle_label_groups = []
        radi = [0.75, 0.5, 0.25, 0.5]
        for i in range(num_circles):
            # Create a circle
            circle = (
                Circle(radius=radi[i], color=WHITE)
                .set_fill(WHITE, opacity=1)
                .to_edge(LEFT)
                .to_edge(DOWN)
                .shift(LEFT * 2)
            )

            # Create a label and set its color to red
            label = Text(f"P{i + 1}", font_size=24).move_to(circle).set_color(RED)

            # Group the circle and the label
            circle_label_group = VGroup(circle, label)
            circle_label_groups.append(circle_label_group)

            # Animate the group moving into position
            if i == 0:
                self.play(circle_label_group.animate.move_to(ORIGIN).to_edge(DOWN))
            else:
                prev_group = circle_label_groups[i - 1]
                self.play(
                    circle_label_group.animate.next_to(prev_group, LEFT, buff=0.5)
                )

            self.wait()

        # Add a clock SVG in the upper right corner
        clock = SVGMobject(
            "img/clock.svg",
            color=WHITE,
            fill_color=WHITE,
            stroke_color=WHITE,
            stroke_width=2
        ).to_edge(UP + RIGHT)

        self.add(clock)
        self.wait(2)
