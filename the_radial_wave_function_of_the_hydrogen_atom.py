from manim import *
import numpy as np
from IPython.display import Video, display
import subprocess
import os

class RadialWavefunctions(Scene):
    def construct(self):
        # Define the radial wavefunctions
        functions = [
            ("1,0", lambda r: 2 * np.exp(-r)),
            ("2,0", lambda r: (1 / np.sqrt(2)) * (1 - r/2) * np.exp(-r/2)),
            ("2,1", lambda r: (1 / np.sqrt(24)) * (r) * np.exp(-r/2)),
            ("3,0", lambda r: 2/np.sqrt(27) * (1 - 2*r/3 + 2*r**2/27) * np.exp(-r/3)),
            ("3,1", lambda r: 8/(27*np.sqrt(6)) * (1 - r/6) * (r) * np.exp(-r/3)),
            ("3,2", lambda r: 4/(81*np.sqrt(30)) * (r**2) * np.exp(-r/3)),
        ]

        # Define the axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-0.2, 2, 0.5],
            x_length=6,
            y_length=8,
            tips=False,
            axis_config={"color": WHITE, "include_ticks": True, "tick_size": 0.05, "stroke_width": 0.5}
        )
        axes.move_to(ORIGIN)

        axis_labels = axes.get_axis_labels(x_label="\\frac{r}{a_0}", y_label="R_{nl}")
        axis_labels[0].scale(0.50)
        axis_labels[1].scale(0.75)

        title = Text("The Radial Wave Function", font_size=24, weight=BOLD).move_to(5.5*UP)
        subtitle = Text("of a Hydrogen Atom", font_size=20, color=BLUE_C).next_to(title, DOWN, buff=0.1)

        gradient_colors = [BLUE_E, PURPLE_E, PINK, RED_E]
        title.set_color_by_gradient(gradient_colors)
        underline = Underline(title, stroke_width=3, stroke_opacity=0.5, stroke_color=gradient_colors, buff=0.1)

        R_nl = MathTex(
            r"R_{nl}(r) = -\sqrt{\left(\frac{2}{na_0}\right)^3 \frac{(n-l-1)!}{2n[(n+l)!]^3}} \left(\frac{2r}{na_0}\right)^l e^{-r/na_0} L_{n-l+1}^{2l+1}\left(\frac{2r}{na_0}\right)",
            font_size=24, color=WHITE
        ).move_to(2.5*UP)

        note1 = Tex("where associated ", font_size=24).next_to(R_nl, 4.5*DOWN).shift(2*LEFT)
        note2 = Tex("Laguerre polynomials:", font_size=24).next_to(note1, DOWN)
        L_s = MathTex(
            r"L_s^r(x) = \sum_{q=0}^s (-1)^q \frac{(s+r)!^2}{(s-q)!(r+q)!} \frac{x^q}{q!}",
            font_size=24
        ).next_to(note2, DOWN).shift(3*RIGHT)

        expressions = [
            MathTex(r"R_{1,0}(r) = 2a_0^{-3/2} e^{-r/a_0}", color=BLUE_C, font_size=28).move_to(3.5*UP + 2*RIGHT),
            MathTex(r"R_{2,0}(r) = \frac{1}{\sqrt{2}} a_0^{-3/2} \left(1 - \frac{r}{2a_0}\right) e^{-r/2a_0}", color=GREEN_C, font_size=24).move_to(3.5*UP + 2*RIGHT),
            MathTex(r"R_{2,1}(r) = \frac{1}{\sqrt{24}} a_0^{-3/2} \frac{r}{a_0} e^{-r/2a_0}", color=GOLD_C, font_size=24).move_to(3.5*UP + 2*RIGHT),
            MathTex(r"R_{3,0}(r) = \frac{2}{\sqrt{27}} a_0^{-3/2} \left(1 - \frac{2r}{3a_0} + \frac{2r^2}{27a_0^2}\right) e^{-r/3a_0}", color=RED_C, font_size=22).move_to(3.5*UP + 2*RIGHT),
            MathTex(r"R_{3,1}(r) = \frac{8}{27\sqrt{6}} a_0^{-3/2} \left(1 - \frac{r}{6a_0}\right) \frac{r}{a_0} e^{-r/3a_0}", color=ORANGE, font_size=22).move_to(3.5*UP + 2*RIGHT),
            MathTex(r"R_{3,2}(r) = \frac{4}{81\sqrt{30}} a_0^{-3/2} \frac{r^2}{a_0^2} e^{-r/3a_0}", color=PINK, font_size=22).move_to(3.5*UP + 2*RIGHT)
        ]

        # Animation sequence
        self.play(Write(VGroup(title, subtitle, underline), lag_ratio=0.0))
        self.wait(0.5)
        self.play(Write(VGroup(R_nl, note1, note2, L_s)))
        self.wait(0.5)
        self.play(VGroup(R_nl, note1, note2, L_s).animate.set_color_by_gradient(gradient_colors))
        self.wait(0.5)
        self.play(Transform(VGroup(R_nl, note1, note2, L_s), VGroup(axes, axis_labels)))
        self.wait(0.5)
        self.play(Write(expressions[0]), run_time=0.5)
        self.wait(0.5)

        x_start = 0
        y_start = -2.5
        colors = [BLUE_C, GREEN_C, GOLD_C, RED_C, ORANGE, PINK]

        for i, (label, func) in enumerate(functions):
            graph = axes.plot(func, color=colors[i % len(colors)], stroke_width=2)
            graph_label = MathTex(f"R_{{{label}}}(r)", color=colors[i % len(colors)], font_size=24).move_to(axes.c2p(x_start + 1.5 * i, y_start))

            if i < len(functions) - 1:
                self.play(Write(VGroup(graph, graph_label)), run_time=0.8)
                self.play(Transform(expressions[0], expressions[i + 1]), run_time=0.5)
                self.wait(0.3)
            else:
                self.play(Write(VGroup(graph, graph_label)), run_time=0.8)
                self.wait(0.5)

        self.wait(2)

# Render using command line to force portrait mode
if __name__ == "__main__":
    # Method 1: Try direct rendering with config
    from manim import config as manim_config

    # Override config
    manim_config.frame_width = 9
    manim_config.frame_height = 16
    manim_config.pixel_height = 1920
    manim_config.pixel_width = 1080

    scene = RadialWavefunctions()
    scene.render()

    video_path = scene.renderer.file_writer.movie_file_path

    # Check the actual dimensions
    import subprocess
    try:
        result = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
                                video_path], capture_output=True, text=True)
        dimensions = result.stdout.strip()
        print(f"Actual video dimensions: {dimensions}")
    except:
        pass

    display(Video(video_path, embed=True))
