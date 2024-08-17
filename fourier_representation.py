from manim import*
import numpy as np

config.frame_width = 9  
config.frame_height = 16

config.pixel_height = 1920  # Set the final output video height to 1920 pixels
config.pixel_width = int(config.pixel_height * (config.frame_width / config.frame_height))  

class Fourierrepresentation(Scene):
    def construct(self):
        # self.camera.background_color = GOLD_A
        axes = Axes(
            x_range=[-np.pi, np.pi, np.pi/2],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=8,
            tips = False,
            axis_config={"color": GRAY_B,
            "include_ticks":True, "tick_size":0.05, 
            "stroke_width":2}).move_to(2*DOWN)
        font_size = 30

        x_tick_labels = VGroup(  
            MathTex(r"-\pi", font_size=font_size).move_to(axes.c2p(-np.pi, 0) + DOWN * 0.2).set_color(GRAY_A),  
            MathTex(r"-\frac{\pi}{2}", font_size=font_size).move_to(axes.c2p(-np.pi / 2, 0) + DOWN * 0.4).set_color(GRAY_A),  
            MathTex(r"\frac{\pi}{2}", font_size=font_size).move_to(axes.c2p(np.pi / 2, 0) + DOWN * 0.4 + RIGHT * 0.2).set_color(GRAY_A),  
            MathTex(r"\pi", font_size=font_size).move_to(axes.c2p(np.pi, 0) + DOWN * 0.2 + RIGHT * 0.2).set_color(GRAY_A),  
        )  

        y_tick_labels1 = VGroup(*[MathTex(str(y), font_size=font_size, color=GRAY_A).move_to(axes.c2p(0, y) + LEFT * 0.2) for y in range(1, 4)])  
        y_tick_labels2 = VGroup(*[MathTex(str(y), font_size=font_size, color=GRAY_A).move_to(axes.c2p(0, y) + LEFT * 0.4) for y in range(-3, 0)])  

        axis_labels = axes.get_axis_labels(x_label = "x", y_label = "v(x)")
        axis_labels[0].set_color(GRAY_B)
        axis_labels[1].set_color(GRAY_B)
 

        title = Tex("Fourier Series", font_size=50).move_to(6*UP)
        text1 = Text(  
            "Find the Fourier representation of the square \n"  
            "wave signal defined as shown in the graph:",  
            font="Times New Roman",  
            font_size=30,  
            color=GRAY_B,
            line_spacing=1.0  
        ).next_to(title, 5*DOWN)         
        gradient_colors = [BLUE, TEAL, GREEN, YELLOW, GREEN, TEAL, BLUE]
        underline = Underline(title,stroke_width = 5, stroke_opacity=0.5,  buff=0.1)
        title.set_color_by_gradient(
            gradient_colors
        )
        underline.set_color_by_grandient(gradient_colors)
        text2 = Text( "Now let's find the fourier series of v(x)",  
            font="Times New Roman",  
            font_size=40) 
        text2.set_color_by_grandient(gradient_colors)

        def piecewise_function(x):  
            if -np.pi < x < -np.pi / 2:  
                return -2  
            elif -np.pi / 2 < x < np.pi / 2:  
                return 2  
            elif np.pi / 2 < x < np.pi:  
                return -2  
            else:  
                return None  # For values outside the defined range
        
        stroke_width= 4
        colorg = BLUE_E


        points = [
            -np.pi, 0,
            -np.pi, -2,
            -np.pi/2, -2,
            -np.pi/2, 2,
            np.pi/2, 2,
            np.pi/2, -2,
            np.pi, -2,
            np.pi, 0
        ]
        
        lines = VGroup()
        for i in range(0, len(points)-2, 2):
            start = axes.c2p(points[i], points[i+1])
            end = axes.c2p(points[(i+2) % len(points)], points[(i+3) % len(points)])
    
            if start[0] == end[0]:  # Vertical line
                line = DashedLine(start=start, end=end, color=colorg, stroke_width=stroke_width)
            else:  # Horizontal line
                line = Line(start=start, end=end, color=colorg, stroke_width=stroke_width)

            lines.add(line)       
 
        vx = MathTex(r"v(x) = \frac{8}{\pi} \sum_{n=0}^{\infty} \frac{(-1)^n}{2n + 1} \cos((2n+1)x)", font_size=40).move_to(text1, 0.1 * DOWN)
        rect = SurroundingRectangle(vx, color=YELLOW, stroke_width=2)
        n = 0
        nTex = Tex(fr"n = {n}", font_size=40, color = GRAY_A).move_to(axes.c2p(-np.pi/2, 3))

        def getSum(a, l, x):
            result = 0
            for n in range(0, a + 1):
                expr = ((-1)**n/(2*n + 1)) * (np.cos((2*n + 1) * x))
                result += expr
            return result

        fourierFunc = lambda x: (8/PI) * getSum(0, 1, x)
        
        graph = axes.plot(fourierFunc, color=BLUE)

        vx1 = MathTex(  
                r"v(x) = \begin{cases} "  
                r"-2 & \text{if } -\pi < x < -\frac{\pi}{2} \\"  
                r" 2 & \text{if   } -\frac{\pi}{2} < x < \frac{\pi}{2} \\"  
                r"-2 & \text{if } \frac{\pi}{2} < x < \pi "  
                r"\end{cases}"  
                ).move_to(axes, 2 * DOWN).set_color(GREEN)
        
        rect1 = SurroundingRectangle(vx1, color=YELLOW, stroke_width=2)

        part1 = vx1[0][0:10]
        part2 = vx1[0][10:23]
        part3 = vx1[0][23:36]
        part4 = vx1[0][36:] #47
        target1 = y_tick_labels2[1]
        target2 = x_tick_labels[0]
        target3 = x_tick_labels[1]
        target4 = y_tick_labels1[1]
        target5 = x_tick_labels[2]
        target6 = x_tick_labels[3]

        # the animation
        # first part
        self.add(title, underline)
        self.play(Write(text1))
        self.play(Create(VGroup(axes, axis_labels, lines)))
        self.play(Create(VGroup( x_tick_labels, y_tick_labels1, y_tick_labels2)))
  
        self.play(VGroup(axes, axis_labels, x_tick_labels, y_tick_labels1, y_tick_labels2, lines).animate.next_to(underline, 
                                                            DOWN),
                    Unwrite(text1), 
                    run_time = 1,
                    lag_ratio = 0.0)    
        
        self.play(Write(part1))
        self.play(FadeIn(part2[0:2], target_position = target1, run_time = 0.5))
        self.play(Write(VGroup(part2[2:4], part2[6:9]), run_time = 0.5))
        self.play(FadeIn(part2[4:6], target_position = target2),
                  FadeIn(part2[9:], target_position = target3),
                  run_time = 0.5)
        self.play(FadeIn(part3[0], target_position = target4, run_time = 0.5))
        self.play(Write(VGroup(part3[1:3], part3[7:10]), run_time = 0.5))
        self.play(FadeIn(part3[3:7], target_position = target3),
                  FadeIn(part3[10:], target_position = target5),
                  run_time = 0.5)
        self.play(FadeIn(part4[0:2], target_position = target1, run_time = 0.5))
        self.play(Write(VGroup(part4[2:4], part4[7:10]), run_time = 0.5))
        self.play(FadeIn(part4[4:7], target_position = target5),
                  FadeIn(part4[10:], target_position = target6),
                  run_time = 0.5)
        self.play(Circumscribe(vx1, fade_out = True, stroke_width = 2))
        self.add(rect1)
        self.play(FadeOut(VGroup(axes, axis_labels, x_tick_labels, y_tick_labels1, y_tick_labels2, lines), target_postion = title),
                  VGroup(vx1, rect1).animate.next_to(title, 4*DOWN))
        self.play(Create(text2))
        self.wait()
        self.play(FadeOut(Group(*self.mobjects), run_time = 0.5))
        
        # second part
        self.play(Create(VGroup(title, underline, axes, axis_labels, lines,x_tick_labels, y_tick_labels1, y_tick_labels2))) 
        self.play(Write(vx), run_time = 0.5)
        self.play(Circumscribe(vx, fade_out = True, stroke_width = 2), run_time = 0.5)
        self.add(rect)
        self.play(Write(VGroup(nTex, graph)))

        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9,10, 11, 12, 13, 14, 15, 25, 30,50,70,80, 100]:
            self.play(ReplacementTransform(nTex, nTex := Tex(fr"n = {i}", font_size=40, color = GRAY_A).move_to(axes.c2p(-np.pi/2, 3))),
                      ReplacementTransform(graph, graph := axes.plot(lambda x: (8/PI) * getSum(i, 1, x), color=BLUE)))

        self.wait()

