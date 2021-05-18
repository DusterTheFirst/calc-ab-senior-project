from manim import *

# x * sin(x^{2}) + 1
def function(x):
    return x * np.sin(x ** 2) + 1


# sin(x^{2}) + 2x^{2} * cos(x^{2})
# def derivative(x):
#     return np.sin(x ** 2) + 2 * (x ** 2) * np.cos(x ** 2)


class Derivative(GraphScene, ZoomedScene):
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

        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=4,
            zoomed_display_width=4,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
            },
            **kwargs
        )

    def setup(self):
        GraphScene.setup(self)
        ZoomedScene.setup(self)

    def construct(self):
        # self.play(Write(Text("DRAFT", color="#808080", fill_opacity=.25).rotate(np.pi/4).scale(4)))

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

        slope_brace_label = slope_brace.get_text("Tangent Line")

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
            .move_to(self.coords_to_point(0, 4.5))
            .to_edge(LEFT)
        )

        self.play(Write(slope_text))

        self.play(Uncreate(slope_line), Uncreate(intersect_dot))

        secant_start = Dot().move_to(self.coords_to_point(-1, function(-1)))
        secant_end = Dot().move_to(self.coords_to_point(1, function(1)))
        secant_line = Line(
            secant_start.get_center(), secant_end.get_center()
        ).set_color(PURPLE)

        self.play(Create(secant_line), Create(secant_start), Create(secant_end))

        secant_text = (
            Tex("Approx. slope at $x = 1$ is ")
            .scale(0.75)
            .move_to(self.coords_to_point(0, 4))
            .to_edge(LEFT)
        )

        secant_slope = (
            DecimalNumber(secant_line.get_slope()).scale(0.75).next_to(secant_text, RIGHT)
        )

        secant_slope_brace = Brace(
            secant_line,
            direction=rotate_vector(
                LEFT, secant_line.get_angle() - np.pi / 2
            )
        )

        secant_slope_brace_label = secant_slope_brace.get_text("Secant Line").rotate(secant_line.get_angle())

        self.play(Create(secant_slope_brace), Write(secant_slope_brace_label))
        self.play(Write(secant_text))
        self.play(Write(secant_slope))
    
        self.wait()

        self.play(Uncreate(secant_slope_brace), Unwrite(secant_slope_brace_label))

        secant_line.add_updater(
            lambda l: l.put_start_and_end_on(
                secant_start.get_center(), secant_end.get_center()
            )
        )

        secant_slope.add_updater(lambda t: t.set_value(secant_line.get_slope()))

        func_part = self.get_graph(function, x_min=-1, x_max=0.5)

        self.play(MoveAlongPath(secant_start, func_part, rate_func=linear, run_time=4))

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        frame.add_updater(lambda f: f.move_to(secant_line.get_center()))
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        self.play(Create(frame))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation())

        func_part = self.get_graph(function, x_min=0.5, x_max=.8)

        self.play(MoveAlongPath(secant_start, func_part, rate_func=linear, run_time=4))

        self.play(frame.animate.scale(.75))

        self.wait()