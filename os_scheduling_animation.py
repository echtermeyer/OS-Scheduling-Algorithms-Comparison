from manim import *
from src.components import *


class CustomMovingCameraScene(MovingCameraScene):
    """Custom Class used to extend the MovingCameraScene class from manimlib with a lot of methods to get the current camera position

    Args:
        MovingCameraScene (_type_): _description_
    """

    def construct(self):
        pass

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
        self, edge: np.ndarray, margin: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER
    ) -> np.ndarray:
        """Used to get the position of the edge of the camera frame with a margin

        Args:
            edge (np.ndarray): This is the edge of the camera frame that should be returned (e.g. LEFT, RIGHT, UP, DOWN)
            margin (float, optional): This is how far from the edge the center of the returned position should be. Defaults to DEFAULT_MOBJECT_TO_EDGE_BUFFER.

        Returns:
            np.ndarray: position of the edge of the camera frame with a margin
        """
        if np.array_equal(edge, UP):
            return self.get_edge(UP) + DOWN * margin
        if np.array_equal(edge, DOWN):
            return self.get_edge(DOWN) + UP * margin
        if np.array_equal(edge, LEFT):
            return self.get_edge(LEFT) + RIGHT * margin
        if np.array_equal(edge, RIGHT):
            return self.get_edge(RIGHT) + LEFT * margin
        return None

    def get_to_corner(
        self,
        corner: np.ndarray,
        x_margin: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER,
        y_margin: float = DEFAULT_MOBJECT_TO_EDGE_BUFFER,
    ) -> np.ndarray:
        """Used to get to a specific corner of the camera frame with a margin
        Args:
            corner (np.ndarray): The desired corner
            x_margin (float, optional): the margin on the X-Axis. Defaults to DEFAULT_MOBJECT_TO_EDGE_BUFFER.
            y_margin (float, optional): the margin on the Y-Axis. Defaults to DEFAULT_MOBJECT_TO_EDGE_BUFFER.

        Returns:
            np.ndarray: position of the corner of the camera frame with a margin
        """
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
        # creative introduction
        # 2 min
        self.wait(1)
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
        self.fcfs_animation()
        self.fcfs_bullet_points()
        self.fcfs_flow()
        self.fcfs_pros_cons()

    def fcfs_animation(self):
        title = AnimatedTitle("FirstComeFirstServe")
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
        CPU_RIGHT = np.array(cpu.get_right() + RIGHT * faktor)

        PROCESS_POLE_POSITION = (
            Process()
            .move_to(CPU_RIGHT * X_AXIS + self.get_to_edge(DOWN, margin=1) * Y_AXIS)
            .get_center()
        )
        # initialize the RoundRobin object
        quantum = 1
        fcfs = AlgorithmAnimation(quantum, type="fcfs")

        self.play(FadeIn(cpu))
        self.wait(2)

        process_sizes = [2, 3, 5, 1, 1, 2]

        # create processes and place them just outside the left edge
        for i, size in enumerate(process_sizes):
            process = (
                Process(title=f"P{i+1}", size=size)
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
        while not fcfs.get_empty():
            # calculate the arc from current process next to cpu

            if cpu_empty:
                arc_to_cpu = ArcBetweenPoints(
                    fcfs.process_queue[0].get_center(), CPU_RIGHT, angle=TAU / 4
                )
                # move current process next to cpu
                self.play(MoveAlongPath(fcfs.process_queue[0], arc_to_cpu))

                # animate queue
                animation = fcfs.move_queue(
                    pole_position=PROCESS_POLE_POSITION,
                    first_process_in_cpu=True,
                    duration=1,
                )
                # the animation might return None if the queue is empty
                if animation is not None:
                    self.play(animation)

            # process
            cpu_empty, animation = fcfs.run()
            self.play(AnimationGroup(animation, clock.rotate(), cpu.rotate_gear()))

    def fcfs_bullet_points(self):
        pass

    def fcfs_flow(self):
        pass

    def fcfs_pros_cons(self):
        pass

    def rr(self):
        self.play(self.move_one_slide(x=RIGHT))
        self.rr_animation()
        self.wait(1)

        # self.play(self.move_one_slide(x=RIGHT))
        self.rr_bullet_points()
        self.wait(1)

        self.play(self.move_one_slide(y=DOWN))
        self.rr_flow()
        self.wait(1)

        self.play(self.move_one_slide(x=RIGHT))
        self.rr_pros_cons()

    def rr_animation(self):
        # create and animate title for RoundRobin
        title = AnimatedTitle("RoundRobin")
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
            Process()
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
                Process(title=f"P{i+1}", size=size)
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

        self.play(FadeOut(clock))
        for i, size in enumerate(process_sizes):
            process = (
                Process(title=f"P{i+1}", size=size)
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
        pass

    def rr_pros_cons(self):
        pass

    def mqs(self):
        self.mqs_animation()
        self.mqs_bullet_points()
        self.mqs_flow()
        self.mqs_pros_cons()

    def mqs_animation(self):
        # Code for animating the MQS process
        pass

    def mqs_bullet_points(self):
        pass

    def mqs_flow(self):
        # Code to demonstrate the flow of processes in MQS
        pass

    def mqs_pros_cons(self):
        # Code to analyze and present the advantages and disadvantages of MQS
        pass

    def metrics(self):
        pass

    def outro(self):
        pass
