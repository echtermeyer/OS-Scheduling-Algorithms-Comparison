import copy

from manim import *
from src.components import *
from src.algorithms import *

PROCESS_SIZES_FCFS = [2, 3, 5, 1, 1, 2]
ADDITIONAL_PROCESS_FCFS = 2
PROCESS_SIZES_RR = PROCESS_SIZES_FCFS
ADDITIONAL_PROCESS_RR = ADDITIONAL_PROCESS_FCFS

PROCESS_COLOR = BLUE
LATEPROCESS_COLOR = ORANGE
CPU_GEAR_COLOR = RED


class CustomMovingCameraScene(MovingCameraScene):
    """Custom Class used to extend the MovingCameraScene class from manimlib with a lot of methods to get the current camera position

    Args:
        MovingCameraScene (_type_): _description_
    """

    def construct(self):
        """Has to be called at the beginning of the construct method of the scene to initialize the camera position"""
        self._initial_camera_width = self.camera.frame.get_width()
        self._initial_camera_center = self.camera.frame.get_center()

    def move_camera_to_initial_position(self, only_x=False, only_y=False) -> Animation:
        """Returns an animation that moves the camera back to the initial position.

        Returns:
            Animation: The movement and scaling of the camera back to the initial position
        """
        if only_x:
            return self.camera.frame.animate.move_to(
                self._initial_camera_center * X_AXIS
                + self.get_current_center() * Y_AXIS
            ).set_width(self._initial_camera_width)
        if only_y:
            return self.camera.frame.animate.move_to(
                self._initial_camera_center * Y_AXIS
                + self.get_current_center() * X_AXIS
            ).set_width(self._initial_camera_width)
        return self.camera.frame.animate.move_to(self._initial_camera_center).set_width(
            self._initial_camera_width
        )

    def get_current_center(self):
        return self.camera.frame.get_center()

    def get_current_width(self):
        return self.camera.frame.get_width()

    def get_current_height(self):
        return self.camera.frame.get_height()

    def move_one_slide(
        self,
        x: np.ndarray = [0, 0, 0],
        y: np.ndarray = [0, 0, 0],
        height=None,
        width=None,
    ):
        x = np.array(x)
        y = np.array(y)
        if height is not None:
            x = x * height
        else:
            x = x * self.get_current_width()

        if width is not None:
            y = y * width
        else:
            y = y * self.get_current_height()
        return self.camera.frame.animate.shift(x + y)

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
        run_time_one_slide = 2
        run_time_back = 2
        # introduction
        # 2 min

        # R0 C0
        self.wait(1)
        self.title_slide()
        intital_left = self.get_to_edge(LEFT)
        self.play(self.move_one_slide(y=DOWN), runtime=run_time_one_slide)

        # R1 C0
        self.wait(1)
        self.introduction()
        self.play(
            self.move_camera_to_initial_position(only_y=True), runtime=run_time_back
        )
        self.play(self.move_one_slide(x=RIGHT), runtime=run_time_one_slide)

        # 2 min
        # R2 C0
        self.wait(1)
        self.fcfs()
        self.play(
            self.move_camera_to_initial_position(only_y=True), runtime=run_time_back
        )
        self.play(self.move_one_slide(x=RIGHT), runtime=run_time_one_slide)

        # 3 min
        # R3 C0
        self.wait(1)
        self.rr()
        self.play(
            self.move_camera_to_initial_position(only_y=True), runtime=run_time_back
        )
        self.play(self.move_one_slide(x=RIGHT), runtime=run_time_one_slide)

        # 3 min
        # R4 C0
        self.wait(1)
        self.mqs()
        self.play(
            self.move_camera_to_initial_position(only_y=True), runtime=run_time_back
        )
        self.play(self.move_one_slide(x=RIGHT), runtime=run_time_one_slide)

        # 3 min
        # R5 C0
        self.wait(1)
        self.metrics()
        self.play(
            self.move_camera_to_initial_position(only_y=True), runtime=run_time_back
        )
        self.play(self.move_one_slide(x=RIGHT), runtime=run_time_one_slide)

        #  reallife examples
        # 2 min
        self.wait(1)
        self.application()
        self.play(self.move_one_slide(y=DOWN), runtime=run_time_one_slide)

        self.wait(1)
        self.outro()

        self.wait(1)

        self.play(
            self.camera.frame.animate.set(
                width=abs(intital_left[0]) + abs(self.get_to_edge(RIGHT, margin=0)[0])
            ).move_to(
                self.get_current_center() * Y_AXIS
                + (intital_left + self.get_to_edge(RIGHT, margin=0)) / 2 * X_AXIS
            ),
            runtime=5,
        )

        self.wait(4)

    def title_slide(self):
        # main title
        title = Text("OS Scheduling Algorithms", font_size=36, color=BLUE).move_to(
            self.get_current_center() + UP * 0.5
        )
        # subtitle text
        subtitle = Text("By Benedikt, Eric and Jannik", font_size=24).next_to(
            title, DOWN
        )

        self.play(FadeIn(title), FadeIn(subtitle), run_time=3)
        self.wait(2)

    def introduction(self):
        # 01 - todo list appeares
        todo = Text("My to-do list:", font_size=24)
        todo1 = Text("- Buy groceries.", font_size=24)
        todo2 = Text("- Annoy Lasse.", font_size=24)
        todo3 = Text("- Take out the trash.", font_size=24)
        todo4 = Text("- Finish AAML Homework.", font_size=24)

        todo_group = VGroup(todo, todo1, todo2, todo3, todo4).arrange(
            DOWN, aligned_edge=LEFT
        )
        todo_group.move_to(self.get_to_edge(LEFT, object_width=todo_group.get_width()))
        self.play(Write(todo_group), run_time=5)
        self.wait(4)
        # 02 - symbols in the middle
        icon1 = SVGMobject("img/intro_outro/double_arrow.svg", fill_color=WHITE).scale(
            0.5
        )
        icon2_1 = SVGMobject("img/intro_outro/arrow_left", fill_color=WHITE).scale(0.4)
        icon2_2 = SVGMobject("img/intro_outro/arrow_right", fill_color=WHITE).scale(0.4)
        icon2 = VGroup(icon2_1, icon2_2).arrange(RIGHT, buff=-0.3)
        icon3 = SVGMobject("img/intro_outro/prio1", fill_color=WHITE).scale(0.6)
        icons = VGroup(icon1, icon2, icon3).arrange(DOWN, buff=1)
        icons.move_to(self.get_current_center())
        self.play(ShowIncreasingSubsets(icons, run_time=6))
        self.wait(3)
        # 03 - question mark on the right
        question = SVGMobject("img/intro_outro/question", fill_color=WHITE).scale(1.2)
        question.move_to(
            self.get_to_edge(RIGHT, margin=1.75, object_width=question.get_width())
        )
        self.play(FadeIn(question), run_time=2)
        self.wait(12)
        self.play(FadeOut(question), run_time=2)

        # 04 - replace question mark with cpu
        cpu = CPU(size=1)
        cpu.move_to(self.get_to_edge(RIGHT, margin=1.75, object_width=cpu.get_width()))
        self.play(FadeIn(cpu), run_time=2)
        self.wait(11)

    def fcfs(self):
        self.fcfs_animation()
        # 54 Seconds
        self.fcfs_bullet_points()

        self.play(self.move_one_slide(y=DOWN))
        # 71 Seconds
        self.fcfs_flow()
        # 108 Seconds
        self.play(self.move_one_slide(y=DOWN))
        self.fcfs_pros_cons()

    def fcfs_animation(self):
        title = AnimatedTitle("First Come First Serve")
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
                ProcessAnimated(color=PROCESS_COLOR, title=f"P{i+1}", size=size)
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
                        color=LATEPROCESS_COLOR,
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
            ("Processes get queued up in the order they arrive", 1),
            ("The first process in the queue gets processed until it's finished", 1),
            (
                "The processes then get moved up in the queue and are processed until there is no process left",
                1,
            ),
        ]

        bulletpoints = AnimatedBulletpoints(points, edge=self.get_to_edge(RIGHT))
        self.play(bulletpoints.create_animation())

    def fcfs_flow(self):
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
            "Simplicity",
            "Fairness",
            "No starvation",
        ]
        neutral = [
            "Limited application",
        ]
        negative = [
            "Long waiting times",
            "No prioritization",
            "Non-Preemptive",
        ]

        animated_review = AnimatedReview(
            positive,
            neutral,
            negative,
            width=90,
            center=self.get_current_center(),
            horizontal=True,
        )
        self.play(animated_review.create_animation())

    def rr(self):

        self.rr_animation()
        self.rr_bullet_points()

        self.play(self.move_one_slide(y=DOWN))
        self.rr_flow()

        self.play(self.move_one_slide(y=DOWN))
        self.rr_pros_cons()

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
                ProcessAnimated(color=PROCESS_COLOR, title=f"P{i+1}", size=size)
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
                    ProcessAnimated(
                        color=LATEPROCESS_COLOR,
                        title=f"P{len(process_sizes)+1}",
                        size=2,
                    )
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

    def rr_bullet_points(self):
        points = [
            ("CPU time gets divided into quantums.", 1),
            ("Each process get's processed for the duration of a quantum.", 1),
            (
                "After each quantum the current process is either finished or it's put back into the queue"
                + "\n=> Preemptive Scheduling",
                1,
            ),
        ]

        bulletpoints = AnimatedBulletpoints(points, edge=self.get_to_edge(RIGHT))
        self.play(bulletpoints.create_animation())

    def rr_flow(self):
        processes = [
            SequenceDiagrammProcess(id=1, arrival_time=0, burst_time=2),
            SequenceDiagrammProcess(id=2, arrival_time=0, burst_time=3),
            SequenceDiagrammProcess(id=3, arrival_time=0, burst_time=5),
            SequenceDiagrammProcess(id=4, arrival_time=0, burst_time=1),
            SequenceDiagrammProcess(id=5, arrival_time=0, burst_time=1),
            SequenceDiagrammProcess(id=6, arrival_time=0, burst_time=2),
            SequenceDiagrammProcess(id=7, arrival_time=4, burst_time=2),
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

    def rr_pros_cons(self):
        title = CustomTitle(
            title_text="Pros and Cons of RR", corner=self.get_to_corner(UL)
        )
        self.play(FadeIn(title))
        positive = [
            "Fixed time slice",
            "Good response times & real time processing",
            "No Starvation",
            "Preemptive",
        ]
        neutral = [
            "Efficiency dependent on quantum",
            "Waiting time vs. context switches",
        ]
        negative = [
            "Low throughput for long processes",
            "No priorities",
        ]

        animated_review = AnimatedReview(
            positive,
            neutral,
            negative,
            width=25,
            horizontal=True,
            center=self.get_current_center(),
        )
        self.play(animated_review.create_animation())

    def mqs(self):
        # Scences of the Mulitlevel-Queue Algorithm
        self.mqs_animation()
        self.mqs_bullet_points()

        self.play(self.move_one_slide(y=DOWN))
        self.mqs_flow()

        self.play(self.move_one_slide(y=DOWN))
        self.mqs_pros_cons()

    def mqs_animation(self):
        # 01 - Title
        title = AnimatedTitle("Multilevel Queue Scheduling")
        self.play(
            title.create_animation(
                center=self.get_current_center(), corner=self.get_to_corner(UL)
            )
        )
        self.wait(6)
        # 02 - Processes move into the screen
        process_sizes = PROCESS_SIZES_FCFS  # [2, 1, 3, 3, 2, 1, 2]
        processes = [
            ProcessAnimated(
                color=PROCESS_COLOR, size=s, title=f"P{len(process_sizes)-i}"
            )
            for i, s in enumerate(process_sizes)
        ]
        process_group = VGroup(*processes).arrange(RIGHT, buff=0.5)

        process_group.next_to(title, DOWN, aligned_edge=LEFT)
        process_group.shift(LEFT * self.get_current_width())
        for process in reversed(processes):
            animation = process.animate.shift(RIGHT * self.get_current_width())
            self.play(animation, run_time=1)
            self.wait(0.5)

        self.wait(1)

        # 03 - Queues appeare
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
        self.play(FadeIn(queue1))

        queue2 = Text("Queue 2 - Low Priority", font_size=24).next_to(
            line, DOWN, aligned_edge=LEFT
        )
        queue2.shift(DOWN * 0.1)
        self.play(FadeIn(queue2))
        self.wait(3)

        # 04 - Queues are named with used algorithms
        self.wait(13)
        new_queue1_text = Text("Foreground - Round Robin", font_size=24).next_to(
            process_group, DOWN, aligned_edge=LEFT
        )
        new_queue1_text.shift(DOWN * 0.1)
        self.play(FadeOut(queue1))
        self.play(FadeIn(new_queue1_text))
        self.wait(8)
        new_queue2_text = Text(
            "Background - First Come First Serve", font_size=24
        ).next_to(line, DOWN, aligned_edge=LEFT)
        new_queue2_text.shift(DOWN * 0.1)
        self.play(FadeOut(queue2))
        self.play(FadeIn(new_queue2_text))
        self.wait(4)

        # 05 - Processes are moved into the queues
        self.wait(7)
        above_indexes = [0, 3, 5]
        below_indexes = [1, 2, 4]
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
        self.wait(12)

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
        self.play(FadeIn(cpu))
        self.play(FadeIn(clock))

        # 06 - Simulation (1 Foreground)
        a1 = queue1_processes[2].adjust_size_with_animation()
        self.play(AnimationGroup(a1, clock.rotate(), cpu.rotate_gear()))
        self.wait(0.5)
        a2 = queue1_processes[1].adjust_size_with_animation()
        self.play(AnimationGroup(a2, clock.rotate(), cpu.rotate_gear()))
        self.play(
            AnimationGroup(
                FadeOut(queue1_processes[1]), queue1_processes[1].animate.scale(0.1)
            )
        )
        a3 = queue1_processes[0].adjust_size_with_animation()
        self.play(AnimationGroup(a3, clock.rotate(), cpu.rotate_gear()))
        self.wait(0.5)
        a4 = queue1_processes[2].adjust_size_with_animation()
        self.play(AnimationGroup(a4, clock.rotate(), cpu.rotate_gear()))
        self.play(
            AnimationGroup(
                FadeOut(queue1_processes[2]), queue1_processes[2].animate.scale(0.1)
            )
        )
        a5 = queue1_processes[0].adjust_size_with_animation()
        self.play(AnimationGroup(a5, clock.rotate(), cpu.rotate_gear()))
        self.play(
            AnimationGroup(
                FadeOut(queue1_processes[0]), queue1_processes[0].animate.scale(0.1)
            )
        )
        self.wait(4)

        # 07 - Simulation (2 Background Part 1)
        a1 = queue2_processes[2].adjust_size_with_animation()
        self.play(AnimationGroup(a1, clock.rotate(), cpu.rotate_gear()))
        self.play(
            AnimationGroup(
                FadeOut(queue2_processes[2]), queue2_processes[2].animate.scale(0.1)
            )
        )

        # 08 - New process arrives while execution
        p7 = ProcessAnimated(
            color=LATEPROCESS_COLOR, size=ADDITIONAL_PROCESS_FCFS, title=f"P7"
        )
        p7.next_to(title, DOWN, aligned_edge=LEFT)
        p7.shift(LEFT * self.get_current_width())
        self.play(p7.animate.shift(RIGHT * self.get_current_width()), run_time=4)
        self.wait(2)

        # 09 - Move new process to foreground
        self.play(
            p7.animate.next_to(new_queue1_text, DOWN, aligned_edge=LEFT), run_time=4
        )

        self.wait(6)

        # 10 - Simulation (3 Foreground Part 2 (new process))
        ax1 = p7.adjust_size_with_animation()
        self.play(AnimationGroup(ax1, clock.rotate(), cpu.rotate_gear()))

        self.wait(1)

        ax2 = p7.adjust_size_with_animation()
        self.play(AnimationGroup(ax2, clock.rotate(), cpu.rotate_gear()))
        self.play(AnimationGroup(FadeOut(p7), p7.animate.scale(0.1)))
        self.wait(2)

        # 11 - Simulation (4 Background Part 2)
        for _ in range(4):
            a2 = queue2_processes[1].adjust_size_with_animation()
            self.play(AnimationGroup(a2, clock.rotate(), cpu.rotate_gear()))
            self.wait(0.5)
        self.play(
            AnimationGroup(
                FadeOut(queue2_processes[1]), queue2_processes[1].animate.scale(0.1)
            )
        )

        for _ in range(2):
            a3 = queue2_processes[0].adjust_size_with_animation()
            self.play(AnimationGroup(a3, clock.rotate(), cpu.rotate_gear()))
            self.wait(0.5)
        self.play(
            AnimationGroup(
                FadeOut(queue2_processes[0]), queue2_processes[0].animate.scale(0.1)
            )
        )
        self.wait(2)
        # 12 - Fade out of all elements
        self.remove(queue1, new_queue1_text, line, new_queue2_text, queue2, cpu, clock)

    def mqs_bullet_points(self):
        # Show diffeent types of queues on the left
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

        self.wait(1)
        self.play(FadeIn(lines), run_time=4)
        self.wait(7)

        # Show bullet points on the right
        self.wait(2)
        points = [
            ("Processes are distributed to different queues", 3),
            ("Queues use different scheduling algorithms", 3),
            ("Execution of queues determind by priority", 0),
        ]

        bulletpoints = AnimatedBulletpoints(
            points, edge=self.get_to_edge(RIGHT), width=40
        )
        self.play(bulletpoints.create_animation())
        self.wait(2)

    def mqs_flow(self):
        # Sequence diagramm with process overview
        processes = [
            SequenceDiagrammProcess(
                id=1, arrival_time=0, burst_time=2, priority="high"
            ),
            SequenceDiagrammProcess(
                id=3, arrival_time=0, burst_time=1, priority="high"
            ),
            SequenceDiagrammProcess(
                id=6, arrival_time=0, burst_time=2, priority="high"
            ),
            SequenceDiagrammProcess(id=2, arrival_time=0, burst_time=1, priority="low"),
            SequenceDiagrammProcess(id=4, arrival_time=0, burst_time=5, priority="low"),
            SequenceDiagrammProcess(id=5, arrival_time=0, burst_time=3, priority="low"),
            SequenceDiagrammProcess(
                id=7, arrival_time=6, burst_time=2, priority="high"
            ),
        ]

        mlq = MultiLevelQueue(quantum=1)
        steps = schedule_processes(mlq, processes)

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
        self.wait(12)

    def mqs_pros_cons(self):
        # Positives and negatives about MLQ
        # 6s opening, 11s pos, 26s neg und rest -> 43s total

        title = CustomTitle(
            title_text="Pros and Cons of MLQ",
            corner=self.get_to_corner(UL),
        )

        cpu = CPU(size=1.75)
        cpu.move_to(
            self.get_current_center() + self.get_current_width() / 4 * RIGHT - 0.5
        )

        self.play(FadeIn(title, cpu), run_time=2)
        self.wait(4)

        positive = [
            "Reduced response time",
            "Increased throughput",
            "Better user experience",
        ]
        neutral = []
        negative = ["Increased complexity", "Risk of process starvation"]

        animated_review = AnimatedReview(
            positive,
            neutral,
            negative,
            width=90,
            left_edge=self.get_to_edge(LEFT),
            override_speed=True,
            speed=0.01,
        )
        self.play(animated_review.create_animation(), run_time=20)
        self.wait(16)

    def metrics(self):
        # Title page
        title = AnimatedTitle("Comparing Algorithms")
        self.play(
            title.create_animation(self.get_current_center(), self.get_to_corner(UL))
        )

        height_without_title = (
            (title.get_bottom() - self.get_current_center())
            + self.get_current_height() / 2
        ) * Y_AXIS
        print("height_under_title:", height_without_title)
        middle_without_title = (
            self.get_to_edge(DOWN, margin=0) + height_without_title / 2
        ) * Y_AXIS
        print("current_top", self.get_to_edge(UP, margin=0))
        print("current_center", self.get_current_center())
        print("middle_under_title:", middle_without_title)
        # self.play(title.animate.to_corner(UP + LEFT))

        # 2D LineChart metric
        stepsize_linechart = 100
        datasets = create_linechart_metrics(
            algorithms=[
                FirstComeFirstServe(),
                RoundRobin(quantum=5),
                MultiLevelQueue(quantum=5),
            ],
            stepsize=stepsize_linechart,
        )
        titles = ["FCFS", "RoundRobin", "MLQ"]
        metric_response_time = MetricResponseTime(
            datasets, titles, x_stepsize=stepsize_linechart
        ).scale(0.9, about_edge=LEFT)
        metric_response_time.next_to(
            middle_without_title + self.get_to_edge(LEFT) * X_AXIS,
            direction=RIGHT,
        )
        self.play(metric_response_time.create_animation())
        self.play(metric_response_time.animate.scale(0.5, about_edge=LEFT))

        # 2D LineChart bullet points
        points = [
            ("FCFS has the worst average turnaround time", 12),
            (
                "Round Robin and MLQ have similar average turnaround times, but Round Robin is slightly better",
                4,
            ),
            (
                "Observations can vary based on the quantum and the characteristics of the processes",
                7,
            ),
        ]
        bulletpoints = AnimatedBulletpoints(
            points,
            width=40,
            edge=self.get_to_edge(RIGHT) * X_AXIS + middle_without_title * Y_AXIS,
        )
        self.play(bulletpoints.create_animation())
        # self.play(FadeOut(bulletpoints))
        self.play(self.move_one_slide(y=DOWN))

        # Calculate metrics for bar charts
        processes = create_processes()

        fcfs_algo = FirstComeFirstServe()
        fcfs_scheduler = Scheduler()
        fcfs_scheduler.set_processes(copy.deepcopy(processes))
        fcfs_scheduler.run_algorithm(fcfs_algo, display=True)
        fcfs_metrics = fcfs_scheduler.get_metrics()

        rr_algo = RoundRobin(quantum=5)
        rr_scheduler = Scheduler()
        rr_scheduler.set_processes(copy.deepcopy(processes))
        rr_scheduler.run_algorithm(rr_algo, display=True)
        rr_metrics = rr_scheduler.get_metrics()

        mlq_algo = MultiLevelQueue(quantum=5)
        mlq_scheduler = Scheduler()
        mlq_scheduler.set_processes(copy.deepcopy(processes))
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
            y_text="Unfairness Score",
        )
        first_bar_chart.scale(0.5)

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
        second_bar_chart.scale(0.5)

        bar_charts_group = VGroup(first_bar_chart, second_bar_chart)
        bar_charts_group.arrange(DOWN, aligned_edge=LEFT)
        bar_charts_group.next_to(self.get_to_edge(RIGHT), LEFT)

        # Animate 1st BarChart
        self.wait(7)
        self.add(first_bar_chart)
        bar_grow_sequence = first_bar_chart.animate_bars(5)
        self.play(bar_grow_sequence)

        # Animate 2nd BarChart
        self.wait(10)
        self.add(second_bar_chart)
        bar_grow_sequence = second_bar_chart.animate_bars(2)
        self.play(bar_grow_sequence)
        self.wait(7)

        # Fade out the MetricResponseTime
        # self.play(FadeOut(metric_response_time))

        # Move BarCharts to the left

        self.play(
            bar_charts_group.animate.scale(0.8).next_to(
                self.get_to_edge(LEFT),
                RIGHT,
                buff=3 * DEFAULT_MOBJECT_TO_EDGE_BUFFER,
            )
        )
        self.wait(2)

        # BarChart metrics
        points = [
            ("Round Robin has the lowest (best) unfairness score", 4),
            ("FCFS and MLQ have similar scores", 5),
            ("Context switches create overhead", 2),
            ("Round Robin requires a lot of context switches", 5),
            (
                "MLQ is more efficient in this area, needing significantly fewer context switches",
                11,
            ),
        ]
        bulletpoints = AnimatedBulletpoints(
            points,
            width=40,
            edge=self.get_to_edge(RIGHT) * X_AXIS,
        )
        self.play(bulletpoints.create_animation())
        self.wait(2)

    def application(self):
        title = AnimatedTitle("Operating Systems")
        self.play(
            title.create_animation(
                center=self.get_current_center(),
                corner=self.get_to_corner(UL),
            ),
            runtime=1,
        )  # 1

        win = CustomTitle("Windows", UL)
        mac = CustomTitle("MacOS", UL)
        lin = CustomTitle("Linux", UL)

        mac.next_to(
            self.get_current_center() * X_AXIS + title.get_bottom() * Y_AXIS,
            DOWN,
            buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2,
        )
        win.next_to(
            mac,
            LEFT,
            aligned_edge=UP,
            buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2,
        )
        lin.next_to(
            mac,
            RIGHT,
            aligned_edge=UP,
            buff=DEFAULT_MOBJECT_TO_MOBJECT_BUFFER * 2,
        )
        titles_succession = Succession(FadeIn(win), FadeIn(mac), FadeIn(lin))  # 4
        self.play(titles_succession)
        # 4 Seconds

        self.wait(8)  # 12
        self.play(FadeOut(lin, run_time=1))  # 13
        self.play(
            win.animate.move_to(
                win.get_center() * Y_AXIS + self.get_current_center() * X_AXIS
            ).shift(LEFT * 3),
            mac.animate.move_to(
                mac.get_center() * Y_AXIS + self.get_current_center() * X_AXIS
            ).shift(RIGHT * 3),
        )  # 14
        # Prozesse
        win_prios = [(32, 1), (23, 2), (16, 2), (5, 1)]
        win_processes = [
            ProcessAnimated(
                color=PROCESS_COLOR, title=f"Prio {prio}", size=size, show_size=False
            )
            for prio, size in win_prios
        ]
        win_processes_group = VGroup(*win_processes)
        win_processes_group.arrange(DOWN, aligned_edge=LEFT)
        win_processes_group.next_to(win, DOWN)

        #
        mac_prios = [
            ("User-interactive", 2),
            ("User-initiated", 1),
            ("Utility", 3),
            ("Background", 1),
        ]
        mac_processes = [
            ProcessAnimated(color=PROCESS_COLOR, title=prio, size=size, show_size=False)
            for prio, size in mac_prios
        ]
        mac_processes_group = VGroup(*mac_processes)
        mac_processes_group.arrange(DOWN, center=True)
        mac_processes_group.next_to(mac, direction=DOWN)
        # 15 Seconds
        self.play(
            Succession(*[FadeIn(x, runtime=1) for x in win_processes_group])
        )  # 18
        # 29 Seconds
        self.wait(11)  # 29
        self.play(
            Succession(*[FadeIn(x, runtime=1) for x in mac_processes_group])
        )  # 33

        self.wait(3)  # 36

        self.play(FadeOut(mac_processes_group, win_processes_group))  # 37
        # 37 Seconds
        cpu = CPU(show_gear=False).move_to(self.get_current_center())
        self.play(FadeIn(cpu))  # 38
        bf = 0.01
        size = 0.5
        core1 = Square(side_length=size).next_to(self.get_current_center(), UL, buff=bf)
        core2 = Square(side_length=size).next_to(self.get_current_center(), UR, buff=bf)
        core3 = Square(side_length=size).next_to(self.get_current_center(), DL, buff=bf)
        core4 = Square(side_length=size).next_to(self.get_current_center(), DR, buff=bf)
        self.play(
            Succession(FadeIn(core1), FadeIn(core2), FadeIn(core3), FadeIn(core4))
        )  # 42

        m1 = ImageMobject("img/m1.jpg")
        i9 = ImageMobject("img/i9.jpg")
        m1.move_to(
            self.get_current_center() * Y_AXIS + mac.get_center() * X_AXIS
        ).shift(DOWN)
        i9.move_to(
            self.get_current_center() * Y_AXIS + win.get_center() * X_AXIS
        ).shift(DOWN)
        self.wait(2)  # 44
        # 44 Seconds
        self.play(FadeOut(cpu, core1, core2, core3, core4))  # 45
        self.play(FadeIn(i9))  # 46
        self.play(FadeIn(m1))  # 47
        self.wait(15)
        # 62

    def outro(self):
        # 01 - recap
        title_text = Text("OS Scheduling Algorithms", font_size=28, color=BLUE)
        # Recap of algorithms
        summary1 = Text("First Come First Serve", font_size=28)
        summary2 = Text("Round Robin", font_size=28)
        summary3 = Text("Multi Level Queue", font_size=28)
        summary = (
            VGroup(title_text, summary1, summary2, summary3)
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(self.get_to_edge(LEFT), buff=1)
        )
        self.play(Write(title_text), run_time=2)
        self.wait(3)
        self.play(Write(summary1), run_time=2)
        self.wait(3)
        self.play(Write(summary2), run_time=2)
        self.wait(4)
        self.play(Write(summary3), run_time=2)
        self.wait(4)

        # callback to opening
        # 01 - todo list
        todo = Text("My TODO List:", font_size=24)
        todo1 = Text("- Buy groceries.", font_size=24)
        todo2 = Text("- Annoy Lasse.", font_size=24)
        todo3 = Text("- Take out the trash.", font_size=24)
        todo4 = Text("- Finish AAML Homework.", font_size=24)

        todo_group = (
            VGroup(todo, todo1, todo2, todo3, todo4)
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(
                self.get_to_edge(RIGHT) * X_AXIS + summary.get_top() * Y_AXIS,
                LEFT,
                aligned_edge=UP,
                buff=2.5,
            )
        )
        self.play(Write(todo_group), run_time=4)

        # 02 - checkmarks
        check = SVGMobject("img/intro_outro/check.svg", fill_color=WHITE).scale(0.15)
        check_group = (
            VGroup(*[check.copy() for _ in range(4)])
            .arrange(DOWN, buff=0.25)
            .next_to(todo_group, direction=RIGHT)
            .shift(DOWN * 0.25)
        )
        self.play(ShowIncreasingSubsets(check_group, run_time=4))
        self.wait(2)
