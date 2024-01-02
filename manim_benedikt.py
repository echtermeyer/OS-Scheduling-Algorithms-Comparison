from manim import *
import random
from src.components import *


class MQS_content():
    # def construct(self):
    #     self.__animation()

    def animation(self, scene):

        # headline 
        headline = Text("Multilevel Queue Scheduling", font_size=36).to_edge(UP)

        # initial lanes - width 4
        initial_rectangles = [
            Rectangle(width=5, height=1, color=BLUE),
            Rectangle(width=5, height=1, color=GREEN),
            Rectangle(width=5, height=1, color=RED)
        ]
        initial_rects_group = VGroup(*initial_rectangles).arrange(DOWN, buff=0.5)

        # final lanes - width 8
        final_rectangles = [
            Rectangle(width=8, height=1, color=BLUE),
            Rectangle(width=8, height=1, color=GREEN),
            Rectangle(width=8, height=1, color=RED)
        ]
        final_rects_group = VGroup(*final_rectangles).arrange(DOWN, buff=0.5)

        # Create arrows
        def create_arrows(rectangles):
            arrows_in = []
            arrows_out = []
            for rect in rectangles:
                start_point_in = rect.get_left() + LEFT
                end_point_in = rect.get_left()
                start_point_out = rect.get_right()
                end_point_out = rect.get_right() + RIGHT
                arrows_in.append(Arrow(start_point_in, end_point_in, buff=0))
                arrows_out.append(Arrow(start_point_out, end_point_out, buff=0))
            return VGroup(*arrows_in), VGroup(*arrows_out)

        arrows_in_group, arrows_out_group = create_arrows(initial_rectangles)

        # texts for each rectangle
        texts = [
            Text("Queue 1", font_size=26),
            Text("Queue 2", font_size=26),
            Text("Queue 3", font_size=26),
        ]

        # position texts inside rectangles
        for rect, text in zip(initial_rectangles, texts):
            text.move_to(rect.get_center())

        texts_group_queue = VGroup(*texts)

        # texts for each rectangle
        texts = [
            Text("System Processes", font_size=26),
            Text("Interactive Processes", font_size=26),
            Text("Batch Processes", font_size=26)
        ]

        # position texts inside initial rectangles
        for rect, text in zip(initial_rectangles, texts):
            text.move_to(rect.get_center())

        texts_group = VGroup(*texts)

        # Priority arrow
        priority_arrow = Arrow(UP*3, DOWN*3, buff=0.1).to_edge(LEFT)
        high_priority_text = Text("High Priority", font_size=24).next_to(priority_arrow, UP, buff=0.1)
        low_priority_text = Text("Low Priority", font_size=24).next_to(priority_arrow, DOWN, buff=0.1)
        shift_amount = RIGHT * 1
        priority_arrow.shift(shift_amount)
        high_priority_text.shift(shift_amount)
        low_priority_text.shift(shift_amount)


        # Create 8 square boxes
        squares = [Square(side_length=0.5, color=WHITE) for _ in range(8)]
        squares_group = VGroup(*squares).arrange(DOWN, buff=0.2).to_edge(LEFT, buff=1)
        

        square_assignments = [0, 2, 0, 1, 1, 2, 0, 1]

        # Reverse the order to start from the bottom
        square_assignments.reverse()

        # -- play --
        scene.play(Write(headline))
        scene.play(Create(initial_rects_group), Create(arrows_in_group), Create(arrows_out_group), run_time=5)
        scene.wait(1)

        # Display queue texts and then make them disappear
        scene.play(Write(texts_group_queue))
        scene.wait(2)
        

        # Display priority arrow and texts
        scene.play(Create(priority_arrow), Write(high_priority_text), Write(low_priority_text))
        scene.wait(2)
        scene.play(FadeOut(texts_group_queue))
        scene.play((Write(texts_group)))
        scene.wait(2)
        scene.play(FadeOut(texts_group), FadeOut(priority_arrow), FadeOut(high_priority_text), FadeOut(low_priority_text))

        # Change the width of the rectangles to 8 and adjust arrows
        new_arrows_in_group, new_arrows_out_group = create_arrows(final_rectangles)
        scene.play(
            Transform(initial_rects_group, final_rects_group),
            Transform(arrows_in_group, new_arrows_in_group),
            Transform(arrows_out_group, new_arrows_out_group)
        )
        scene.wait(2)

        # Display the square boxes
        scene.play(Create(squares_group))
        scene.wait(2)

        # Animate squares moving to rectangles
        squares_group = squares_group[::-1]
        buffer_space = 0.1  # Adjust this value for more or less space
        for i, rect_index in enumerate(square_assignments):
            target_rect = final_rectangles[rect_index]
            # Calculate horizontal offset based on how many squares are already in the rectangle
            squares_in_rect = square_assignments[:i].count(rect_index)
            horizontal_offset = LEFT * (target_rect.width / 2 - 0.25 - (0.5 + buffer_space) * squares_in_rect)
            
            target_position = target_rect.get_center() + horizontal_offset
            # Move each square to its target rectangle
            scene.play(ApplyMethod(squares_group[i].move_to, target_position))
            scene.wait(0.5)  # Wait time between each square's movement, adjust as needed

        scene.wait(4)


