"""
Talking about how acoustic sensors work.
Change in voltage results in signals
You have extremely messy data, and then you use filters to remove 
"""

from manim import *
from math import exp, cos, sin, sqrt, pi, radians
from random import random


class main(Scene):
    def construct(self):
        ax = NumberPlane(
            tips=False,
            x_range=[-3, 3, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=5,
            y_length=5,
            # x_axis_config={"numbers_to_include": np.arange(-3, 3, 1)},
            # y_axis_config={"numbers_to_include": np.arange(-1.5, 1.5, 0.5)}
        )

        box = Square(side_length=5.0)

        noisy_graph = ax.plot(
            noisy, x_range=[-3, 3], use_smoothing=True).set_color(RED_B)

        # function_label = MathTex(r"\left(\frac{1}{2\sqrt{d}}\sum_{n=1}^{d}\cos\left(2\pi\left(nx-\phi_{2}\left(n\right)\right)\right)\right)").shift(UP * 1.8 + RIGHT * 3)
        # function_label = function_label.scale(0.5)

        y_label = Text("Pressure").shift(UP * 3).scale(0.5)
        x_label = Text("Time").shift(RIGHT * 3).scale(0.5)

        self.play(Create(ax),
                  Create(box),
                  run_time=0.5)

        self.wait(1)

        self.play(Write(y_label),
                  Write(x_label),
                  run_time=0.5)

        self.wait(1)

        self.play(Create(noisy_graph), run_time=3)

        filtered_graph = ax.plot(
            filtered, x_range=[-3, 3], use_smoothing=True).set_color(GREEN_B)

        self.wait(1)

        self.play(Transform(noisy_graph, filtered_graph), run_time=3)

        # self.play(Uncreate(noisy_graph, reverse=False),
        #           Create(filtered_graph),
        #           run_time=3)
        # self.play(Create(filtered_graph),
        # run_time=3)

        group = Group(ax, box, noisy_graph, filtered_graph, y_label, x_label)
        self.wait(1)
        self.play(FadeOut(group), run_time=2)


def phi(n):
    return (1000 * cos(12345.43224 * n)) % 1


def noisy(x):
    d = 40
    multiplyer = (1 / (2 * sqrt(d)))

    sum = 0
    for n in range(d):
        sum += cos(1 * pi * (n * x - phi(n)))
        sum += random() - 0.5

    return multiplyer * sum


def filtered(x):
    return (0.5 * exp(-(x ** 2)) * sin(50 * x))