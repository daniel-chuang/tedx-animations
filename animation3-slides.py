"""
Using MORE sensors to find the location of a sound
"""
from manim import *
from math import sqrt


class main(Scene):
    def construct(self):
        # Creating a plane
        ax = NumberPlane(
            tips=False,
            x_range=[-9, 9, 1],
            y_range=[-9, 9, 1],
            axis_config={"stroke_width": 0},
            background_line_style={"stroke_width": 0.8, "stroke_color": BLUE_D},
            x_length=18,
            y_length=18,
        )

        # Initializing the origin sound wave
        origin = Dot(radius=0.1, color=RED_B, z_index=1)
        radius = ValueTracker(0.15)
        circle = Circle(radius=radius.get_value(), color=RED_E, z_index=5)

        # Creating an updater for the sound wave
        circle.add_updater(
            lambda x: x.become(
                Circle(radius.get_value(), z_index=5).move_to(origin.get_center())
            )
        )

        # Initializing the dot sensor groups
        s = 0.2  # half of the side length of the equilateral triangle formed by a triad of sensors
        sensor_groups = [VGroup(), VGroup(), VGroup()]

        for i, sensor_group in enumerate(sensor_groups):
            for j in [RIGHT * s, LEFT * s, UP * s * sqrt(3)]:
                dot = Dot(z_index=3).shift(j)
                dot.add_updater(
                    # lambda x: x.set_color(GREEN_E) if radius.get_value() > calculate_distance(x.get_center(), [0, 0, 0]) else x
                    lambda x: x.set_color(GREEN_E)
                    if abs(
                        radius.get_value()
                        - calculate_distance(x.get_center(), origin.get_center())
                    )
                    < 0.1
                    else x.set_color(WHITE)
                )
                sensor_group += dot
            sensor_group = (
                sensor_group.shift((2 + 1.8 * i) * UP)
                .rotate((2 * PI / 3) * i, about_point=[0, 0, 0])
                .rotate(
                    (1.5 * PI / 3) * (i + 1),
                    about_point=sensor_group.get_center_of_mass(),
                )
            )
            sensor_group += Dot(
                sensor_group.get_center_of_mass(), radius=0.4, color=GREY_B, z_index=2
            )

        # Animating the creation of the sound origin
        # text = Text("Locating the origin of a sound")
        # self.play(Write(text), run_time=0.5)
        # self.wait(2)
        # self.play(Unwrite(text), run_time=0.2)

        # text = Text("This dot represents an sound").shift(UP)
        # self.wait(0.5)
        # self.play(Write(text), run_time=0.5)
        self.play(FadeIn(origin), Create(circle))
        self.wait(1)
        # self.play(Unwrite(text), run_time=0.2)

        # Animating the creation of the sensor groups
        # text = Text("Placing sensors").shift(UP)
        # self.play(Write(text), run_time=0.5)
        # self.wait(0.5)

        self.play(
            Create(ax, run_time=1, lag_ratio=0.1),
            FadeIn(sensor_groups[0]),
            FadeIn(sensor_groups[1]),
            FadeIn(sensor_groups[2]),
        )
        # self.play(Unwrite(text), run_time=0.2)

        # Animating the sound wave expanding, and the sensors reacting
        # text = Text("Now sound plays").shift(UP)
        # self.play(Write(text), run_time=0.5)
        # self.wait(2)
        # self.play(Unwrite(text), run_time=0.2)
        self.play(
            radius.animate.set_value(7), run_time=8, rate_func=rate_functions.linear
        )

        # Animating the sensors finding the direction of the sound
        # text = Text("Find the intersection").shift(UP)
        # self.play(Write(text), run_time=0.5)
        # self.wait(2)
        # self.play(Unwrite(text), run_time=0.2)
        # self.wait(1)

        arrows = VGroup()
        for i, sensor_group in enumerate(sensor_groups):
            arrow = Arrow(
                sensor_group.get_center_of_mass(),
                sensor_group.get_center_of_mass() * (0.14 - 0.042 * i),
                buff=0,
                color=GREEN_C,
            )
            arrow.num = i
            arrow = arrow.add_updater(
                lambda x: x.become(
                    Arrow(
                        sensor_groups[x.num].get_center_of_mass(),
                        sensor_groups[x.num].get_center_of_mass()
                        * (0.14 - 0.042 * x.num)
                        + origin.get_center_of_mass(),
                        buff=0,
                        color=GREEN_C,
                        z_index=1,
                    )
                )
            )
            arrows += arrow

        self.play(Create(arrows, lag_ratio=0.5), run_time=1.5)

        # Animating the sound wave coming back
        self.play(radius.animate.set_value(0.15), run_time=0.7)
        text = Text("Location identified!").shift(UP + RIGHT * 3.2)
        self.play(Write(text), run_time=0.5)
        self.wait(2.2)
        self.play(
            text.animate.become(
                Text("Moving the sound around...", z_index=20)
                .shift(UP + RIGHT * 3.2)
                .scale(0.75)
            )
        )

        # Animating the arrows following everything
        # Arrow updater
        for arrow in arrows:
            arrow.clear_updaters()
            arrow = arrow.add_updater(
                lambda x: x.become(
                    Line(
                        sensor_groups[x.num].get_center_of_mass(),
                        origin.get_center_of_mass(),
                        color=GREEN_C,
                        z_index=1,
                    )
                )
            )

        sound = VGroup(origin, circle)
        for shift in [RIGHT * 2.5, UP * 2, DL * 4.6]:  # can add UP * 3 + RIGHT
            circle.clear_updaters()
            self.play(Uncreate(arrows), run_time=0.3)
            self.play(sound.animate.shift(shift), run_time=1)

            circle.add_updater(
                lambda x: x.become(
                    Circle(radius.get_value()).move_to(origin.get_center())
                )
            )

            self.play(
                radius.animate.set_value(8),
                run_time=5.5,
                rate_func=rate_functions.linear,
            )
            self.play(Create(arrows), run_time=0.7)
            self.play(radius.animate.set_value(0.15), run_time=0.2)
            self.wait(1)

        # Fading out everything
        circle.clear_updaters()
        for arrow in arrows:
            arrow.clear_updaters()
        self.play(*[FadeOut(mob) for mob in self.mobjects])


def calculate_distance(matrix1, matrix2):
    sum = 0
    for i in range(len(matrix1)):
        sum += abs(matrix1[i] - matrix2[i]) ** 2
    return sqrt(sum)