class MFQS_content():
    # def construct(self):
    #     self.__animation()

    def animation(self, scene):
        # headline 
        headline = Text("Multilevel Feedback Queue Scheduling", font_size=36).to_edge(UP)

        # rectangles
        rectangles = [
            Rectangle(width=4, height=1, color=BLUE),
            Rectangle(width=4, height=1, color=GREEN),
            Rectangle(width=4, height=1, color=RED),
            Rectangle(width=4, height=1, color=YELLOW)
        ]
        rects_group = VGroup(*rectangles).arrange(DOWN, buff=0.5)

        # arrows in
        arrows_in = []
        for rect in rectangles:
            start_point = rect.get_left() + LEFT
            end_point = rect.get_left()
            arrow = Arrow(start_point, end_point, buff=0)
            arrows_in.append(arrow)
        arrows_in_group = VGroup(*arrows_in)

        # arrows out
        arrows_out = []
        for rect in rectangles:
            start_point = rect.get_right()
            end_point = rect.get_right() + RIGHT
            arrow = Arrow(start_point, end_point, buff=0)
            arrows_out.append(arrow)
        arrows_out_group = VGroup(*arrows_out)


        # arrows connector
        # arrows = []
        # for i in range(len(rectangles) - 1):
        #     start_point = rectangles[i].get_right()
        #     end_point = rectangles[i + 1].get_left()
        #     arrow = Arrow(start_point, end_point, buff=0.1)
        #     arrows.append(arrow)
        # arrows_group_2 = VGroup(*arrows)


        arrows = []
        for i in range(len(rectangles) - 1):
            start_point = rectangles[i].get_right() + RIGHT * 0.5
            point1 = start_point - DOWN * (rectangles[i+1].get_top()[1] - rectangles[i].get_bottom()[1])/2
            # point2 = end_point + DOWN * (rectangles[i+1].get_top()[1] - rectangles[i].get_bottom()[1])/2
            end_point = rectangles[i + 1].get_left() + LEFT * 0.5

            path = VMobject()
            path.set_points_as_corners([start_point, point1, end_point])
            arrow = Arrow().become(path)
            arrows.append(arrow)

        arrows_group_2 = VGroup(*arrows)

        # -- play --
        scene.play(Write(headline))
        scene.play(Create(rects_group), Create(arrows_in_group), Create(arrows_out_group), Create(arrows_group_2), run_time=5)
        scene.wait(5)

# Old Version:
# class MasterScene(Scene):
#     def construct(self):
#         mqs_content = MQS_content()
#         # mfqs_content = MFQS_content()

#         mqs_content.animation(self)
#         self.clear()
#         # mfqs_content.animation(self)
#         # self.clear()
#         self.wait(1)

# New Version:

