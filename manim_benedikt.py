from manim import *
import random


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



class MasterScene(Scene):
    def construct(self):
        mqs_content = MQS_content()
        # mfqs_content = MFQS_content()

        mqs_content.animation(self)
        self.clear()
        # mfqs_content.animation(self)
        # self.clear()
        self.wait(1)

