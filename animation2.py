"""
Using sensors to find the direction of a sound
"""
from manim import *
from math import *


class main(Scene):
    def construct(self):

        # Initializing background plane
        ax = NumberPlane(
            x_range=[0, 10.1, 1],  # 7.1 base
            y_range=[0, 4, 1],
            x_length=20.2,  # 14.2 base width
            y_length=8,
            axis_config={"stroke_width": 0.4, "color": BLUE_D},
            background_line_style={"stroke_width": 0.8, "stroke_color": BLUE_D},
            z_index=0,
        ).shift(LEFT * 1.9)

        # Initializing sound circle thing (off screen)
        origin = Dot(radius=0.1, color=RED_B).shift(DOWN * 4)
        radius = ValueTracker(0.15)
        circle = Circle(radius=radius.get_value(), color=RED_E, z_index=1).move_to(
            origin.get_center_of_mass()
        )
        circle.add_updater(
            lambda x: x.become(
                Circle(radius.get_value(), z_index=1).move_to(origin.get_center())
            )
        )

        # Initializing sensor group
        sensor_group = VGroup(z_index=2)
        text_group = VGroup(z_index=3)

        s = 0.4
        for i, j in enumerate([LEFT * s, UP * s * sqrt(3), RIGHT * s]):
            dot = Dot(radius=0.16).shift(j)
            dot.add_updater(
                lambda x: x.set_color(GREEN_E)
                if abs(
                    radius.get_value() - calculate_distance(x.get_center(), DOWN * 4)
                )
                < 0.145
                else x.set_color(WHITE)
            )
            sensor_group += dot
            text_group += (
                Text(str(i + 1), color=BLACK)
                .move_to(dot.get_center())
                .scale(0.5)
                .rotate(-PI / 2)
            )
        sensor_group = sensor_group.rotate(
            (1.5 * PI / 3), about_point=sensor_group.get_center_of_mass()
        )
        sensor_origin = Dot(sensor_group.get_center_of_mass(), radius=0.8, color=GREY_B)
        text_group = text_group.rotate(
            (1.5 * PI / 3), about_point=sensor_group.get_center_of_mass()
        )

        # text = Text("Using sensor to find direction of sound")
        # self.play(Write(text), run_time=0.5)
        # self.wait(2.5)
        # self.play(Unwrite(text), run_time=0.5)

        self.play(Create(ax), Create(origin), Create(circle))

        self.play(FadeIn(sensor_origin), FadeIn(sensor_group))
        self.play(Write(text_group))

        # text = Text("Sound plays").shift(RIGHT * 3).scale(0.7)
        # self.play(Write(text), run_time=0.2)
        # self.wait(1.4)
        # self.play(Unwrite(text), run_time=0.2)

        self.play(
            radius.animate.set_value(6), run_time=5, rate_func=rate_functions.slow_into
        )

        print(sensor_group.get_center())
        arrow = Arrow(
            sensor_group.get_center_of_mass(),
            origin.get_center() + sensor_group.get_center_of_mass() * 2,
            buff=0,
            color=GREEN_C,
        )
        text = Text("Direction found!").shift(DOWN * 2 + RIGHT * 2.2).scale(0.7)

        self.play(Create(arrow), Write(text), run_time=0.5)

        self.wait(2.5)

        self.play(*[FadeOut(mob) for mob in self.mobjects], FadeOut(circle))


def calculate_distance(matrix1, matrix2):
    sum = 0
    for i in range(len(matrix1)):
        sum += abs(matrix1[i] - matrix2[i]) ** 2
    return sqrt(sum)
