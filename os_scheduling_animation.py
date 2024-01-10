from manim import *
from src.components import *
from src.algorithms import *

PROCESS_SIZES_FCFS = [2, 3, 5, 1, 1, 2]
ADDITIONAL_PROCESS_FCFS = 2
PROCESS_SIZES_RR = PROCESS_SIZES_FCFS
ADDITIONAL_PROCESS_RR = ADDITIONAL_PROCESS_FCFS


class CustomMovingCameraScene(MovingCameraScene):
    """Custom Class used to extend the MovingCameraScene class from manimlib with a lot of methods to get the current camera position

    Args:
        MovingCameraScene (_type_): _description_
    """

    def construct(self):
        """Has to be called at the beginning of the construct method of the scene to initialize the camera position"""
        self._initial_camera_width = self.camera.frame.get_width()
        self._initial_camera_center = self.camera.frame.get_center()

    def move_camera_to_initial_position(self) -> Animation:
        """Returns an animation that moves the camera back to the initial position.

        Returns:
            Animation: The movement and scaling of the camera back to the initial position
        """
        return self.camera.frame.animate.move_to(self._initial_camera_center).set_width(
            self._initial_camera_width
        )

    def get_current_center(self):
        return self.camera.frame.get_center()

    def get_current_width(self):
        return self.camera.frame.get_width()

    def get_current_height(self):
        return self.camera.frame.get_height()

    def move_one_slide(self, x: np.ndarray = [0, 0, 0], y: np.ndarray = [0, 0, 0]):
        x = np.array(x)
        y = np.array(y)
        return self.camera.frame.animate.shift(
            x * self.get_current_width() + y * self.get_current_height()
        )

    def get_edge(self, edge: np.ndarray) -> np.ndarray:
        """Used to get the edge of the camera frame

        Args:
            edge (np.ndarray): This is the edge of the camera frame that should be returned (e.g. LEFT, RIGHT, UP, DOWN)

        Returns:
            np.ndarray: The position of the edge of the camera frame
        """
        if not any(
            np.array_equal(edge, valid_edge) for valid_edge in [LEFT, RIGHT, UP, DOWN]
        ):
            raise ValueError("edge must be one of LEFT, RIGHT, UP, DOWN")
        if np.array_equal(edge, LEFT):
            return self.camera.frame.get_left()
        if np.array_equal(edge, RIGHT):
            return self.camera.frame.get_right()
        if np.array_equal(edge, UP):
            return self.camera.frame.get_top()
        if np.array_equal(edge, DOWN):
            return self.camera.frame.get_bottom()

        return None

    def get_to_edge(
        self,
        edge: np.ndarray,
        margin: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER,
        object_width: float = 0,
        object_height: float = 0,
    ) -> np.ndarray:
        """Used to get the position of the edge of the camera frame with a margin

        Args:
            edge (np.ndarray): This is the edge of the camera frame that should be returned (e.g. LEFT, RIGHT, UP, DOWN)
            margin (float, optional): This is how far from the edge the center of the returned position should be. Defaults to DEFAULT_MOBJECT_TO_EDGE_BUFFER.
            object_width (float, optional): When used to move an object this takes the width of an object to adjust the margin. Defaults to 0.
            object_width (float, optional): When used to move an object this takes the height of an object to adjust the margin. Defaults to 0.

        Returns:
            np.ndarray: position of the edge of the camera frame with a margin
        """

        if np.array_equal(edge, UP):
            return self.get_edge(UP) + DOWN * margin + DOWN * object_height / 2
        if np.array_equal(edge, DOWN):
            return self.get_edge(DOWN) + UP * margin + UP * object_height / 2
        if np.array_equal(edge, LEFT):
            return self.get_edge(LEFT) + RIGHT * margin + RIGHT * object_width / 2
        if np.array_equal(edge, RIGHT):
            return self.get_edge(RIGHT) + LEFT * margin + LEFT * object_width / 2
        return None

    def get_to_corner(
        self,
        corner: np.ndarray,
        x_margin: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER,
        y_margin: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER,
        object_width: float = 0,
        object_height: float = 0,
    ) -> np.ndarray:
        """Used to get to a specific corner of the camera frame with a margin

        Args:
            corner (np.ndarray): The desired corner
            x_margin (float, optional): the margin on the X-Axis. Defaults to DEFAULT_MOBJECT_TO_EDGE_BUFFER.
            y_margin (float, optional): the margin on the Y-Axis. Defaults to DEFAULT_MOBJECT_TO_EDGE_BUFFER.
            object_width (float, optional): When used to move an object this takes the width of an object to adjust the margin. Defaults to 0.
            object_height (float, optional): When used to move an object this takes the height of an object to adjust the margin. Defaults to 0.

        Returns:
            np.ndarray: position of the corner of the camera frame with a margin
        """

        x_margin += object_width / 2
        y_margin += object_height / 2
        if np.array_equal(corner, UR):
            return (
                self.get_to_edge(edge=RIGHT, margin=x_margin) * X_AXIS
                + self.get_to_edge(edge=UP, margin=y_margin) * Y_AXIS
            )
        if np.array_equal(corner, UL):
            return (
                self.get_to_edge(edge=LEFT, margin=x_margin) * X_AXIS
                + self.get_to_edge(edge=UP, margin=y_margin) * Y_AXIS
            )
        if np.array_equal(corner, DR):
            return (
                self.get_to_edge(edge=RIGHT, margin=x_margin) * X_AXIS
                + self.get_to_edge(edge=DOWN, margin=y_margin) * Y_AXIS
            )
        if np.array_equal(corner, DL):
            return (
                self.get_to_edge(edge=LEFT, margin=x_margin) * X_AXIS
                + self.get_to_edge(edge=DOWN, margin=y_margin) * Y_AXIS
            )
        return None


