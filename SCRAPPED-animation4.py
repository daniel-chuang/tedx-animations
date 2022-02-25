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
            background_line_style={
                "stroke_width": 0.8, "stroke_color": BLUE_D},
        ).shift(LEFT * 1.9)

        # Initializing sound circle thing (off screen)
        origin = Dot(radius=0.1, color=RED_B, z_index=1).shift(DOWN * 4)
        radius = ValueTracker(0.15)
        circle = Circle(radius=radius.get_value(), color=RED_E,
                        z_index=2).move_to(origin.get_center_of_mass())
        circle.add_updater(
            lambda x: x.become(
                Circle(radius.get_value()).move_to(origin.get_center()))
        )

        # Initializing sensor group
        sensor_group = VGroup()

        s = 0.4
        for j in [RIGHT * s, LEFT * s, UP * s * sqrt(3)]:
            dot = Dot(radius=0.16, z_index=1).shift(j)
            dot.add_updater(
                lambda x: x.set_color(GREEN_E) if abs(radius.get_value(
                ) - calculate_distance(x.get_center(), DOWN * 4)) < 0.145 else x.set_color(WHITE)
            )
            sensor_group += dot
        sensor_group = sensor_group.rotate(
            (1.5 * PI / 3), about_point=sensor_group.get_center_of_mass())
        sensor_group += Dot(sensor_group.get_center_of_mass(),
                            radius=0.8, color=GREY_B, z_index=0)

        text = Text("Using sensor to find direction of sound")
        self.play(Write(text), run_time=0.5)
        self.wait(2.5)
        self.play(Unwrite(text), run_time=0.5)

        self.play(Create(ax),
                  Create(origin),
                  Create(circle))

        self.play(FadeIn(sensor_group))

        text = Text("Sound plays").shift(RIGHT * 3).scale(0.7)
        self.play(Write(text), run_time=0.2)
        self.wait(1.4)
        self.play(Unwrite(text), run_time=0.2)

        self.play(radius.animate.set_value(6),
                  run_time=5, rate_func=rate_functions.slow_into)

        arrow = Arrow(sensor_group.get_center_of_mass(), origin.get_center(
        ) + sensor_group.get_center_of_mass() * 2, buff=0, color=GREEN_C)
        text = Text("Direction found!").shift(
            DOWN * 2 + RIGHT * 2.2).scale(0.7)

        self.play(Create(arrow),
                  Write(text), run_time=0.5)

        self.wait(2.5)


        everything = VGroup(ax, origin, circle, sensor_group, text, arrow)
        circle.clear_updaters()
        self.play(*[FadeOut(mob)for mob in self.mobjects],
                  FadeOut(circle))

        # Creating a plane
        ax2 = NumberPlane(
            tips=False,
            x_range=[-9, 9, 1],
            y_range=[-9, 9, 1],
            axis_config={"stroke_width": 0},
            background_line_style={
                "stroke_width": 0.8, "stroke_color": BLUE_D},
            x_length=18,
            y_length=18
        )

        # Initializing the origin2 sound wave
        origin2 = Dot(radius=0.1, color=RED_B, z_index=1)
        radius2 = ValueTracker(0.15)
        circle2 = circle2(radius=radius2.get_value(), color=RED_E, z_index=2)

        # Creating an updater for the sound wave
        circle2.add_updater(
            lambda x: x.become(circle2(radius2.get_value()).move_to(origin2.get_center()))
        )

        # Initializing the dot sensor groups
        s = 0.2  # half of the side length of the equilateral triangle formed by a triad of sensors
        sensor_groups2 = [VGroup(), VGroup(), VGroup()]

        for i, sensor_group2 in enumerate(sensor_groups2):
            for j in [RIGHT * s, LEFT * s, UP * s * sqrt(3)]:
                dot = Dot(z_index=1).shift(j)
                dot.add_updater(
                    #lambda x: x.set_color(GREEN_E) if radius2.get_value() > calculate_distance(x.get_center(), [0, 0, 0]) else x
                    lambda x: x.set_color(GREEN_E) if abs(radius2.get_value(
                    ) - calculate_distance(x.get_center(), origin2.get_center())) < 0.1 else x.set_color(WHITE)
                )
                sensor_group2 += dot
            sensor_group2 = sensor_group2.shift((2 + 1.8*i) * UP).rotate((2 * PI / 3) * i, about_point=[
                0, 0, 0]).rotate((1.5 * PI / 3) * (i+1), about_point=sensor_group2.get_center_of_mass())
            sensor_group2 += Dot(sensor_group2.get_center_of_mass(),
                                radius=0.4, color=GREY_B, z_index=0)

        # Animating the creation of the sound origin2
        text2 = Text("Locating the origin2 of a sound")
        self.play(Write(text2), run_time=0.5)
        self.wait(2)
        self.play(Unwrite(text2), run_time=0.2)

        text2 = Text("This dot represents an sound").shift(UP)
        self.wait(0.5)
        self.play(Write(text2), run_time=0.5)
        self.play(Create(origin2),
                  Create(circle2))
        self.wait(1)
        self.play(Unwrite(text2), run_time=0.2)

        # Animating the creation of the sensor groups
        text2 = Text("Placing sensors").shift(UP)
        self.play(Write(text2), run_time=0.5)
        self.wait(0.5)

        self.play(Create(ax2, run_time=1, lag_ratio=0.1),
                  FadeIn(sensor_groups2[0]),
                  FadeIn(sensor_groups2[1]),
                  FadeIn(sensor_groups2[2]))
        self.play(Unwrite(text2), run_time=0.2)

        # Animating the sound wave expanding, and the sensors reacting
        text2 = Text("Now sound plays").shift(UP)
        self.play(Write(text2), run_time=0.5)
        self.wait(2)
        self.play(Unwrite(text2), run_time=0.2)
        self.play(radius2.animate.set_value(7),
                  run_time=8,
                  rate_func=rate_functions.linear)

        # Animating the sensors finding the direction of the sound
        text2 = Text("Find the intersection").shift(UP)
        self.play(Write(text2), run_time=0.5)
        self.wait(2)
        self.play(Unwrite(text2), run_time=0.2)
        self.wait(1)

        arrows = VGroup()
        for i, sensor_group2 in enumerate(sensor_groups2):
            arrow = Arrow(sensor_group2.get_center_of_mass(), sensor_group2.get_center_of_mass() * (0.14 - 0.042*i), buff=0, color=GREEN_C)
            arrow.num = i
            arrow = arrow.add_updater(
                lambda x: x.become(Arrow(sensor_groups2[x.num].get_center_of_mass(), sensor_groups2[x.num].get_center_of_mass() * (0.14 - 0.042*x.num) + origin2.get_center_of_mass(), buff=0, color=GREEN_C))
            )
            arrows += arrow
        
        self.play(Create(arrows, lag_ratio=0.5), run_time=1.5)
        
        # Animating the sound wave coming back
        self.play(radius2.animate.set_value(0.15),
                  run_time=0.7)
        text2 = Text("Location identified!").shift(UP + RIGHT * 3.2)
        self.play(Write(text2), run_time=0.5)
        self.wait(2.2)
        self.play(text2.animate.become(Text("Moving the sound around...", z_index=999).shift(UP + RIGHT * 3.2).scale(0.75)))

        # Animating the arrows following everything
        # Arrow updater
        for arrow in arrows:
            arrow.clear_updaters()
            arrow = arrow.add_updater(
                    lambda x: x.become(Line(sensor_groups2[x.num].get_center_of_mass(), origin2.get_center_of_mass(), color=GREEN_C))
            )

        sound = VGroup(origin2, circle2)
        for shift in [RIGHT * 2.5, UP * 2, DL * 4.6]: # can add UP * 3 + RIGHT
            circle2.clear_updaters()
            self.play(Uncreate(arrows), run_time=0.3)
            self.play(sound.animate.shift(shift), run_time=1)

            circle2.add_updater(
                lambda x: x.become(circle2(radius2.get_value()).move_to(origin2.get_center()))
            )

            self.play(radius2.animate.set_value(8), run_time=5.5, rate_func=rate_functions.linear)
            self.play(Create(arrows), run_time=0.7)
            self.play(radius2.animate.set_value(0.15), run_time=0.2)
            self.wait(1)

        # Fading out everything
        circle2.clear_updaters()
        for arrow in arrows:
            arrow.clear_updaters()
        self.play(*[FadeOut(mob)for mob in self.mobjects])


def calculate_distance(matrix1, matrix2):
    sum = 0
    for i in range(len(matrix1)):
        sum += abs(matrix1[i] - matrix2[i]) ** 2
    return sqrt(sum)