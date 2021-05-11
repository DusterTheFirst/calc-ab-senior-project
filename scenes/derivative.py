from manim import *

# x * sin(x^{2}) + 1
def function(x):
    return x * np.sin(x ** 2) + 1


# sin(x^{2}) + 2x^{2} * cos(x^{2})
def derivative(x):
    return x * np.sin(x ** 2) + 1


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
        title_text = Text("What Is A Derivative?").set_color(ORANGE)
        subtitle_text = (
            Text("Zachary Kohnen").set_color(BLUE).scale(0.5).shift(DOWN * 0.7)
        )

        self.play(Create(title_text), Create(subtitle_text))
        self.wait(2)
        self.play(title_text.animate.to_edge(UL).scale(0.3), Uncreate(subtitle_text))
        self.wait(0.25)


        # Setup Graph

        graph_title = MathTex("f(x) = x \\times sin(x^{2}) + 1")
        self.play(Create(graph_title))
        self.wait(2)
        self.play(graph_title.animate.to_edge(UR).scale(.5))

        self.setup_axes(True)
        func_graph = self.get_graph(function, x_min=-2, x_max=3)
        self.play(Create(func_graph, run_time=1.5))

        # d1 = Dot()
        # d2 = Dot()
        # l1 = Line(d1.get_center(), d2.get_center()).set_color(ORANGE)

        x = ValueTracker(0)
        y = ValueTracker(0)

        # d1.add_updater(lambda z: z.set_x(x.get_value()))
        # d2.add_updater(lambda z: z.set_y(y.get_value()))
        # l1.add_updater(
        #     lambda z: z.become(Line(d1.get_center(), d2.get_center()).set_color(ORANGE))
        # )

        # b1 = Brace(line)
        # b1text = b1.get_text("Horizontal distance")
        # b2 = Brace(line, direction=line.copy().rotate(PI / 2).get_unit_vector())
        # b2text = b2.get_tex("x-x_1")

        self.play(x.animate.set_value(5))
        self.play(y.animate.set_value(4))
        self.wait()
