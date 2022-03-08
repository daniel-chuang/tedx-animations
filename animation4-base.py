"""
Giving an introductory animation on how sound waves work.
"""
from pickle import TRUE
from manim import *
from math import *


class main(Scene):
    def construct(self):
        # Making a speaker
        speaker_rect = Rectangle(width=2, height=3)
        speaker_circle_top = Circle(radius=0.2, color=WHITE).shift(UP * 1)
        speaker_circle_bottom_inner = Circle(radius=0.15, color=WHITE).shift(DOWN * 0.5)
        speaker_circle_bottom_outer = Circle(radius=0.8, color=WHITE).shift(DOWN * 0.5)
        speaker_circle_bottom_arc = Arc(radius=0.5, angle=PI / 2).shift(DOWN * 0.5)
        speaker_leg_1_vert = Line(
            speaker_rect.get_bottom() + LEFT * 0.7,
            speaker_rect.get_bottom() + LEFT * 0.7 + DOWN * 0.25,
        )
        speaker_leg_2_vert = Line(
            speaker_rect.get_bottom() + RIGHT * 0.7,
            speaker_rect.get_bottom() + RIGHT * 0.7 + DOWN * 0.25,
        )
        speaker_leg_1_hor = Line(
            speaker_leg_1_vert.get_bottom() + LEFT * 0.12,
            speaker_leg_1_vert.get_bottom() + RIGHT * 0.12,
        )
        speaker_leg_2_hor = Line(
            speaker_leg_2_vert.get_bottom() + LEFT * 0.12,
            speaker_leg_2_vert.get_bottom() + RIGHT * 0.12,
        )
        speaker = VGroup(
            speaker_rect,
            speaker_circle_top,
            speaker_circle_bottom_inner,
            speaker_circle_bottom_outer,
            speaker_leg_1_vert,
            speaker_leg_2_vert,
            speaker_leg_1_hor,
            speaker_leg_2_hor,
            speaker_circle_bottom_arc,
        )
        speaker.scale(0.6).shift(DOWN * 2)
        self.play(Create(speaker))

        # sound waves
        ax = NumberPlane(
            x_range=[-PI, PI, 0.1],
            y_range=[-1, 1, 0.1],
            x_length=14.2,
            y_length=1,
            axis_config={"stroke_width": 0, "color": BLUE_D},
            background_line_style={"stroke_width": 0},
        )
        self.add(ax)

        # Graph
        f = ValueTracker(107.99)
        wave = ax.plot(
            lambda x: sin(10 * x), x_range=[-PI, PI], use_smoothing=True
        ).shift(UP * 1)
        wave.add_updater(
            lambda x: x.become(
                ax.plot(
                    lambda x: sin(f.get_value() * x),
                    x_range=[-PI, PI],
                    use_smoothing=True,
                ).shift(UP * 1)
            )
        )

        # Sound wave circles
        circle1 = Circle(radius=0).shift(DOWN * 2.35)
        circle1.add_updater(lambda x: func(x, f, 0))
        circle2 = Circle(radius=0).shift(DOWN * 2.35)
        circle2.add_updater(lambda x: func(x, f, 1))
        circle3 = Circle(radius=0).shift(DOWN * 2.35)
        circle3.add_updater(lambda x: func(x, f, 2))
        circles = VGroup(circle1, circle2, circle3)
        self.add(circle1)

        # Animating
        self.play(Create(wave))
        for i in range(53):
            if i == 3:
                self.add(circle2)
            if i == 6:
                self.add(circle3)
            self.play(
                f.animate.set_value(f.get_value() - 2), run_time=0.2, rate_func=linear
            )

        # Cleanup animations
        for mob in self.mobjects:
            mob.clear_updaters()
        self.play(circles.animate.set_fill(opacity=0), run_time=0.2)
        self.play(Uncreate(speaker), Uncreate(circles), Uncreate(wave), run_time=1.2)
        self.wait(0.5)


def func(x, f, i):
    if f.get_value() < 108:
        radius = 3 - ((f.get_value() / (300 / f.get_value()) - i * 4) % 3)
        return x.become(
            Circle(radius=radius)
            .shift(DOWN * 2.35)
            .set_stroke(RED, opacity=1 - radius / 3)
        ).set_fill(RED, opacity=(1 - radius / 3) / 2)
    return x