class OS(Scene):
    def construct(self):
        # creative introduction
        # 2 min
        # self.introduction()
        # 2 min
        # self.fcfs()
        # In der ÜBerleitung Preemptive verwenden und erklären was das bedeutet
        # 3 min
        # self.rr()
        # 3 min
        self.mqs()
        # 3 min
        # self.metrics()
        # reallife examples
        # 2 min
        # self.outro()

    def mqs(self):
        self.next_section(skip_animations=True)
        self.next_section()

        # 01 - Title
        title = AnimatedTitle("Multilevel Queue Scheduling")
        self.play(title.create_animation())

        # 02 - Processes
        process_sizes = [2,1,3,3,2,1,2]
        processes = [Process(size=s, title=f"P{len(process_sizes)-i}") for i, s in enumerate(process_sizes)]
        process_group = VGroup(*processes).arrange(RIGHT, buff=0.5)
        process_group.to_edge(LEFT)
        process_group.next_to(title, DOWN, aligned_edge=LEFT)
        process_group.shift(LEFT*config.frame_width)
        self.play(process_group.animate.shift(RIGHT*config.frame_width), run_time=4)

        # 03 - Queues
        line = DashedLine(LEFT * 0.5, RIGHT * 0.5, dash_length=0.005).set_length(config.frame_width - 1)
        line.move_to(ORIGIN)
        line.shift(DOWN*0.6)
        self.add(line)

        queue1 = Text("Queue 1 - High Priority", font_size=24).next_to(process_group, DOWN, aligned_edge=LEFT)
        queue1.shift(DOWN*0.1)
        self.add(queue1)

        queue2 = Text("Queue 2 - Low Priority", font_size=24).next_to(line, DOWN, aligned_edge=LEFT)
        queue2.shift(DOWN*0.1)
        self.add(queue2)
        
        self.wait(2)
        # 04 - Queues Examples
        new_queue1_text = Text("Foreground - Round Robin", font_size=24).next_to(process_group, DOWN, aligned_edge=LEFT)
        new_queue1_text.shift(DOWN*0.1)
        self.play(FadeOut(queue1))
        self.play(FadeIn(new_queue1_text))


        new_queue2_text = Text("Background - First Come, First Serve", font_size=24).next_to(line, DOWN, aligned_edge=LEFT)
        new_queue2_text.shift(DOWN*0.1)
        self.play(FadeOut(queue2))
        self.play(FadeIn(new_queue2_text))
        
        # 05 - Move Processes to Queues
        above_indexes = [0, 3, 5]
        below_indexes = [1, 2, 4, 6]
        queue1_processes = VGroup()
        queue2_processes = VGroup()

        above_initial_pos = line.get_top() + UP * 0.9 + LEFT * (config.frame_width / 2 - 1)
        below_initial_pos = line.get_bottom() + DOWN * 1.5 + LEFT * (config.frame_width / 2 - 1)

        buffer_space = 0.5

        if above_indexes:
            first_proc_above = processes[above_indexes[0]]
            self.play(first_proc_above.animate.move_to(above_initial_pos))
            last_process_position = first_proc_above.get_right()
            queue1_processes.add(first_proc_above)

            for idx in above_indexes[1:]:
                proc = processes[idx]
                self.play(proc.animate.next_to(last_process_position, RIGHT, buff=buffer_space))
                last_process_position = proc.get_right()
                queue1_processes.add(proc)

        if below_indexes:
            first_proc_below = processes[below_indexes[0]]
            self.play(first_proc_below.animate.move_to(below_initial_pos))
            last_process_position = first_proc_below.get_right()
            queue2_processes.add(first_proc_below)

            for idx in below_indexes[1:]:
                proc = processes[idx]
                self.play(proc.animate.next_to(last_process_position, RIGHT, buff=buffer_space))
                last_process_position = proc.get_right()
                queue2_processes.add(proc)


        cpu = CPU(size=0.5)
        clock = Clock(radius=0.5)
        clock.to_edge(UP + RIGHT, buff=0.3)
        cpu.next_to(clock, LEFT, buff=0.25)
        self.add(cpu, clock)

        # 06 - Simulation (1 Foreground)
        self.wait(4)
        self.play(FadeOut(queue1_processes), run_time=2)
        self.wait(2)

        # 07 - Simulation (2 Background Part 1)
        self.play(FadeOut(queue2_processes[2:4]), run_time=2)

        #TODO: proper animation of RR and FCFS
        # animation = queue1_processes[0].adjust_size_with_animation(-1)
        # self.play(AnimationGroup(animation))

        # 08 - New process while execution
        p8 = Process(size=2, title=f"P8")
        p8.next_to(title, DOWN, aligned_edge=LEFT)
        p8.shift(LEFT*config.frame_width)  
        self.play(p8.animate.shift(RIGHT*config.frame_width), run_time=4)

        # 09 - Move new process to foreground
        self.play(p8.animate.move_to(above_initial_pos))
        self.wait(2)
        # 10 - Simulation (3 Foreground Part 2 (new process))
        self.play(FadeOut(p8), run_time=2)
        self.wait(2)

        # 11 - Simulation (4 Background Part 2)
        self.play(FadeOut(queue2_processes[0:2]), run_time=2)


        # 12 - 
        self.remove(queue1, new_queue1_text, line, new_queue2_text, queue2, cpu, clock)

        # review = AnimatedReview(["nice"],["ok"], ["bad"])
        # self.play(review.create_animation())

        # After animation of algorithm (at the moment just dummy data)
        # self.clear()
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
        # sequence_diagram = SequenceDiagram("MLQ", steps=steps)
        # self.play(sequence_diagram.create_animations())
        self.wait(2)
        self.clear()