class OS(CustomMovingCameraScene):
    def construct(self):
        super().construct()
        # creative introduction
        # 2 min
        self.camera.frame.save_state()
        # self.introduction()
        # self.clear()
        # self.camera.frame.restore()
        # # 2 min
        self.play(self.move_one_slide(x=RIGHT * 0.5))
        self.fcfs()
        self.wait(1)
        # self.clear()
        # self.camera.frame.restore()
        # # In der Überleitung Preemptive verwenden und erklären was das bedeutet
        # # 3 min

        # self.rr()
        # self.clear()
        # self.camera.frame.restore()

        # # 3 min
        # self.mqs()
        # self.clear()
        # self.camera.frame.restore()

        # # 3 min
        # self.metrics()
        # self.clear()
        # self.camera.frame.restore()

        # # reallife examples
        # # 2 min
        # self.outro()
        # self.clear()
        # self.camera.frame.restore()

    def introduction(self):
        # 01 - todo list
        todo = Text("My TODO List:", font_size=24)
        todo1 = Text("- Buy groceries.", font_size=24)
        todo2 = Text("- Annoy Lasse.", font_size=24)
        todo3 = Text("- Take out the trash.", font_size=24)
        todo4 = Text("- Finish AAML Homework.", font_size=24)

        todo_group = VGroup(todo, todo1, todo2, todo3, todo4).arrange(
            DOWN, aligned_edge=LEFT
        )
        todo_group.move_to(self.get_to_edge(LEFT, object_width=todo_group.get_width()))
        self.play(Write(todo_group), run_time=4)

        # 02 - symbols
        icon1 = SVGMobject("img/intro_outro/double_arrow.svg", fill_color=WHITE).scale(
            0.5
        )
        icon2_1 = SVGMobject("img/intro_outro/arrow_left", fill_color=WHITE).scale(0.4)
        # icon2_1.shift(LEFT*2)
        icon2_2 = SVGMobject("img/intro_outro/arrow_right", fill_color=WHITE).scale(0.4)
        # icon2_2.shift(RIGHT*2)
        icon2 = VGroup(icon2_1, icon2_2).arrange(RIGHT, buff=-0.3)
        # icon2 = VGroup(icon2_1, icon2_2).arrange(DOWN, buff=-0.3)
        icon3 = SVGMobject("img/intro_outro/prio1", fill_color=WHITE).scale(0.6)

        icons = VGroup(icon1, icon2, icon3).arrange(DOWN, buff=1)
        icons.move_to(self.get_current_center())
        self.play(ShowIncreasingSubsets(icons, run_time=3))

        # 03 - question mark
        question = SVGMobject("img/intro_outro/question", fill_color=WHITE).scale(1.2)
        question.move_to(
            self.get_to_edge(RIGHT, margin=1.75, object_width=question.get_width())
        )
        self.play(FadeIn(question), run_time=2)
        self.wait(4)
        self.play(FadeOut(question), run_time=2)

        # 04 - cpu
        cpu = CPU(size=1)
        cpu.move_to(self.get_to_edge(RIGHT, margin=1.75, object_width=cpu.get_width()))
        self.play(FadeIn(cpu), run_time=2)
        self.wait(4)

        # 05 - evlt. processes hinzufügen
        # fadout mit question mark. und fade in von prozessen mit cpu

    def fcfs(self):
        # TODO an camera position anpassen

        # self.fcfs_animation()
        # self.fcfs_bullet_points()
        # self.play(self.move_camera_to_initial_position())
        self.fcfs_flow()
        # self.play(self.move_one_slide(x=RIGHT * 2))
        # self.fcfs_pros_cons()

    def fcfs_animation(self):
        title = AnimatedTitle("First-Come-First-Serve")
        self.play(
            title.create_animation(
                center=self.get_current_center(),
                corner=self.get_to_corner(UL),
            )
        )
        # create and animate CPU
        cpu = CPU(show_gear=True, title="CPU", center=self.get_current_center())

        # Define all the points around the clock for later use
        factor = 1.5
        CPU_RIGHT = np.array(cpu.get_right() + RIGHT * factor)

        PROCESS_POLE_POSITION = (
            ProcessAnimated()
            .move_to(CPU_RIGHT * X_AXIS + self.get_to_edge(DOWN, margin=1) * Y_AXIS)
            .get_center()
        )
        # initialize the RoundRobin object
        quantum = 1
        fcfs = AlgorithmAnimation(quantum, type="fcfs")

        self.play(FadeIn(cpu))
        self.wait(2)

        # create processes and place them just outside the left edge
        for i, size in enumerate(PROCESS_SIZES_FCFS):
            process = (
                ProcessAnimated(title=f"P{i+1}", size=size)
                .move_to(self.get_to_corner(DL, y_margin=1))
                .shift(LEFT * 4)
            )
            fcfs.add_process(process)

        # animate processes into cpu queue position
        self.play(
            fcfs.move_queue(
                pole_position=PROCESS_POLE_POSITION,
                first_process_in_cpu=False,
                duration=5,
            )
        )

        # create and animate clock
        clock = Clock(radius=0.75)

        clock.move_to(self.get_to_corner(UR, x_margin=1, y_margin=1))
        self.play(FadeIn(clock))

        cpu_empty = True

        # Track the number of quantums that have been executed
        enumeration = 0
        while not fcfs.get_empty():
            # Add a new process after the third quantum
            if enumeration == 3:
                fcfs.add_process(
                    ProcessAnimated(
                        title=f"P{len(PROCESS_SIZES_FCFS)+1}",
                        size=ADDITIONAL_PROCESS_FCFS,
                        color=RED,
                    )
                    .move_to(self.get_to_corner(DL, y_margin=1))
                    .shift(LEFT * 4)
                )

            if cpu_empty:
                # calculate the arc from current process next to cpu
                arc_to_cpu = ArcBetweenPoints(
                    fcfs.process_queue[0].get_center(), CPU_RIGHT, angle=TAU / 4
                )
                # move current process next to cpu
                self.play(MoveAlongPath(fcfs.process_queue[0], arc_to_cpu))

                # animate queue
                queue_movement = fcfs.move_queue(
                    pole_position=PROCESS_POLE_POSITION,
                    first_process_in_cpu=True,
                    duration=1,
                )
                # the animation might return None if the queue is empty
                if queue_movement is not None:
                    self.play(queue_movement)

            # process
            cpu_empty, run_animation = fcfs.run()
            self.play(AnimationGroup(run_animation, clock.rotate(), cpu.rotate_gear()))
            enumeration += 1
        self.play(FadeOut(clock))

    def fcfs_bullet_points(self):
        points = [
            "Processes get queued up in the order they arrive.",
            "The first process in the queue gets processed until it's finished.",
            "The processes then get moved up in the queue and are processed until there is no process left.",
        ]

        bulletpoints = AnimatedBulletpoints(points, edge=self.get_to_edge(RIGHT))
        self.play(bulletpoints.create_animation())

    def fcfs_flow(self):
        # TODO: Sind das die von euch @Jannik/Benedikt oder noch von mir?
        # Sind jetzt angepasst von Jannik
        # TODO
        processes = [
            SequenceDiagrammProcess(id=idx + 1, arrival_time=0, burst_time=size)
            for idx, size in enumerate(PROCESS_SIZES_FCFS)
        ]
        processes.append(
            SequenceDiagrammProcess(
                id=len(processes) + 1,
                arrival_time=3,
                burst_time=ADDITIONAL_PROCESS_FCFS,
            )
        )

        fcfs = FirstComeFirstServe()
        steps = schedule_processes(fcfs, processes=processes)

        sequence_diagram = SequenceDiagram(
            "FCFS", steps=steps, upper_left_corner=self.get_to_corner(UL)
        )
        self.play(
            sequence_diagram.create_animations(
                left_edge=self.get_to_edge(LEFT),
                top_edge=self.get_to_edge(UP),
                frame_height=self.get_current_height(),
                frame_width=self.get_current_width(),
            )
        )
        self.wait(2)

    def fcfs_pros_cons(self):
        title = CustomTitle(
            title_text="Pros and Cons of FCFS", corner=self.get_to_corner(UL)
        )
        self.play(FadeIn(title))
        positive = [
            "Due to it's simplicity FCFS is easy to implement and understand.",
            "It treats all processes equally, which is fair.",
            "It also doesn't starve processes as high priority processes don't delay the processing of lower prio processes.",
        ]
        neutral = [
            "It's application is limited systems without the need of prioritization or real time processing.",
        ]
        negative = [
            "FCFS can lead to long waiting times, especially for tasks that arrive just after a long task.",
            "It cannot prioritize important or urgent tasks.",
            "Once a task starts executing, it runs to completion (Non-preemptive). This can cause issues if a high-priority task arrives after a long-running task has already started",
        ]

        animated_review = AnimatedReview(
            positive,
            neutral,
            negative,
            width=90,
            left_edge=self.get_to_edge(LEFT),
        )
        self.play(animated_review.create_animation())

    def rr(self):
        self.play(self.move_one_slide(x=RIGHT))
        self.rr_animation()
        self.wait(1)

        # self.play(self.move_one_slide(x=RIGHT))
        self.rr_bullet_points()
        self.wait(1)

        # self.play(self.move_one_slide(y=DOWN))
        self.move_camera_to_initial_position()
        self.rr_flow()
        self.wait(1)

        self.play(self.move_one_slide(x=RIGHT * 2))
        self.rr_pros_cons()
        self.wait(2)

    def rr_animation(self):
        # create and animate title for RoundRobin
        title = AnimatedTitle("Round Robin")
        self.play(
            title.create_animation(
                center=self.get_current_center(),
                corner=self.get_to_corner(UL),
            )
        )

        # create and animate CPU
        cpu = CPU(show_gear=True, title="CPU", center=self.get_current_center())
        # Define all the points around the clock for later use
        faktor = 1.5

        CPU_TOP = np.array(cpu.get_top() + UP * faktor)
        CPU_BOTTOM = np.array(cpu.get_bottom() + DOWN * faktor)
        CPU_RIGHT = np.array(cpu.get_right() + RIGHT * faktor)
        CPU_LEFT = np.array(cpu.get_left() + LEFT * faktor)

        CPU_RIGHT_UPPER_CORNER = np.array(
            (CPU_RIGHT * X_AXIS + CPU_TOP * Y_AXIS) - (UP + RIGHT) * 0.75
        )
        CPU_LEFT_UPPER_CORNER = np.array(
            (CPU_LEFT * X_AXIS + CPU_TOP * Y_AXIS) - (UP + LEFT) * 0.75
        )
        CPU_LEFT_LOWER_CORNER = np.array(
            (CPU_LEFT * X_AXIS + CPU_BOTTOM * Y_AXIS) - (DOWN + LEFT) * 0.75
        )

        # save where the process to be executed next moves (right to the cpu at the bottom edge)
        PROCESS_POLE_POSITION = (
            ProcessAnimated()
            .move_to(CPU_RIGHT * X_AXIS + self.get_to_edge(DOWN, margin=1) * Y_AXIS)
            .get_center()
        )

        self.play(FadeIn(cpu))
        self.wait(2)

        # initialize the RoundRobin object
        quantum = 1
        rr = AlgorithmAnimation(quantum, type="rr")

        # Define all processes with it's lenghts
        process_sizes = [2, 3, 5, 1, 1, 2]
        # process_sizes = [2, 3]
        # create processes and place them just outside the left edge
        for i, size in enumerate(process_sizes):
            process = (
                ProcessAnimated(title=f"P{i+1}", size=size)
                .move_to(self.get_to_corner(DL, y_margin=1))
                .shift(LEFT * 4)
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

        clock.move_to(self.get_to_corner(UR, x_margin=1, y_margin=1))
        self.play(FadeIn(clock))

        # animate the process of RoundRobin
        enumeration = 0
        while not rr.get_empty():
            if enumeration == 3:
                new_process = (
                    ProcessAnimated(title=f"P{len(process_sizes)+1}", size=2, color=RED)
                    .move_to(self.get_to_corner(DL, y_margin=1))
                    .shift(LEFT * 4)
                )
                rr.add_process(new_process)
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
            # the animation might return None if the queue is empty
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
            enumeration += 1

        self.play(FadeOut(clock))
        for i, size in enumerate(process_sizes):
            process = (
                ProcessAnimated(title=f"P{i+1}", size=size)
                .move_to(self.get_to_corner(DL, y_margin=1))
                .shift(LEFT * 4)
            )
            rr.add_process(process)

        self.play(
            rr.move_queue(
                pole_position=PROCESS_POLE_POSITION,
                first_process_in_cpu=False,
                duration=5,
            )
        )

    def rr_bullet_points(self):
        points = [
            "CPU time gets divided into quantums.",
            "Each process get's processed for the duration of a quantum.",
            "After each quantum the current process is either finished or it's put back into the queue."
            + "\n=> Preemptive Schedulung",
        ]

        bulletpoints = AnimatedBulletpoints(points, edge=self.get_to_edge(RIGHT))
        self.play(bulletpoints.create_animation())

    def rr_flow(self):
        # steps = [
        #     {"id": 1, "start": 0, "size": 1},
        #     {"id": 2, "start": 1, "size": 1},
        #     {"id": 3, "start": 2, "size": 1},
        #     {"id": 4, "start": 3, "size": 1},
        #     {"id": 5, "start": 4, "size": 1},
        #     {"id": 6, "start": 5, "size": 1},
        #     {"id": 1, "start": 6, "size": 1},
        #     {"id": 2, "start": 7, "size": 1},
        #     {"id": 7, "start": 8, "size": 1},
        #     {"id": 3, "start": 9, "size": 1},
        #     {"id": 6, "start": 10, "size": 1},
        #     {"id": 2, "start": 11, "size": 1},
        #     {"id": 3, "start": 12, "size": 1},
        #     {"id": 3, "start": 13, "size": 1},
        #     {"id": 3, "start": 14, "size": 1},
        # ]
        # id: int, arrival_time: int, burst_time: int
        processes = [
            SequenceDiagrammProcess(id=1, arrival_time=0, burst_time=2),
            SequenceDiagrammProcess(id=2, arrival_time=0, burst_time=3),
            SequenceDiagrammProcess(id=3, arrival_time=0, burst_time=5),
            SequenceDiagrammProcess(id=4, arrival_time=0, burst_time=1),
            SequenceDiagrammProcess(id=5, arrival_time=0, burst_time=1),
            SequenceDiagrammProcess(id=6, arrival_time=0, burst_time=2),
            SequenceDiagrammProcess(id=7, arrival_time=8, burst_time=2),
        ]
        rr = RoundRobin(quantum=1)
        steps = schedule_processes(rr, processes)

        sequence_diagram = SequenceDiagram(
            "Round Robin", steps=steps, upper_left_corner=self.get_to_corner(UL)
        )
        self.play(
            sequence_diagram.create_animations(
                left_edge=self.get_to_edge(LEFT),
                top_edge=self.get_to_edge(UP),
                frame_height=self.get_current_height(),
                frame_width=self.get_current_width(),
            )
        )
        self.wait(2)
        self.clear()

    def rr_pros_cons(self):
        title = CustomTitle(
            title_text="Pros and Cons of RR", corner=self.get_to_corner(UL)
        )
        self.play(FadeIn(title))
        positive = [
            "RR is designed to treat all processes equally by allocating each a fixed time slice.",
            "RR can offer good response times and real time processing.",
            "Similar to FCFS every process gets an equal chance to execute, and can't starve.",
            "RR is preemptive which means that no single process can clogg the CPU.",
        ]
        neutral = [
            "The efficiency of RR heavily depends on the appropriate choice of the time quantum. A balance betwen high average waiting time and few context switches must be found.",
        ]
        negative = [
            "Processes that require more time than the average may suffer in terms of throughput",
            "RR doesn't support priority scheduling.",
        ]

        animated_review = AnimatedReview(
            positive,
            neutral,
            negative,
            width=90,
            left_edge=self.get_to_edge(LEFT),
        )
        self.play(animated_review.create_animation())

    def mqs(self):
        self.wait(1)
        self.play(self.move_one_slide(x=RIGHT))
        self.mqs_animation()

        self.mqs_bullet_points()
        self.mqs_flow()
        self.mqs_pros_cons()

        self.wait(1)

    def mqs_animation(self):
        # 01 - Title
        title = AnimatedTitle("Multilevel Queue Scheduling")
        self.play(
            title.create_animation(
                center=self.get_current_center(), corner=self.get_to_corner(UL)
            )
        )

        # 02 - Processes
        process_sizes = [2, 1, 3, 3, 2, 1, 2]
        processes = [
            ProcessAnimated(size=s, title=f"P{len(process_sizes)-i}")
            for i, s in enumerate(process_sizes)
        ]
        process_group = VGroup(*processes).arrange(RIGHT, buff=0.5)

        process_group.next_to(title, DOWN, aligned_edge=LEFT)
        process_group.shift(LEFT * self.get_current_width())
        self.play(
            process_group.animate.shift(RIGHT * self.get_current_width()), run_time=4
        )

        # 03 - Queues

        line = DashedLine(
            self.get_to_edge(LEFT),
            self.get_to_edge(RIGHT),
            dash_length=0.005,
        )
        line.move_to(self.get_current_center()).shift(DOWN * 0.6)

        self.play(FadeIn(line))

        queue1 = Text("Queue 1 - High Priority", font_size=24).next_to(
            process_group, DOWN, aligned_edge=LEFT
        )
        queue1.shift(DOWN * 0.1)
        # self.add(queue1)
        self.play(FadeIn(queue1))

        queue2 = Text("Queue 2 - Low Priority", font_size=24).next_to(
            line, DOWN, aligned_edge=LEFT
        )
        queue2.shift(DOWN * 0.1)
        # self.add(queue2)
        self.play(FadeIn(queue2))

        self.wait(2)
        # 04 - Queues Examples
        new_queue1_text = Text("Foreground - Round Robin", font_size=24).next_to(
            process_group, DOWN, aligned_edge=LEFT
        )
        new_queue1_text.shift(DOWN * 0.1)
        self.play(FadeOut(queue1))
        self.play(FadeIn(new_queue1_text))

        new_queue2_text = Text(
            "Background - First Come, First Serve", font_size=24
        ).next_to(line, DOWN, aligned_edge=LEFT)
        new_queue2_text.shift(DOWN * 0.1)
        self.play(FadeOut(queue2))
        self.play(FadeIn(new_queue2_text))

        # 05 - Move Processes to Queues
        above_indexes = [0, 3, 5]
        below_indexes = [1, 2, 4, 6]
        queue1_processes = VGroup()
        queue2_processes = VGroup()

        buffer_space = 0.5

        if above_indexes:
            first_proc_above = processes[above_indexes[0]]
            self.play(
                first_proc_above.animate.next_to(
                    new_queue1_text, DOWN, aligned_edge=LEFT
                )
            )

            last_process_position = first_proc_above.get_right()
            queue1_processes.add(first_proc_above)

            for idx in above_indexes[1:]:
                proc = processes[idx]
                self.play(
                    proc.animate.next_to(
                        last_process_position, RIGHT, buff=buffer_space
                    )
                )
                last_process_position = proc.get_right()
                queue1_processes.add(proc)

        if below_indexes:
            first_proc_below = processes[below_indexes[0]]

            self.play(
                first_proc_below.animate.next_to(
                    new_queue2_text, DOWN, aligned_edge=LEFT
                )
            )

            last_process_position = first_proc_below.get_right()
            queue2_processes.add(first_proc_below)

            for idx in below_indexes[1:]:
                proc = processes[idx]
                self.play(
                    proc.animate.next_to(
                        last_process_position, RIGHT, buff=buffer_space
                    )
                )
                last_process_position = proc.get_right()
                queue2_processes.add(proc)
        self.wait(2)

        cpu = CPU(size=0.5)
        clock = Clock(radius=0.5)
        clock.move_to(
            self.get_to_corner(
                UR,
                x_margin=0.3,
                y_margin=0.3,
                object_width=clock.get_width(),
                object_height=clock.get_height(),
            )
        )
        cpu.next_to(clock, LEFT, buff=0.25)
        self.add(cpu, clock)

        # 06 - Simulation (1 Foreground)
        self.wait(4)
        self.play(FadeOut(queue1_processes), run_time=2)
        self.wait(2)

        # 07 - Simulation (2 Background Part 1)
        self.play(FadeOut(queue2_processes[2:4]), run_time=2)

        # TODO: proper animation of RR and FCFS
        # animation = queue1_processes[0].adjust_size_with_animation(-1)
        # self.play(AnimationGroup(animation))

        # 08 - New process while execution
        p8 = ProcessAnimated(size=2, title=f"P8")
        p8.next_to(title, DOWN, aligned_edge=LEFT)
        p8.shift(LEFT * self.get_current_width())
        self.play(p8.animate.shift(RIGHT * self.get_current_width()), run_time=4)

        # 09 - Move new process to foreground
        self.play(p8.animate.next_to(new_queue1_text, DOWN, aligned_edge=LEFT))
        self.wait(2)
        # 10 - Simulation (3 Foreground Part 2 (new process))
        self.play(FadeOut(p8), run_time=2)
        self.wait(2)

        # 11 - Simulation (4 Background Part 2)
        self.play(FadeOut(queue2_processes[0:2]), run_time=2)

        # 12 -
        self.remove(queue1, new_queue1_text, line, new_queue2_text, queue2, cpu, clock)

    def mqs_bullet_points(self):
        # TODO: add title
        # several queues
        line = DashedLine(LEFT * 0.5, RIGHT * 0.5, dash_length=0.005).set_length(7)
        lines = [line.copy() for _ in range(4)]
        queues = [
            Text("system processes"),
            Text("interactive processes"),
            Text("interactive editing processes"),
            Text("batch processes"),
            Text("student processes"),
        ]
        group = []
        for i in range(len(lines)):
            group.append(queues[i].scale(0.5))
            group.append(lines[i])
        group.append(queues[-1].scale(0.5))
        lines = VGroup(*group).arrange(DOWN, buff=0.25)

        lines.move_to(self.get_current_center())
        lines.shift(LEFT * 3)
        self.play(FadeIn(lines))
        self.wait(5)

        # bullet points
        points = [
            "Processes are distributed to different queues.",
            "Queues use different scheduling algorithms.",
            "Execution of queues determind by priority.",
        ]

        bulletpoints = AnimatedBulletpoints(
            points, edge=self.get_to_edge(RIGHT), width=40
        )
        self.play(bulletpoints.create_animation())
        self.wait(5)

        # review = AnimatedReview(["some positive things about this..., and some more"],["this is ok..."], ["these things are very very bad..."]).to_edge(RIGHT)
        # self.play(review.create_animation())

    def mqs_flow(self):
        # Code to demonstrate the flow of processes in MQS
        # Your code: ...

        self.clear()

        # TODO: Sind das die von euch @Jannik/Benedikt oder noch von mir?
        # steps = [
        #     {"id": 1, "start": 0, "size": 4},
        #     {"id": 2, "start": 4, "size": 2},
        #     {"id": 3, "start": 6, "size": 1},
        #     {"id": 4, "start": 7, "size": 5},
        #     {"id": 2, "start": 12, "size": 2},
        #     {"id": 3, "start": 14, "size": 2},
        #     {"id": 4, "start": 16, "size": 5},
        #     {"id": 3, "start": 21, "size": 3},
        # ]

        mlq = MultiLevelQueue(quantum=1)
        steps = schedule_processes(mlq)

        sequence_diagram = SequenceDiagram(
            "MLQ", steps=steps, upper_left_corner=self.get_to_corner(UL)
        )
        self.play(
            sequence_diagram.create_animations(
                left_edge=self.get_to_edge(LEFT),
                top_edge=self.get_to_edge(UP),
                frame_height=self.get_current_height(),
                frame_width=self.get_current_width(),
            )
        )
        self.wait(2)
        self.clear()

    def mqs_pros_cons(self):
        # Code to analyze and present the advantages and disadvantages of MQS
        pass

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
        datasets = create_linechart_metrics(
            algorithms=[
                FirstComeFirstServe(),
                RoundRobin(quantum=1),
                MultiLevelQueue(quantum=1),
            ],
            stepsize=10,
        )
        print(datasets)
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

        # Calculate metrics for bar charts
        processes = create_processes()

        fcfs_algo = FirstComeFirstServe()
        fcfs_scheduler = Scheduler()
        fcfs_scheduler.set_processes(processes)
        fcfs_scheduler.run_algorithm(fcfs_algo, display=True)
        fcfs_metrics = fcfs_scheduler.get_metrics()

        rr_algo = RoundRobin(quantum=1)
        rr_scheduler = Scheduler()
        rr_scheduler.set_processes(processes)
        rr_scheduler.run_algorithm(rr_algo, display=True)
        rr_metrics = rr_scheduler.get_metrics()

        mlq_algo = MultiLevelQueue(quantum=1)
        mlq_scheduler = Scheduler()
        mlq_scheduler.set_processes(processes)
        mlq_scheduler.run_algorithm(mlq_algo, display=True)
        mlq_metrics = mlq_scheduler.get_metrics()

        # 1st BarChart metric
        first_bar_chart = MetricBarChart(
            datasets=[
                fcfs_metrics["fairness_index"],
                rr_metrics["fairness_index"],
                mlq_metrics["fairness_index"],
            ],
            titles=["FCFS", "RR", "MLQ"],
            y_text="Fairness Index",
        )
        first_bar_chart.scale(0.5).to_corner(
            UP + RIGHT, buff=DEFAULT_MOBJECT_TO_EDGE_BUFFER
        )
        self.add(first_bar_chart)
        bar_grow_sequence = first_bar_chart.animate_bars()
        self.play(bar_grow_sequence)

        # 2nd BarChart metric
        second_bar_chart = MetricBarChart(
            datasets=[
                fcfs_metrics["context_switches"],
                rr_metrics["context_switches"],
                mlq_metrics["context_switches"],
            ],
            titles=["FCFS", "RR", "MLQ"],
            y_text="Context Switches",
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
        # 01 - recap
        summary1 = Text("First Come First Serve", font_size=28)
        summary2 = Text("Round Robin", font_size=28)
        summary3 = Text("Multi Level Queue", font_size=28)

        summary = (
            VGroup(summary1, summary2, summary3)
            .arrange(DOWN, aligned_edge=LEFT)
            .to_edge(LEFT, buff=1)
        )
        self.play(Write(summary), run_time=4)
        self.wait(2)

        # todo list
        # 01 - todo list
        todo = Text("My TODO List:", font_size=24)
        todo1 = Text("- Buy groceries.", font_size=24)
        todo2 = Text("- Annoy Lasse.", font_size=24)
        todo3 = Text("- Take out the trash.", font_size=24)
        todo4 = Text("- Finish AAML Homework.", font_size=24)

        todo_group = (
            VGroup(todo, todo1, todo2, todo3, todo4)
            .arrange(DOWN, aligned_edge=LEFT)
            .to_edge(RIGHT, buff=3)
        )
        self.play(Write(todo_group), run_time=4)
        self.wait(2)

        # icons
        check = SVGMobject("img/intro_outro/check.svg", fill_color=WHITE).scale(0.15)
        check_group = (
            VGroup(*[check.copy() for _ in range(4)])
            .arrange(DOWN, buff=0.25)
            .next_to(todo_group, direction=RIGHT)
            .shift(DOWN * 0.25)
        )
        self.play(ShowIncreasingSubsets(check_group, run_time=4))
        self.wait(2)
