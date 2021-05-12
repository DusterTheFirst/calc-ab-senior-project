from manim import *

# x * sin(x^{2}) + 1
def function(x):
    return x * np.sin(x ** 2) + 1


# sin(x^{2}) + 2x^{2} * cos(x^{2})
# def derivative(x):
#     return np.sin(x ** 2) + 2 * (x ** 2) * np.cos(x ** 2)


class Derivative(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            y_min=-1,
            y_max=5,
            y_labeled_nums=np.arange(-1, 5, 1),
            x_min=-2,
            x_max=3,
            x_labeled_nums=np.arange(-2, 3, 1),
            graph_origin=2 * DOWN + 1 * LEFT,
            **kwargs,
        )

    def construct(self):
        # Introduction
        title_text = Text("Derivatives From Secant Lines").set_color(ORANGE)
        subtitle_text = (
            Text("Zachary Kohnen").set_color(BLUE).scale(0.5).shift(DOWN * 0.7)
        )

        self.play(Write(title_text), Write(subtitle_text))
        self.wait(2)
        self.play(title_text.animate.scale(0.3).to_edge(UL), Unwrite(subtitle_text))
        self.wait(0.25)

        # Setup Graph

        graph_title = MathTex("f(x) = x \\times \sin(x^{2}) + 1")
        self.play(Write(graph_title))
        self.wait(2)
        self.play(graph_title.animate.to_edge(UR).scale(0.5))

        self.setup_axes(True)
        func_graph = self.get_graph(function, x_min=-2, x_max=3)
        self.play(Create(func_graph, run_time=1.5))

        intersect_dot = Dot().move_to(func_graph.points[0])
        self.add(intersect_dot)

        def line_updater(line):
            x, y = self.point_to_coords(intersect_dot.get_center())

            line.become(
                Line(2 * LEFT, 2 * RIGHT)
                .set_color(ORANGE)
                .rotate(self.angle_of_tangent(x, func_graph))
                .shift(intersect_dot.get_center())
            )

        slope_line = Line(3 * LEFT, 3 * RIGHT).set_color(ORANGE)
        line_updater(slope_line)

        self.play(Create(slope_line))

        slope_brace = Brace(
            slope_line,
            direction=rotate_vector(
                LEFT, self.angle_of_tangent(2, func_graph) - np.pi / 2
            ),
        )

        slope_brace_label = slope_brace.get_text("Line Tangent to the Curve")

        self.play(Create(slope_brace), Write(slope_brace_label))

        self.wait()

        self.play(Uncreate(slope_brace), Unwrite(slope_brace_label))

        slope_line.add_updater(line_updater)
        self.play(
            MoveAlongPath(intersect_dot, func_graph, rate_func=linear, run_time=4)
        )
        self.wait()

        self.play(Uncreate(slope_line))

        self.play(intersect_dot.animate.move_to(self.coords_to_point(1, function(1))))

        self.play(Create(slope_line))
        slope_line.remove_updater(line_updater)


        slope_text = (
            Tex(
                f"Exact slope at $x = 1$ is ${round(self.slope_of_tangent(1, func_graph), 2)}$"
            )
            .scale(0.75)
            .move_to(self.coords_to_point(1.5, 4))
        )

        self.play(Write(slope_text))

        self.play(Uncreate(slope_line), Uncreate(intersect_dot))

        secant_text = (
            Tex(
                f"Approximate slope at $x = 1$ is ",
                "$TODO$"
            )
            .scale(0.75)
            .move_to(self.coords_to_point(1.5, 3.5))
        )

        self.play(Write(secant_text))

        # d1 = Dot()
        # d2 = Dot()
        # l1 = Line(d1.get_center(), d2.get_center()).set_color(ORANGE)

        # x = ValueTracker(0)
        # y = ValueTracker(0)

        # d1.add_updater(lambda z: z.set_x(x.get_value()))
        # d2.add_updater(lambda z: z.set_y(y.get_value()))
        # l1.add_updater(
        #     lambda z: z.become(Line(d1.get_center(), d2.get_center()).set_color(ORANGE))
        # )

        # b1 = Brace(line)
        # b1text = b1.get_text("Horizontal distance")
        # b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        # b2text = b2.get_tex("x-x_1")

        # self.play(x.animate.set_value(5))
        # self.play(y.animate.set_value(4))
        self.wait()