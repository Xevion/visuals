from typing import List

from manim import *
from palettable.matplotlib import Inferno_20


class BubbleSort(Scene):
    """
    A animation of Bubble Sort sorting algorithm.

    Very simple, a arrangement of boxes containing singular digits within them, slowly swapping values until
    the array is sorted in increasing order.
    """

    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)

        self.array = [3, 8, 3, 6, 6, 4, 1, 4, 8, 4, 2, 7, 9, 8, 6, 8]
        self.squares: List[VGroup] = []
        self.entire = VGroup()
        self.size_multiplier = (14 - 1.5) / len(self.array)
        self.arrow_cur = 0
        self.arrow_shown = False

    def construct(self):
        """Main method."""

        self.assemble()
        self.add(self.entire)
        self.entire.to_edge(LEFT, buff=0.75)

        running = True
        while running:
            running = self.tick()

    def assemble(self):
        """Assemble all animation elements"""
        max_value = max(self.array)
        min_value = min(self.array)
        for i, value in enumerate(self.array):
            square = VGroup()
            value_interpolation = (value - min_value) / (max_value - min_value)
            # color = colour.Color(hsl=(, 1, 0.5)).get_hex_l()
            colors = Inferno_20.hex_colors
            stroke = Square(stroke_color=colors[int(value_interpolation * (len(colors) - 1 - 3)) + 3],
                            stroke_width=8 * self.size_multiplier, fill_opacity=0, stroke_opacity=1,
                            side_length=self.size_multiplier)
            digit = Text(str(value), size=1.3 * self.size_multiplier)

            square.add(stroke, digit)
            square.shift(RIGHT * self.size_multiplier * i)

            self.entire.add(square)
            self.squares.append(square)

        bottom = self.squares[0].get_bottom()
        self.arrow = Arrow(bottom + DOWN * self.size_multiplier, bottom, buff=0, fill_opacity=0)
        self.entire.add(self.arrow)

    def tick(self) -> bool:
        """
        Animates a single tick of the Bubble Sort sorting algorithm, swapping one value with another at most.

        :return: True if anything was swapped, otherwise False.
        """
        for i in range(len(self.array) - 1):
            if not self.arrow_shown and i == 0:
                self.move_arrow(i, time=0)
                self.show_arrow(True)
            if self.array[i] > self.array[i + 1]:
                self.move_arrow(i + 0.5, time=0.10 * i)
                self.swap(i, i + 1)
                self.show_arrow(False)
                self.wait(0.2)
                self.array[i], self.array[i + 1] = self.array[i + 1], self.array[i]
                self.squares[i], self.squares[i + 1] = self.squares[i + 1], self.squares[i]
                return True

        return False

    def move_arrow(self, i, time: float = 0.15) -> None:
        """Move the arrow to a specific position around the array."""
        shift = RIGHT * (i - self.arrow_cur) * self.size_multiplier
        if time == 0:
            self.arrow.shift(shift)
        else:
            self.play(self.arrow.animate.shift(shift), run_time=time, rate_func=rate_functions.ease_in_out_sine)
        self.arrow_cur = i

    def show_arrow(self, val: bool = True) -> None:
        """Show or hide the arrow via it's opacity."""
        self.play(
            self.arrow.animate.set_opacity(1 if val else 0),
            run_time=0.05
        )

    def swap(self, x: int, y: int) -> None:
        """Swaps two positions in the array with each other."""
        dir = x < y
        diff = abs(x - y) * self.size_multiplier
        self.play(
            self.squares[x].animate.shift(UP * self.size_multiplier * 1.1),
            self.squares[y].animate.shift(DOWN * self.size_multiplier * 1.1),
            run_time=0.12
        )

        self.play(
            self.squares[x].animate.shift((RIGHT if dir else LEFT) * diff),
            self.squares[y].animate.shift((LEFT if dir else RIGHT) * diff),
            run_time=0.2
        )

        self.play(
            self.squares[x].animate.shift(DOWN * self.size_multiplier * 1.1),
            self.squares[y].animate.shift(UP * self.size_multiplier * 1.1),
            run_time=0.12
        )
        pass

    def change_digit(self, pos: int, val: int) -> None:
        """Change the digit present at a specific position in the array."""
        pass
