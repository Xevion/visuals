from itertools import chain
from typing import Tuple, List, Optional

import manim
from manim import Scene, LEFT, BLUE, Square, RIGHT, VGroup, Text, DOWN, UP, Transform


class AddTwoNumbers(Scene):
    def construct(self):
        squares = []
        arrows = []

        nodes1 = 8640373282
        nodes2 = 1389430953

        nodes1 = list(map(int, list(reversed(str(nodes1)))))
        nodes2 = list(map(int, list(reversed(str(nodes2)))))
        group1, texts1 = self.create_list_node(nodes1)
        group2, texts2 = self.create_list_node(nodes2)
        group1.shift(UP * 2.5)
        group1.shift(RIGHT * 4)
        # group2.shift(UP * 0.5)
        group2.shift(RIGHT * 4)
        x, y = 0, 0
        carry = 0

        final = VGroup()
        previous_square: Optional[Square] = None

        # xy_text = Text(f'X: {x} Y: {y} Carry: {carry}', size=0).to_edge(UP, buff=0.1)
        xy_text = Text(f'Carry: {carry}', size=0.5).to_edge(UP, buff=0.1)
        self.add(xy_text)
        while x < len(nodes1) + 1 or y < len(nodes2) + 1:
            # new_xy_text = Text(f'X: {x} Y: {y} Carry: {carry}', size=0.5).to_edge(UP, buff=0.1)
            new_xy_text = Text(f'Carry: {carry}', size=0.5).to_edge(UP, buff=0.1)
            self.play(Transform(xy_text, new_xy_text), run_time=0.2)

            node_sum = carry
            use_carry = x == len(nodes1) and y == len(nodes2) and node_sum > 0
            if not use_carry:
                if x < len(nodes1):
                    node_sum += nodes1[x]
                if y < len(nodes2):
                    node_sum += nodes2[y]
            carry = node_sum // 10

            animations = []
            if x < len(nodes1) + 1:
                animations.append(group1.animate.shift(LEFT * 4))
                x += 1

            if y < len(nodes2) + 1:
                animations.append(group2.animate.shift(LEFT * 4))
                y += 1

            if x > 0 or y > 0:
                animations.append(final.animate.shift(LEFT * 4))

            self.play(*animations)

            if not use_carry:
                if x > len(nodes1) or y > len(nodes2):
                    continue

            square = Square(stroke_color=BLUE, stroke_width=8, fill_opacity=0, stroke_opacity=1, side_length=2)
            text = Text(str(node_sum if use_carry else node_sum % 10), size=2.6)

            animations = [manim.FadeIn(square), manim.FadeIn(text)]
            if previous_square is not None:
                arrow = manim.Arrow(previous_square.get_right(), previous_square.get_right() + (RIGHT * 2), buff=0.05)
                # arrow.shift(DOWN * 2.5)
                animations.append(manim.FadeIn(arrow))
                final.add(arrow)

            text.shift(DOWN * 2.5)
            square.shift(DOWN * 2.5)
            self.play(*animations, run_time=0.5)
            final.add(square)
            final.add(text)
            previous_square = square

            self.wait(0.25)


        self.add(group1, group2)
        self.wait(2.5)

    def create_list_node(self, nodes: List[int]) -> Tuple[VGroup, List[Text]]:
        texts = []
        squares = []
        arrows = []
        vgroup = VGroup()

        for i, node in enumerate(nodes):
            square = Square(stroke_color=BLUE, stroke_width=8, fill_opacity=0, stroke_opacity=1, side_length=2)
            text = Text(str(node), size=2.6)
            arrow = manim.Arrow(square.get_right(), square.get_right() + (RIGHT * 2), buff=0.05)

            square.shift(RIGHT * i * 4)
            text.shift(RIGHT * i * 4)
            arrow.shift(RIGHT * i * 4)

            texts.append(text)
            squares.append(square)
            if i != len(nodes) - 1:
                arrows.append(arrow)

        for object in chain.from_iterable([squares, texts, arrows]):
            vgroup.add(object)
        for text in texts:
            self.add(text)

        return vgroup, texts
