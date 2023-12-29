from manim import *


from src.components import *


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

        title = AnimatedTitle("RoundRobin")
        self.play(title.create_animation())

        cpu = CPU(color=RED, show_gear=True, title="CPU\nw/ RoundRobin")

        self.play(FadeIn(cpu))
        self.wait(2)

        process_sizes = [
            1,
            2,
            1,
            4,
            3,
            #     2,
            #     3,
            #     1,
            #     3,
            #     1,
        ]

        # self.add_section("RoundRobin01")
        processes: List[Process] = []
        # create processes
        for i, size in enumerate(process_sizes):
            process = (
                Process(title=f"P{i}", size=size, use_square=True)
                .to_edge(LEFT)
                .to_edge(DOWN)
                .shift(LEFT * 2)
            )
            processes.append(process)
        # animate processes into starting position
        for i, process in enumerate(processes):
            if i == 0:
                self.play(process.animate.move_to(ORIGIN).to_edge(DOWN))
            else:
                self.play(process.animate.next_to(processes[i - 1], LEFT, buff=0.5))
            self.wait()

        # self.add_section("RoundRobin02")

        clock = Clock(radius=0.75)

        clock.to_edge(RIGHT).to_edge(UP)
        self.play(FadeIn(clock))

        #
        self.next_section()

        quantum = 1
        self.wait(2)
        # Animate the process of RoundRobin
        animation = processes[3].adjust_size_with_animation(-3)
        self.play(animation)
        self.play(processes[3].title_text.animate.next_to(processes[3].shape, UP))
        self.wait(2)


class RoundRobinAnimation:
    def __init__(self, quantum: int) -> None:
        self.quantum = quantum
        self.process_queue = []

    def add_process(self, process: Process):
        self.process_queue.append(process)

    def run(self):
        if len(self.process_queue) == 0:
            return
        current_process = self.process_queue.pop(0)
        current_process.size -= 1
        if current_process.size >= 0:
            self.process_queue.append(current_process)


# class ExampleScene(Scene):
#     def construct(self):
#         datasets = [np.array([1, 2, 3, 4]), np.array([4, 3, 2, 1])]
#         titles = ["Dataset 1", "Dataset 2"]
#         metric_response_time = MetricResponseTime(datasets, titles)
#         self.play(metric_response_time.create_animation())
