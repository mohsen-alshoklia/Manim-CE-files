from manim import*

# Create a custom class that inherits from ThreeDScene and contains all the Mobjects, 
# and the coordinate system as attributes
class CustomSceneSOR(ThreeDScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mobject1 = Circle()
        self.mobject2 = Square()
        self.axes = ThreeDAxes(
            x_range=[0, 12, 1],
            y_range=[-8, 8, 1],
            z_range = [-8, 8, 1],
            x_length=7.2,
            y_length=6,
            z_length = 6,
            axis_config={"color": WHITE, "tip_shape": StealthTip,
            "include_ticks":True, "tick_size":0.05,
            "stroke_width":0.6}
        )
        for axis in self.axes:
            axis.tip.set_opacity(0.6)
        # Define objects as attributes
        self.axis_labels = self.axes.get_axis_labels(x_label = "x", y_label = "y", z_label = "z")
  
        self.axis_labels[0].move_to(self.axes.c2p(12.4, 0, 0))
        self.axis_labels[1].move_to(self.axes.c2p(0, 8.4, 0)).rotate(-PI/2)
        self.axis_labels[2].move_to(self.axes.c2p(0, 0, 8.4))

        def func(x):
            return 5*((x+4)/4 - 2)**3 - 7*((x+4)/4 - 2)**2 + 5
        
        a, b, c = 2, 9, 11 

        self.graph1 = self.axes.plot(func, x_range=[2, 9], color=BLUE)
        self.graph1.set_stroke(width=3)
        def matheq(math, place,direction, color=color,font_size=30, buff = 0.2):
                    math = (
                        MathTex(math, font_size=font_size, color=color)
                        .next_to(place, direction, buff = 0.2))
                    return math 
        def Dline(A,B, C, D,stroke_width = 1,color = color):
            Dline = DashedLine(
                start=self.axes.c2p(A, B),
                end=self.axes.c2p(C, D),
                stroke_width=3,
                color=color)
            return Dline
        self.Dline1 = Dline(a, func(a), a, 0, color = GREEN)
        self.Dline2 = Dline(b, func(b), b, 0, color = RED)

        self.graph1_lab = matheq("y = f(x)", place=self.graph1, direction=UP, color=YELLOW)
        self.Dline1_lab = matheq("a",self.Dline1,DOWN,GREEN)
        self.Dline2_lab = matheq("b",self.Dline2,DOWN,RED)
        self.group1 = VGroup(self.Dline1, self.Dline2, self.Dline1_lab, self.Dline2_lab, self.graph1)

        def pointing_vector(x, y, xs, ys):
            
            vector = Vector([ x*self.axes.x_axis.unit_size, y*self.axes.y_axis.unit_size, 0],
            buff = 0.1, color=YELLOW)
            vector.shift([xs*self.axes.x_axis.unit_size, ys*self.axes.y_axis.unit_size, 0]) 
            vector.set_length(0.01)
            return vector
        self.vector1 = pointing_vector(0, -5, -0.5, 9)
        self.vector2 = pointing_vector(0,5,-0.5, -5)
        self.vector3 = pointing_vector(5,0,-7.9, 1.5)
        self.vector4 = pointing_vector(-5,0,6.8, 1.5)

        self.graph2 = self.graph1.copy().set_stroke(width=5)

        self.blue_number_line = NumberLine(
            x_range=[0, 12, 1],
            length=7.2,
            include_ticks=True,
            tick_size=0.05,
            include_tip=True,
            color=BLUE,
        )

        def Sline(A, B, C, D, color = color):
            Sline = Line(self.axes.c2p(A, func(B)),
            self.axes.c2p(C, D), color = color).set_stroke(width = 3)
            return Sline
        self.line1 = Sline(a,a, a, 0, color = BLUE)
        self.line2 = Sline(b,b, b, 0, color = BLUE)
        
        self.x_label = self.axis_labels[0]
        self.region = self.axes.get_area(self.graph1, x_range=[a, b], color=BLUE)
        self.region.set_opacity(1)
        self.e = ValueTracker(0)
        self.surface = always_redraw(
            lambda: Surface(
                lambda u, v: self.axes.c2p(
                    v, func(v) * np.cos(u), func(v) * np.sin(u)
                ),u_range = [0, self.e.get_value()/3],
                v_range = [a, b],
                checkerboard_colors=[BLUE],
                fill_opacity = 1,
                stroke_width = 0.001,
                resolution=(20, 20)
            )
        )
        self.sector_radius1 =func(a)*self.axes.y_length / (self.axes.y_range[1] - self.axes.y_range[0]) 
        self.face1 = always_redraw(
            lambda: Sector(
                inner_radius = 0,
                outer_radius=self.sector_radius1,
                start_angle=0,
                angle=self.e.get_value()/3,   
                color=BLUE,
                fill_opacity=0.8,
                stroke_width=0
            ).rotate_about_origin(PI/2,
                                    UP).rotate(PI/2, axis=self.axes.get_x_axis().get_unit_vector(),
                                                about_point = self.axes.c2p(a, 0, 0)).align_to(self.graph1, LEFT)
        )
        self.sector_radius2 =func(b)*self.axes.y_length / (self.axes.y_range[1] - self.axes.y_range[0])  
        self.face2 = always_redraw(
            lambda: Sector(
                inner_radius = 0,
                outer_radius=self.sector_radius2,
                start_angle=0,
                angle=self.e.get_value()/3,   
                color=BLUE,
                fill_opacity=1,
                stroke_width=0
            ).rotate_about_origin(PI/2,
                                    UP).rotate(PI/2, axis=self.axes.get_x_axis().get_unit_vector(),
                                                about_point = self.axes.c2p(b, 0, 0)).align_to(self.graph1, RIGHT)
        )

        def animate_to_2pi(value_tracker):
          animation = value_tracker.animate.set_value(6*PI)      
          return animation
        self.e1 = animate_to_2pi(self.e)
        self.e2 = ValueTracker(0)

        self.ellipse4 = Ellipse(width=2/3, height=0.266667, 
                                color=WHITE, fill_opacity=0, stroke_opacity = 0,
                                stroke_width=0.1).move_to(self.axes.c2p(7.8, 4.2, 4.2**(np.sqrt(3)/2)))

        self.ellipse5 = Ellipse(width=1/3, height=0.1333334, 
                                color=WHITE, fill_opacity=0, stroke_opacity = 0,
                                stroke_width=0.1).move_to(self.axes.c2p(7.4, 3.6, 3.6**(np.sqrt(3)/2)))
        self.ellipse = always_redraw(
            lambda: ParametricFunction(
                lambda t:  [3.6 + 3 * np.cos(t) , 2.6 + 1.8*np.sin(t), 2.6*(np.sqrt(3)/2)],
                t_range = [0, self.e2.get_value()],
                stroke_color=WHITE,
                fill_opacity = 0,
                stroke_width= 1,
                stroke_opacity=1
            )) 
        

        self.text1 = Text("حساب حجم هذاالمجسم", 
            font="Aldhabi",
            font_size=50).set_color(YELLOW)
        self.text1.move_to(self.ellipse.get_center()).rotate(PI/6, axis = RIGHT)
        self.text2 = Text("غيرمنتظم الشكل الهندسي!!", 
            font="Aldhabi",
            font_size=50).set_color(YELLOW)
        self.text2.move_to(self.ellipse.get_center()).rotate(PI/6, axis = RIGHT)
        self.surface1 = always_redraw(
            lambda: Surface(
                lambda u, v: self.axes.c2p(
                    v, func(v) * np.cos(u), func(v) * np.sin(u)
                ),u_range = [0, self.e.get_value()/3],
                v_range = [a, b],
                checkerboard_colors=[BLUE],
                fill_opacity = 0.3,
                stroke_width = 0.001,
                resolution=(20, 20)
            )
        )
        self.sector_radius1 =func(a)*self.axes.y_length / (self.axes.y_range[1] - self.axes.y_range[0]) 
        self.face11 = always_redraw(
            lambda: Sector(
                inner_radius = 0,
                outer_radius=self.sector_radius1,
                start_angle=0,
                angle=self.e.get_value()/3,   
                color=BLUE,
                fill_opacity=0.1,
                stroke_width=0
            ).rotate_about_origin(PI/2,
                                    UP).rotate(PI/2, axis=self.axes.get_x_axis().get_unit_vector(),
                                                about_point = self.axes.c2p(a, 0, 0)).align_to(self.graph1, LEFT)
        )
        self.sector_radius2 =func(b)*self.axes.y_length / (self.axes.y_range[1] - self.axes.y_range[0])  
        self.face12 = always_redraw(
            lambda: Sector(
                inner_radius = 0,
                outer_radius=self.sector_radius2,
                start_angle=0,
                angle=self.e.get_value()/3,   
                color=BLUE,
                fill_opacity=0.1,
                stroke_width=0
            ).rotate_about_origin(PI/2,
                                    UP).rotate(PI/2, axis=self.axes.get_x_axis().get_unit_vector(),
                                                about_point = self.axes.c2p(b, 0, 0)).align_to(self.graph1, RIGHT)
        )

        dx_list = [7,3.5,1.75, 0.7, 0.35, 0.140]
        kwargs = {
            "stroke_color": RED_D,
            "fill_color": RED_D,
            "checkerboard_colors": [RED_D, RED_D],
            "fill_opacity": 0.7,
            "stroke_width" : 0.01,
        }
        def get_cylinders(dx):
            self.cylinders = VGroup()
            for x in np.arange(a,b,dx):
                self.cylinderS = Cylinder(
                    radius=func(x)* self.axes.y_axis.unit_size,
                    height=dx* self.axes.x_axis.unit_size,
                    show_ends=True,
                    direction=RIGHT,
                    resolution=(20, 20),
                    **kwargs
                ).move_to(self.axes.c2p(x/2 + (x+dx)/2, 0)) 
                self.cylinders.add(self.cylinderS)
            return self.cylinders
        
        self.cylinders_list = VGroup(
            *[get_cylinders(dx) for dx in dx_list]
        )
       

        self.brace = BraceBetweenPoints(self.axes.c2p(a, 0), self.axes.c2p(b, 0),
                            direction=DOWN, color=ORANGE, 
                            sharpness=5, buff = 0.1).shift(1.8*DOWN)
        self.delta_x_text = matheq("\\Delta x = ", 
                        place=self.brace, direction=DOWN,
                        font_size=50, color=YELLOW)
        self.n_value_text = matheq("n = ", place=self.graph1, font_size=50, direction=UP,
                        buff = 1, color=YELLOW).shift(0.4*UP).align_to(self.delta_x_text, LEFT)
        self.n_value_text_right1 = matheq(str(1),place = self.n_value_text,
                                direction = RIGHT,font_size=50, color = YELLOW)
        self.delta_x_value = matheq("b - a",place = self.delta_x_text,
                            font_size=50, direction = RIGHT,color = YELLOW)
        self.n_value_text_right2 = matheq("2",place = self.n_value_text,
                                direction = RIGHT,font_size=50, color = YELLOW)
        self.delta_x_value2 = matheq("\\frac{b-a}{2}",place = self.delta_x_text,
                            direction = RIGHT,font_size=50, color = YELLOW)
        self.point1 = Dot(self.axes.c2p(a, func(a)), color= RED_A) 
        self.Dline1v = Dline(a, func(a), a, 0, color = RED_A)
        self.Dline1v_lab = matheq("a", place = self.Dline1v, direction = DOWN,color = GREEN)
        self.Dline1h = Dline(a, func(a), 0, func(a), color = RED_A)
        self.Dline1h_lab = matheq("f(a)", place = self.Dline1h, direction = UP, color = YELLOW)
        self.firts_cylinder= self.cylinders_list[0]
        self.point2 = Dot(self.axes.c2p((a+b)/2, func((a+b)/2)), color= RED_A) 
        self.Dline2v = Dline((a+b)/2, func((a+b)/2), (a+b)/2, 0, color = RED_A)
        self.Dline2v_lab = matheq("\\frac{a+b}{2}", place = self.Dline2v, direction = DOWN,
                        color = GREEN)
        self.Dline2h = Dline((a+b)/2, func((a+b)/2), 0, func((a+b)/2), color = RED_A)
        self.Dline2h_lab = matheq("f(\\frac{a+b}{2})", place = self.Dline2h, direction = UP,
        color = YELLOW).shift(0.5*LEFT)
        self.second_cylinder= self.cylinders_list[1]
        self.fcylinder = self.get_cylinders(dx_list[0])
    
        def create_rect(mobject, color = ORANGE, stroke_width=1, fill_opacity=0.1):
                        rect = SurroundingRectangle(mobject, fill_opacity=fill_opacity, color=color, stroke_width=stroke_width) 
                        return rect 


class FirstPofSolidsOfRevolution(CustomSceneSOR):
    def construct(self):

        self.play(Create(self.axes),
                Create(self.axis_labels),
                run_time=1, 
                )

        self.play(
                    Create(self.graph1),
                    Write(self.graph1_lab), 
                    run_time = 1)
        self.wait()
        self.play(Succession(Create(self.Dline1) ,Write(self.Dline1_lab),
            run_time = 1))
        self.play(Succession(Create(self.Dline2) ,Write(self.Dline2_lab),
            run_time = 1))
        self.wait(2)
        self.play(self.vector1.animate.set_length(1.7)
                .set_color(YELLOW).set_rate_func(rate_functions.ease_out_bounce),
                Create(self.graph2), run_time = 0.9)
        self.play(FadeTransform(self.vector1, self.vector2), run_time=0.1)
        self.play(LaggedStart(
                        self.vector2.animate.set_length(1.7)
                        .set_color(YELLOW).set_rate_func(rate_functions.ease_out_bounce),
                        Create(self.blue_number_line),
                        ApplyMethod(self.x_label.set_color, BLUE),
                        ApplyMethod(self.x_label.scale, 2),
                        lag_ratio=0.0,
                        run_time = .9))
        self.play(LaggedStart(
                        ApplyMethod(self.x_label.scale, 0.5),
                        FadeOut(self.vector2), run_time=0.1))
        self.wait(2)
        self.play(AnimationGroup(self.vector3.animate.set_length(1.7)
        .set_color(YELLOW).set_rate_func(rate_functions.ease_out_bounce),
        Create(self.line1), run_time = 0.9))
        self.play(FadeTransform(self.vector3, self.vector4), run_time=0.1)
        self.play(AnimationGroup(self.vector4.animate.set_length(1.65)
        .set_color(YELLOW).set_rate_func(rate_functions.ease_out_bounce),
        Create(self.line2), run_time = 0.9))
        self.play(LaggedStart(
                        FadeIn(self.region),
                        FadeOut(VGroup(self.graph1,self.graph2 ,self.Dline1, self.Dline2,
                                    self.line1, self.line2, self.blue_number_line, self.graph1_lab, 
                                    self.Dline1_lab, self.Dline2_lab, self.vector4)),
                        lag_ratio=0.0,
                        run_time=0.1))

        self.move_camera(phi=60 * DEGREES,theta=-30*DEGREES, run_tim2 = 0.5)
        self.add(self.surface, self.face1, self.face2)
        self.begin_ambient_camera_rotation(rate=0.25) 
        self.play(
            self.e,
            Rotating(self.region,
                axis=RIGHT,
                radians = 2*PI,
                about_point=self.axes.c2p(0,0,0),
                run_time =0.5 ), 
                run_time=1.5, 
                rate_func = rate_functions.smooth
            )

        self.play(FadeOut(VGroup(self.region)))
        self.wait(1.5) 
        self.stop_ambient_camera_rotation()
        self.move_camera(theta=-90 * DEGREES)
        self.add(self.ellipse, self.ellipse4, self.ellipse5)
        self.play(self.e2.animate.set_value(2*PI))

        self.play(Succession(self.ellipse4.animate.set_opacity(1),
            self.ellipse5.animate.set_opacity(1)), run_time=1)
        self.play(Write(self.text1, reverse=True,
            rate_func=rush_from, remover=False))
        self.play(Unwrite(self.text1), run_time = 0.5)
        self.wait(0.5)
        self.play(Write(self.text2, reverse=True,remover = False, run_time=1))
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)))

class CalculusAreaRiemann(MovingCameraScene):
    def construct(self):

        title = Text("حساب المساحة تحت منحنى الدالة", 
            font="Aldhabi", 
            font_size=50).set_color(YELLOW).to_edge(UP)
        underline = Underline(title, color = YELLOW, buff=0.0)
        rectangle = ScreenRectangle(aspect_ratio=6/3, height=3.7)
        rectangle.set_color(RED)

        axes = Axes(
            x_range=[-1, 10, 1],
            y_range=[-1, 8, 1],
            x_length=6,
            y_length=3,
            axis_config={"color": WHITE, "tip_shape": StealthTip,
            "include_ticks":True, "tick_size":0.05,
            "stroke_width":0.6})
        for axis in axes:
            axis.tip.set_opacity(0.6)

        axis_labels = axes.get_axis_labels(x_label = "x", y_label = "y")
        axis_labels[0].move_to(axes.c2p(10.4, 0))
        axis_labels[0].scale(0.75)
        axis_labels[1].move_to(axes.c2p(0, 8.5))
        axis_labels[1].scale(0.75)

        def func(x):
            return 5 * ((x + 4) / 4 - 2) ** 3 - 7 * ((x + 4) / 4 - 2) ** 2 + 5
        a,b = 2, 9
        c = (a + b) / 2

        # Create the graph of the function
        graph1 = axes.plot(func, x_range=[2, 9], color=BLUE)
        graph1.set_stroke(width=3)

        def Dline(A,B, C, D,stroke_width = 1,color = color):
            Dline = DashedLine(
                start=axes.c2p(A, func(B)),
                end=axes.c2p(C, D),
                stroke_width=3,
                color=color)
            return Dline
        Dline1 = Dline(a, a, a, 0, color = GREEN)
        Dline2 = Dline(b, b, b, 0, color = RED)

        # create labels
        def labels(label, place,direction, 
        color=color,w=1, buff = 0.2):
            label = (
                MathTex(label)
                .set(width=w)
                .next_to(place, direction, buff = 0.2)
                .set_color(color))
            return label
        graph1_lab = labels("y = f(x)", w=1, 
        place=graph1, direction=UP, color=YELLOW)
        Dline1_lab = labels("a",Dline1,DOWN,GREEN, w = 0.2  )
        Dline2_lab = labels("b",Dline2,DOWN,RED, w = 0.2  )



        # Create the region enclosed by the graph, x-axis, and lines
        region = axes.get_area(graph1, x_range=[a, b], color=BLUE)
        region.set_opacity(0.2)


        n_value_text = (
            MathTex("n = ")
            .next_to(axes.c2p(5.5, func(5.5)), UP, buff=0.4)
            .set_color(YELLOW)
            .add_background_rectangle()
        )

        dx_list = [7,3.5, 1.75, 1, 0.5, 0.3, 0.1, 0.05, 0.025, 0.01, 0.001]

        rectangles = VGroup(
            *[
                axes.get_riemann_rectangles(
                    graph=graph1,
                    x_range=[2, 9],
                    stroke_width=0.1,
                    stroke_color=WHITE,
                    dx=dx,
                )
                for dx in dx_list
            ]
        )
        first_area = rectangles[0]

        n_value_text_right1 = (
            MathTex(str(1))
            .next_to(n_value_text, RIGHT, buff=0.4)
            .set_color(YELLOW)
            .add_background_rectangle()
        )
        # self.add(title)
        self.play(LaggedStart(
                        Write(title, reverse=True,
                            rate_func=rush_from, remover=False),
                        Write(underline, reverse=True,
                            rate_func=rush_from, remover=False),
                        Create(rectangle),
                        run_time=1.5,
                        lat_ratio=0.0))
        self.play(LaggedStart(
                                Write(VGroup(axes, axis_labels, Dline1, Dline2,
                                        Dline1_lab, Dline2_lab)), 
                                Create(graph1),
                                lag_ratio=0.0, 
                                run_time = 1.5))
# 3 seconds 
        self.play(Write(VGroup(
        n_value_text,
        n_value_text_right1, first_area)), run_time = 1.5)
        self.wait(8)
# 12.5 seconds
        for k in range(1, len(dx_list)-1):
            n_value = 7/dx_list[k]
            n_value_text_right = (
                MathTex(str(int(n_value)))
                .next_to(n_value_text, RIGHT, buff=0.4)
                .set_color(YELLOW)
                .add_background_rectangle()
            )
            new_area = rectangles[k]
            self.play(LaggedStart(
                            Transform(n_value_text_right1,n_value_text_right),
                            Transform(first_area, new_area),
                            lag_ratio=0.0,
                            run_time=0.5
                            ))
            self.wait(0.5)
        
# 21.5 seconds        
        self.play(LaggedStart(
                        FadeOut(VGroup(axes, axis_labels, graph1,first_area, new_area,
                                n_value_text, n_value_text_right1, Dline1,
                                Dline2, Dline1_lab,Dline2_lab)),
                        rectangle.animate.scale(1.4),
                        lag_ratio=0.0,
                        run_time=1
                        ))
# 22.5 seconds
        frectangles1 = rectangles[5]
        frectangles1.set_opacity(1)
        group2 = VGroup(axes,axis_labels, graph1, frectangles1, Dline1,
        Dline2, Dline1_lab,Dline2_lab).copy().shift(2*LEFT + DOWN/2.1)
        # dot= Dot(region.get_center())
        def matheq(math, place,direction, 
        color=color,w=1, buff = 0.2):
            label = (
                MathTex(math)
                .set(width=w)
                .next_to(place, direction, buff = 0.2)
                .set_color(color))
            return label 
    
        onerectangle= Rectangle(width=0.2, height=1.4*func(a)*axes.y_axis.unit_size,
            fill_opacity=1, stroke_width=0.1, fill_color=BLUE).move_to(
                axes.c2p(15.5, 10.5)).shift(2*LEFT + DOWN/2)
        brace1 = Brace(onerectangle, direction=DOWN, color=ORANGE,sharpness=5)
        brace2 = Brace(onerectangle, direction=LEFT, color=ORANGE,sharpness=5)
        brace3 = Brace(frectangles1[4], direction=DOWN, 
            color=ORANGE,sharpness=5, buff = 0.5)
        labelbrace1 = matheq("\\Delta x",w= 0.4, place=brace1,buff = 0.1,
            direction=DOWN, color=PINK)
        labelbrace2 = matheq("f(a + k \\Delta x)",w= 1.1, place=brace2,
            buff = 0.1, direction=LEFT, color=PINK)
        labelbrace3 = matheq("\\Delta x = \\frac{b-a}{n}",w= 1, 
            place=brace3, direction=DOWN,buff = 0.1, color=PINK).shift(0.1*UP)
        eq1 = matheq("A = f(a + k \\Delta x) \\Delta x",w= 2.4, 
            place=labelbrace1, direction=DOWN,buff = 1, color=GREEN).shift(0.7*LEFT)
        eq2 = matheq("S_n = \\sum_ {k=0}^{n} f(a + k \\Delta x) \\Delta x",w= 3.36, 
            place=eq1, direction=DOWN,buff = 0.5, color=GREEN).shift(0.5*LEFT+ 0.2*DOWN)
        eq3 = matheq("    = \\sum_ {k=0}^{n} f(c_k) \\Delta x",w= 2, 
            place=eq2, direction=DOWN,buff = 0.5, color=GREEN) #.shift(0.5*LEFT+ 0.2*DOWN)
        eq4 = matheq("J = \\lim_{n \\to \\infty} \\sum_ {k=0}^{n} f(c_k) \\Delta x",w= 3.36, 
            place=labelbrace2, direction=LEFT,buff = 0.5, color=WHITE).shift(3*LEFT)
        eq5 = matheq("Area = \\int_{a}^{b} f(x) dx",w= 3.36, 
            place=labelbrace2, direction=LEFT,buff = 0.5, color=YELLOW).shift(0.9*LEFT+1.1*DOWN)
        
        eq51 = eq5[0][0:4]
        eq52 = eq5[0][4]
        eq53 = eq5[0][5]
        eq54 = eq5[0][6]
        eq55 = eq5[0][7]
        eq56 = eq5[0][8:]
        
        frectangles = rectangles[10]
        frectangles.set_opacity(0.3).shift(2*LEFT + DOWN/2.1)


        self.add(group2,onerectangle ,brace1,brace2, labelbrace1, labelbrace2,
         brace3, labelbrace3, eq1, eq2, eq3, eq4, frectangles)
        self.play(Transform(group2[3], frectangles), run_time = 0.5)
        self.play(LaggedStart(ApplyWave(frectangles),
                FadeIn(eq51, target_position= frectangles.get_center()),
                run_time=1))
        self.play(FadeIn(eq52, run_time=0.1))
        self.play(LaggedStart(
                        Transform(eq4[0][2:13].copy(), eq53),
                        Transform(group2[6].copy(),eq55),
                        Transform(group2[7].copy(),eq54),
                        Transform(eq4[0][13:].copy(), eq56),
                        run_time=1,
                        lag_ratio=0.1
                        ))
        self.play(Circumscribe(eq5, fade_out=False, color = RED))
        rect = SurroundingRectangle(eq5, color=RED, stroke_width=2)
        self.play(Create(rect))
        self.wait(0.5)
        self.play(FadeOut(Group(*self.mobjects), run_time = 0.5))

class ThirdPofSolidsOfRevolution(CustomSceneSOR):
    def construct(self):

        self.set_camera_orientation(phi=60 * DEGREES, theta=-22.5 * DEGREES)
        self.e.set_value(6*PI)
        self.add(self.axes, self.axis_labels, self.surface, self.face1, self.face2)
        self.begin_ambient_camera_rotation(rate=-PI/12)
        self.wait(2)
        self.add(self.region)
        self.play(
            self.e.animate.set_value(0),
            Rotating(self.region,
                axis=RIGHT,
                radians = -2*PI,
                about_point=self.axes.c2p(0,0,0)
                ), 
                run_time=1.5, 
                rate_func = rate_functions.smooth
            )
        self.stop_ambient_camera_rotation() 
        self.move_camera(theta = -90*DEGREES,phi = 0*DEGREES, run_time = 1)
        self.play(FadeOut(self.region), FadeIn(VGroup(self.graph1, self.group1)))
        self.region.set_opacity(0.3)
        self.remove(self.surface, self.face1, self.face2)
        self.wait()
        self.add(self.surface1, self.face11, self.face12)
        self.play(LaggedStart(
                        Create(self.firts_cylinder),
                        Write(VGroup(self.n_value_text, self.n_value_text_right1)),
                        run_time=1,
                        lag_ratio=0.0))
        self.play(LaggedStart(
                        self.firts_cylinder.animate.set_opacity(0.1),
                        Create(VGroup(self.point1, self.Dline1v,self.Dline1v_lab,
                                    self.Dline1h, self.Dline1h_lab)),
                        run_time=3,
                        lag_ratio=0.0))
        self.wait(2)
        self.play(Indicate(self.Dline1h_lab, scale=4, run_time=2))  
        self.wait(4)       
        self.play(LaggedStart(
                        Write(self.delta_x_text),
                        GrowFromCenter(self.brace),
                        lag_ratio=0.0))         
        self.play(Write(self.delta_x_value))
        self.play(LaggedStart(
                        self.firts_cylinder.animate.set_opacity(0.7),
                        FadeOut(VGroup(self.point1, self.Dline1v,self.Dline1v_lab,
                                    self.Dline1h, self.Dline1h_lab, self.graph1,self.group1,
                                    self.n_value_text, self.n_value_text_right1,
                                    self.delta_x_text, self.delta_x_value, self.brace)),
                        FadeIn(self.region),
                        run_time=1,
                        lag_ratio=0.0))

        self.move_camera(phi = 60*DEGREES)
        self.wait()       
        self.begin_ambient_camera_rotation(rate=PI/12)
        self.play(
            self.e.animate.set_value(6*PI),
            Rotating(self.region,
                axis=RIGHT,
                radians = 2*PI,
                about_point=self.axes.c2p(0,0,0),
                ),
                run_time=1.5, 
                rate_func = rate_functions.smooth
            )   
        self.play(FadeOut(self.region, run_time= 0.1))
        self.wait(2.9)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi = 0*DEGREES, theta=-90*DEGREES)
        self.play(LaggedStart(
                        FadeOut(VGroup(self.surface1, self.face11, self.face12)),
                        FadeIn(VGroup(self.n_value_text,self.graph1, self.group1, 
                                self.n_value_text_right1,self.delta_x_text, self.delta_x_value)),
                        run_time=1,
                        lag_ratio=0.0))
        self.play(self.e.animate.set_value(0))
        self.play(LaggedStart(
                        FadeTransform(self.n_value_text_right1,self.n_value_text_right2),
                        FadeTransform(self.delta_x_value,self.delta_x_value2),
                        self.firts_cylinder.animate.set_opacity(0.1),
                        Create(self.Dline2v),

                        run_time=1,
                        lag_ratio=0.0))
        self.wait(2)
        self.play(FadeTransform(self.firts_cylinder,self.second_cylinder))
        self.wait(2)
        self.play(LaggedStart(
                        Create(VGroup(self.point1, self.Dline1v,self.Dline1v_lab,
                                self.Dline1h, self.Dline1h_lab)),
                        self.second_cylinder[0].animate.set_opacity(0.1),
                        run_time=2,
                        lag_ratio=0.0)
        )
        self.wait(5)
        self.play(LaggedStart(
                        Create(VGroup(self.point2, self.Dline2v,self.Dline2v_lab,
                                self.Dline2h, self.Dline2h_lab)),
                        self.second_cylinder[0].animate.set_opacity(0.7),
                        self.second_cylinder[1].animate.set_opacity(0.1),
                        run_time=2,
                        lag_ratio=0.0)
        )
        self.play(self.second_cylinder[1].animate.set_opacity(0.7))
        self.wait(4)
        self.add(VGroup(self.surface1, self.face11,self.region, self.face12))
        self.play(
                FadeOut(VGroup(self.n_value_text,self.graph1, self.group1, 
                        self.n_value_text_right2,self.delta_x_text, self.delta_x_value2,
                        self.point1, self.Dline1v,self.Dline1v_lab,self.Dline1h, self.Dline1h_lab,
                        self.point2, self.Dline2v,self.Dline2v_lab,self.Dline2h, self.Dline2h_lab)))
                        
        self.wait(2)       
        self.move_camera(phi = 60*DEGREES)
        self.begin_ambient_camera_rotation(rate=PI/12)
        self.play(
            self.e.animate.set_value(6*PI),
            Rotating(self.region,
                axis=RIGHT,
                radians = 2*PI,
                about_point=self.axes.c2p(0,0,0),
                run_time =0.5 ), 
                run_time=1.5, 
                rate_func = rate_functions.smooth
            ) 
        self.play(FadeOut(VGroup(self.graph1,self.region), run_time= 0.1))
        self.wait(4.9)
        self.stop_ambient_camera_rotation()
        self.move_camera(phi = 0*DEGREES,theta=-90*DEGREES,focal_distance = 50, run_time = 1)
        self.add(VGroup(self.delta_x_text, self.delta_x_value2,
                    self.n_value_text, self.n_value_text_right2))
        self.wait(4)


class fourthPofSolidsOfRevolution1(CustomSceneSOR): 
    def construct(self):

#first part
   
        brace1 = Brace(self.fcylinder, direction=DOWN, 
            color=ORANGE,sharpness=5, buff = 0.5)
        labelbrace1 = self.matheq("n",font_size=50, place=brace1,buff = 0.1,
            direction=DOWN, color=RED_A)
        brace2 = Brace(self.fcylinder[0], direction=DOWN, 
            color=ORANGE,sharpness=5, buff = 0.5)
        labelbrace2 = self.matheq("\\Delta x",font_size=30, place=brace2,buff = 0.1,
            direction=DOWN, color=RED_A)       
        self.set_camera_orientation(focal_distance=50)

        self.play(FadeIn(VGroup(self.fcylinder, self.axes, self.axis_labels)))
        self.wait()
        self.play(LaggedStart(
                            GrowFromCenter(brace1), 
                            Write(labelbrace1),
                            lag_ratio=0.0))
        self.wait()
        self.play(Transform(VGroup(brace1, labelbrace1), VGroup(brace2, labelbrace2)))
        self.play(Succession(*[VGroup(brace1, labelbrace1).animate.next_to(self.fcylinder[j], 
                                                            DOWN) for j in range(1, 15)],
                            run_time=10))
        self.wait()


        dot_list = VGroup(
            *[Dot(self.axes.c2p((self.a+j*self.dx_list[0]), self.func(self.a+j*self.dx_list[0])), color= RED_A) for j in range(15)]
        )
        centera = self.axes.c2p(self.a , 0, 0)
        up_centera = self.axes.c2p(self.a, self.func(self.a), 0)  
        brace3 = BraceBetweenPoints(centera, up_centera, direction=LEFT, 
            color=ORANGE, sharpness=5, buff = 0.1)
        labelbrace3 = self.matheq("f(x_1)", place=brace3,buff = 0.1,
        direction=LEFT, color=RED_A)
        def SlineI(A, B, C, D, color = BLUE):
            Sline = Line(self.axes.c2p(A, B),
             self.axes.c2p(C, D), color = color) 
            return Sline
        linei = [SlineI(self.a+i*self.dx_list[0],0, self.a+(i+1)*self.dx_list[0], 0) for i in [0, 1, 2, 3, 4, 5, 14]]
        Dlinei = [self.Dline(self.a+i*self.dx_list[0], self.func(self.a+i*self.dx_list[0]), self.a+i*self.dx_list[0], 0, 
                color = BLUE) for i in [0, 1, 2, 3, 4,5, 14]]

        arrow1 = Arrow(start=labelbrace3[0][2:4].get_right(), end=linei[0].get_left(),color=YELLOW, buff=0.1)

        self.play(LaggedStart(
                    FadeTransform(brace1, brace3),
                    FadeTransform(labelbrace1, labelbrace3),
                    run_time=1,
                    lag_ratio=0.0))
        self.wait(2)
        self.play(LaggedStart(
                    Indicate(labelbrace3[0][2:4], scale=8),
                    FadeIn(VGroup(linei[0], self.group1, dot_list[0])),
                    GrowArrow(arrow1, point_color=YELLOW, use_override=False, rate_func=smooth),
                    self.fcylinder[0].animate.set_opacity(0.3),
                    self.fcylinder[1:].animate.set_opacity(0),
                    run_time=2,
                    lag_ratio=0.0))
        self.wait(4)
        centera = self.axes.c2p(self.a+self.dx_list[0] , 0, 0)
        up_centera = self.axes.c2p(self.a+self.dx_list[0], self.func(self.a+self.dx_list[0]), 0)  
        brace4 = BraceBetweenPoints(centera, up_centera, direction=LEFT, 
            color=ORANGE, sharpness=5, buff = 0.1)
        labelbrace4 = self.matheq("f(x_2)", place=brace4,buff = 0.1,
        direction=LEFT, color=RED_A)
        arrow2 = Arrow(start=labelbrace4[0][2:4].get_right(), end=linei[1].get_left(),color=YELLOW, buff=0.1)

        self.play(LaggedStart(
                    self.fcylinder[0].animate.set_opacity(0),
                    self.fcylinder[1].animate.set_opacity(0.3),
                    FadeOut(arrow1),
                    run_time=1,
                    lag_ratio=0.0))
        self.play(LaggedStart(
                    FadeTransform(brace3, brace4),
                    FadeTransform(dot_list[0], dot_list[1]),
                    FadeTransform(labelbrace3, labelbrace4),
                    FadeTransform(linei[0], linei[1]),
                    FadeTransform(Dlinei[0], Dlinei[1]),
                    run_time=1,
                    lag_ratio=0.0))
        self.wait()
        self.play(LaggedStart(
                    Indicate(labelbrace4[0][2:4], scale=8),
                    GrowArrow(arrow2, point_color=YELLOW, use_override=False, rate_func=smooth),
                    run_time=2,
                    lag_ratio=0.0))
        self.wait(3)
        self.play(LaggedStart(
                    FadeOut(arrow2),
                    self.fcylinder.animate.set_opacity(0.7),
                    run_time=1,
                    lag_ratio=0.0))
        # self.wait()
# it should be 34 seconds
        for j in [2,3,4, 14]:
            center = self.axes.c2p(self.a + j*self.dx_list[0], 0, 0)
            up_center = self.axes.c2p(self.a + j*self.dx_list[0], self.func(self.a + j*self.dx_list[0]), 0)
            brace5 = BraceBetweenPoints(center, up_center, direction=LEFT, 
                color=ORANGE, sharpness=5, buff = 0.1)
            if j !=14:
                labelbrace5 = self.matheq(f"f(x_{j+1:<2d})", place=brace5,buff = 0.1,
                    direction=LEFT, color=YELLOW)
                self.play(LaggedStart(
                                Transform(brace4, brace5),
                                Transform(dot_list[1], dot_list[j]),
                                Transform(linei[1], linei[j]),
                                Transform(Dlinei[1], Dlinei[j]),
                                Transform(labelbrace4, labelbrace5),
                                run_time=1,
                                lag_ratio=0.0))
                self.wait(0.5)
            else:
                labelbrace5 = self.matheq("f(x_n)", place=brace5,buff = 0.1,
                    direction=LEFT, color=YELLOW)
                self.play(LaggedStart(
                                Transform(brace4, brace5),
                                Transform(dot_list[1], dot_list[j]),
                                Transform(linei[1], linei[6]),
                                Transform(Dlinei[1], Dlinei[6]),
                                Transform(labelbrace4, labelbrace5),
                                run_time = 1,
                                lag_ratio=0.0))
                self.wait()
        self.remove(brace4, labelbrace4, dot_list[1], self.group1, linei[1], Dlinei[1])
        self.wait() 


class fourthPofSolidsOfRevolution2(CustomSceneSOR):
    def construct(self):
        self.set_camera_orientation(focal_distance=50)
        self.add(self.axes, self.axis_labels, self.fcylinder)
        self.wait(7)
        # self.play(ApplyWave(fcylinder))
        self.play(Group(*self.mobjects).animate.scale(0.5).to_edge(DL))
        cylinderoff= self.fcylinder[9].copy().to_edge(UP)
        self.play(FadeTransform(self.fcylinder[9], cylinderoff))
        self.play(Rotate(cylinderoff, angle=PI, axis = [0, 1, 0]))
        self.play(cylinderoff.animate.stretch(10 / (7/15), dim=0))

        brace_cylinderoff_D = Brace(cylinderoff, direction=DOWN, 
            color=ORANGE,sharpness=5, buff = 0.2)
        label_brace_cylinderoff_D = self.matheq("h", place=brace_cylinderoff_D, buff = 0,
                                        direction=DOWN, color=RED_A)
        center = self.axes.c2p(2 + 9*(7/15), 0, 0)
        up_center = self.axes.c2p(2 + 9*(7/15), self.func(2+9*(7/15)), 0)
        brace_cylinderoff_L = BraceBetweenPoints(center, up_center, direction=LEFT, 
                                    color=ORANGE,
                                    sharpness=5, 
                                    buff = 0.1).next_to(cylinderoff, LEFT).align_to(cylinderoff, UP)
        label_brace_cylinderoff_L = self.matheq("r", place=brace_cylinderoff_L,buff = 0.1,
                                        direction=LEFT ,color=RED_A)
        Volume= self.matheq("V = \\pi r^2 h", place= ORIGIN, direction=LEFT,color=WHITE,
                        font_size=40)
        self.wait()
        self.play(LaggedStart(
                    Write(label_brace_cylinderoff_L),
                    GrowFromCenter(brace_cylinderoff_L),
                    lag_ratio=0.0,
                    run_time=1
        ))
        self.play(LaggedStart(
                    Write(label_brace_cylinderoff_D),
                    GrowFromCenter(brace_cylinderoff_D),
                    lag_ratio=0.0,
                    run_time=1
        ))
        self.wait(2)
        self.play(Succession(
                        Write(Volume[0][0:3]),
                        LaggedStart(
                                FadeOut(label_brace_cylinderoff_L, target_position=Volume[0][3:5]),
                                FadeIn(Volume[0][3:5], target_position=label_brace_cylinderoff_L),
                                lag_ratio=0.0,
                                run_time=1),
                        LaggedStart(
                                FadeIn(Volume[0][5], target_position=label_brace_cylinderoff_D),
                                FadeOut(label_brace_cylinderoff_D, target_position=Volume[0][5]),
                                lag_ratio=0.0,
                                run_time=1),
                        FadeOut(VGroup(brace_cylinderoff_L, brace_cylinderoff_D), run_time=0.1),
                        ))
        rectv = self.create_rect(Volume, color = RED, fill_opacity=0)
        self.play(Succession(
                            Circumscribe(Volume, fade_out=False, color = RED),
                            Create(rectv)))
        self.play(cylinderoff.animate.stretch((7/15)/10, dim=0))
        self.play(LaggedStart(
                        FadeTransform(cylinderoff, self.fcylinder[9]),
                        VGroup(Volume, rectv).animate.to_edge(UL),
                        run_time=1,
                        lag_ratio = 0.0
                        ))
        self.wait(1.9)

##fourth part:
        fcylinders = []
        fcylinder0 = self.fcylinder[0].copy().to_edge(UR)
        fcylinders.append(fcylinder0)


        for i in range(1, 15):    
            fcylinderi = self.fcylinder[i].copy().next_to(fcylinders[i-1], DOWN, buff = 1)
            fcylinders.append(fcylinderi)

        bracesf = [Brace(fcylinders[i], direction=DOWN, color=ORANGE, sharpness=5, 
                    buff = 0.1) for i in range(0, 3)]
        labelbracef = [self.matheq("\\Delta x", place=bracesf[i], buff = 0,
                direction=DOWN, color=RED_A) for i in range(0, 3)]


        bracesfl = []
        for j in range(0, 6):
            center = self.axes.c2p(self.a + j*self.dx_list[0], 0, 0)
            up_center = self.axes.c2p(self.a + j*self.dx_list[0], self.func(self.a + j*self.dx_list[0]), 0)
            bracesflj = BraceBetweenPoints(center, up_center, direction=LEFT, 
                color=ORANGE,
                sharpness=5, 
                buff = 0.1).next_to(fcylinders[j], LEFT).align_to(fcylinders[j], UP)
            bracesfl.append(bracesflj)
        
        labelbracesfl = []
        for j in range(0, 6):
            labelbracef12 = self.matheq(f"f(x_{j+1:<2d})", place=bracesfl[j],buff = 0.1,
                direction=LEFT, color=RED_A)
            labelbracesfl.append(labelbracef12)
        eqs = [self.matheq(f"V_{i+1} = \\pi (f(x_{i+1}))^2 \\Delta x", 
                place=fcylinders[i], direction=LEFT,  
                color=RED_A).shift(1.5*LEFT) for i, _ in enumerate(fcylinders)] 
        for i in range(0, 3):
            if i == 0:
                self.play(Transform(self.fcylinder[i], fcylinders[i]), run_time = 1.5)
                self.play(Rotate(self.fcylinder[i], angle=PI, axis = [0, 1, 0]))
                self.play(LaggedStart(
                                Write(VGroup(bracesf[i], labelbracef[i])),
                                Write(VGroup(bracesfl[i], labelbracesfl[i])),
                                lag_ratio=0.0,
                                run_time=0.5))
                self.play(Write(eqs[i][0][0:5], run_time = 0.5))
                self.wait(3.5)
                self.play(Succession(
                        Transform(labelbracesfl[i], eqs[i][0][5:12]),
                        Transform(labelbracef[i], eqs[i][0][12:], run_time = 0.9),
                        FadeOut(VGroup(bracesf[i],bracesfl[i]), run_time=0.1)
                        ))
                self.wait(2)
            else:
                self.play(Transform(self.fcylinder[i], fcylinders[i]), run_time = 1.5)
                self.play(Rotate(self.fcylinder[i], angle=PI, axis = [0, 1, 0]))
                self.play(LaggedStart(
                                Write(VGroup(bracesf[i], labelbracef[i])),
                                Write(VGroup(bracesfl[i], labelbracesfl[i])),
                                lag_ratio=0.0,
                                run_time=0.5))
                self.play(Write(eqs[i][0][0:5], run_time = 0.5))
                self.play(Succession(
                        Transform(labelbracesfl[i], eqs[i][0][5:12]),
                        Transform(labelbracef[i], eqs[i][0][12:], run_time = 0.9),
                        FadeOut(VGroup(bracesf[i],bracesfl[i]), run_time=0.1)
                        ))
                self.wait(2)

        
        self.wait(2)
        self.play(LaggedStart(  
                                *[Transform(self.fcylinder[i], self.fcylinders[i]) for i in range(3, 15)],
                                *[FadeIn(eqs[i],target_position= self.fcylinders[i]) for i in [3,4]],
                                FadeOut(VGroup(self.axes, self.axis_labels)),
                                run_time=1, 
                                lag_ratio=0.0))
        
        
        self.wait(3)

        sol0 = MathTex("V_{solid}", color=YELLOW, font_size=40).to_edge(UL)
        sol1 = self.matheq("\\approx",
            place = sol0, direction = RIGHT,
            color = YELLOW, buff = 0.1, font_size=40)
        sol2 = self.matheq(" \\pi (f(x_1))^2 \\Delta x + \\pi (f(x_2))^2 \\Delta x + \\pi (f(x_3))^2 \\Delta x + \\dots + \\pi (f(x_n))^2 \\Delta x ",
            place = sol1, direction = RIGHT, color = YELLOW, buff=0.1, font_size=40)
        self.play(LaggedStart(
                        *[FadeIn(sol2[0][i*12:(i+1)*12], target_position = VGroup(eqs[i][0], labelbracesfl[i], labelbracef[i])) for i in range(3)],
                        *[FadeOut(VGroup(eqs[i][0], labelbracesfl[i], labelbracef[i]),target_position=sol2[0][i*12:(i+1)*12] ) for i in range(3)],
                        FadeIn(sol2[0][36:40], 
                                target_position = eqs[3][0]),
                        FadeIn(sol2[0][40:], 
                                target_position = eqs[4][0]),
                        FadeOut(VGroup(eqs[3],eqs[4])),
                        FadeOut(self.fcylinder),
                        FadeOut(VGroup(Volume, rectv)), 
                        run_time=2,
                        lag_ratio = 0.0))
       
        self.play(Succession(
                        Write(sol1),
                        FadeIn(self.copy1), 
                        FadeIn(sol0,target_position = self.copy1)))


        self.wait()


class fourthPofSolidsOfRevolution3(CustomSceneSOR):
    def construct(self):

        copy1=VGroup(self.axis_labels,self.axes, self.surface,self.face1, self.face2).copy().scale(0.5).to_edge(DR)

        self.set_camera_orientation(focal_distance=50)


        sol0 = self.MathTex("V_{solid}", color=YELLOW, font_size=40).to_edge(UL)
        sol1 = self.matheq("\\approx",
            place = sol0, direction = RIGHT,
            color = YELLOW, buff = 0.1, font_size=40)
        sol2 = self.matheq(" \\pi (f(x_1))^2 \\Delta x + \\pi (f(x_2))^2 \\Delta x + \\pi (f(x_3))^2 \\Delta x + \\dots + \\pi (f(x_n))^2 \\Delta x ",
            place = sol1, direction = RIGHT, color = YELLOW, buff=0.1, font_size=40)

        self.add(copy1, sol0, sol1, sol2)

        surrecpi= [self.create_rect(part, color = RED) for part in [sol2[0][i] for i in [0, 12, 24, 40]]]
        surecdeltax = [self.create_rect(part, color = GREEN) for part in [sol2[0][i:i+2] for i in [9, 21, 33, 49]]]
        self.play(
            LaggedStart(
                *[Create(surrecpi[i]) for i in range(0, len(surrecpi))],
                *[Create(surecdeltax[i]) for i in range(0, len(surecdeltax))],
                lag_ratio=0.2),
            run_time=3)
        self.play(LaggedStart(
                        *[FadeOut(part, target_position = sol2[0][0]) for part in [sol2[0][i] for i in [12, 24, 40]]],
                        *[FadeOut(part, target_position = sol2[0][49:51]) for part in [sol2[0][i:i+2] for i in [9, 21, 33]]],
                        *[FadeOut(surrecpi[i], target_position = sol2[0][49:51]) for i in range(0, len(surrecpi))],
                        *[FadeOut(surecdeltax[i], target_position = sol2[0][49:51]) for i in range(0, len(surecdeltax))],
                lag_ratio = 0.0), run_time = 3) 

        sol3 = self.matheq(" \\pi \left( (f(x_1))^2 + (f(x_2))^2 +  (f(x_3))^2  + \\dots + (f(x_n))^2 \\right) \\Delta x",
            place = sol1, direction = RIGHT, color = YELLOW, buff=0.1, font_size=40)
        sol4 = sol0.copy().next_to(sol0, DOWN, buff=1.5)
        sol5 = sol1.copy().next_to(sol4, RIGHT, buff=0.1)
        sol6 = sol3[0][0].copy().next_to(sol5, RIGHT, buff=0.2).set_font_size(45)
        sol7 = self.matheq("\\sum_ {i = 1}^{n} (f(x_i))^2 \\Delta x", place = sol6, 
        direction = RIGHT, color = YELLOW, font_size=45)

        surrecsum= [self.create_rect(part, stroke_width=3).scale(0.8) for part in [sol3[0][i] for i in [6, -7]]]
        surallsum = self.create_rect(sol3[0][2:-3], stroke_width=3)
        suradelx = self.create_rect(sol3[0][42:], stroke_width=3)
        suradeln = self.create_rect(sol7[0][0], stroke_width=3)
        suri = self.create_rect(sol7[0][9], stroke_width=3)
        surisum = self.create_rect(sol7[0][2], stroke_width=3)
        suradeab = self.create_rect(sol5, stroke_width=3)
        surrectsol7 = self.create_rect(sol7[0][5:], stroke_width=3)
        self.play(FadeTransform(
                            VGroup(sol2[0][0:9], sol2[0][11],sol2[0][13:21], 
                                    sol2[0][23],sol2[0][25:33], sol2[0][35:40],sol2[0][41:]), 
                            sol3))

        self.wait(4)
        self.play(Write(VGroup(sol4, sol5, sol6)))
        self.wait()

        self.play(Write(sol7[0][1]))
        self.play(LaggedStart(
                        Create(surallsum),
                        FadeIn(sol7[0][5:13], target_position = sol3[0][2:-3]),
                        lag_ratio=0.0
                        ))
        self.play(LaggedStart(
                        FadeTransform(surallsum, suradelx),
                        FadeIn(sol7[0][13:], target_position = sol3[0][42:]),
                        lag_ratio=0.0,
                        run_time=1.5
                        ))   # 18 seconds
        
        self.play(LaggedStart(
                                Create(suri), 
                                FadeOut(suradelx),
                                lag_ratio=0.0,
                                run_time = 0.5))
        self.play(LaggedStart(
                        FadeTransform(suri, surisum),
                        FadeIn(sol7[0][2], target_position = sol7[0][9]),
                        Write(sol7[0][3]),
                        Create(surrecsum[0]),
                        lag_ratio=0.0,
                        run_time=0.5
                        ))

        self.play(LaggedStart(
                        FadeOut(surisum),
                        FadeIn(sol7[0][4], target_position = sol3[0][6]),
                        FadeTransform(surrecsum[0], surrecsum[1]),
                        lag_ratio=0.0
                        ))
        self.play(LaggedStart(
                        FadeOut(surrecsum[1]),
                        FadeIn(sol7[0][0], target_position = sol3[0][-7]),
                        lag_ratio=0.0
                        ))  # 21 seconds
        
        self.wait(10.5)
        for i in range(13):
            self.play(Flash(sol7[0][0]))
        self.wait()
        for i in [3, 6, 7, 8, 9, "n"]:
            if i != "n":
                sol8 = self.matheq(f"10^{i}", place = sol7[0][0], 
                    direction = RIGHT, color = YELLOW, font_size=35).move_to(sol7[0][0])
                self.play(Transform(sol7[0][0],sol8))
            else:
                sol9 = self.matheq("n", place = sol7[0][0], 
                    direction = RIGHT, color = YELLOW, font_size=35).move_to(sol7[0][0]) 
                self.play(Transform(sol7[0][0],sol9), run_time=0.5)
                self.wait(0.5) 
        self.wait(9)  # 57 seconds



class fourthPofSolidsOfRevolution4(CustomSceneSOR):    
    def construct(self):

        copy1=VGroup(self.axis_labels,self.axes, self.surface,self.face1, self.face2).copy().scale(0.5).to_edge(DR)
        sol0 = MathTex("V_{solid}", color=YELLOW, font_size=40).to_edge(UL)
        sol1 = self.matheq("\\approx",
            place = sol0, direction = RIGHT,
            color = YELLOW, buff = 0.1, font_size=40)
        sol2 = self.matheq(" \\pi (f(x_1))^2 \\Delta x + \\pi (f(x_2))^2 \\Delta x + \\pi (f(x_3))^2 \\Delta x + \\dots + \\pi (f(x_n))^2 \\Delta x ",
            place = sol1, direction = RIGHT, color = YELLOW, buff=0.1, font_size=40)


        surrecpi= [self.create_rect(part, color = RED) for part in [sol2[0][i] for i in [0, 12, 24, 40]]]
        surecdeltax = [self.create_rect(part, color = GREEN) for part in [sol2[0][i:i+2] for i in [9, 21, 33, 49]]]

        sol3 = self.matheq(" \\pi \left( (f(x_1))^2 + (f(x_2))^2 +  (f(x_3))^2  + \\dots + (f(x_n))^2 \\right) \\Delta x",
            place = sol1, direction = RIGHT, color = YELLOW, buff=0.1, font_size=40)
        sol4 = sol0.copy().next_to(sol0, DOWN, buff=1.5)
        sol5 = sol1.copy().next_to(sol4, RIGHT, buff=0.1)
        sol6 = sol3[0][0].copy().next_to(sol5, RIGHT, buff=0.2).set_font_size(45)
        sol7 = self.matheq("\\sum_ {i = 1}^{n} (f(x_i))^2 \\Delta x", place = sol6, 
        direction = RIGHT, color = YELLOW, font_size=45)

        surrecsum= [self.create_rect(part, stroke_width=3).scale(0.8) for part in [sol3[0][i] for i in [6, -7]]]
        surallsum = self.create_rect(sol3[0][2:-3], stroke_width=3)
        suradelx = self.create_rect(sol3[0][42:], stroke_width=3)
        suradeln = self.create_rect(sol7[0][0], stroke_width=3)
        suri = self.create_rect(sol7[0][9], stroke_width=3)
        surisum = self.create_rect(sol7[0][2:4], stroke_width=3)
        suradeab = self.create_rect(sol5, stroke_width=3)
        surrectsol7 = self.create_rect(sol7[0][5:], stroke_width=3)
        
        self.set_camera_orientation(focal_distance=50)
        self.add(copy1, sol0, sol1, sol3, sol4, sol5, sol6, sol7)
        
        sol10 = sol0.copy().next_to(sol4, DOWN, buff=1.5)
        sol11 = self.matheq("=", place = sol10, 
        direction = RIGHT, color = YELLOW,font_size=45, buff=0.1)
        sol12 = sol3[0][0].copy().next_to(sol11, RIGHT, buff=0.1)
        sol13 = self.matheq("\\lim_{n \\to \\infty} \\sum_ {i = 1}^{n} \\pi (f(x_i))^2 \\Delta x",
                        place = sol11, direction = RIGHT, color = YELLOW,font_size=45, buff=0.1)

        surrectsol131 = self.create_rect(sol13[0][0:11], stroke_width=3)
        surrectsol132 = self.create_rect(sol13[0][11:], stroke_width=3)

        self.wait(5)
        self.play(Succession(
                            Write(VGroup(sol13[0][0:3], sol13[0][6:]), run_time=2),
                            Write(sol13[0][3:6], run_time=2)
                            ))
        self.wait(3)
        self.play(FadeIn(suradeab))
        self.wait()
        self.play(FadeIn(sol11, target_position=sol5))
        self.play(Succession(
                            FadeIn(sol10, target_position=sol4),
                            Circumscribe(VGroup(sol10, sol11, sol13)),
                            FadeOut(suradeab)
                            ))

        self.wait(3) # 21 seconds
        sol15 = self.matheq("V_{solid} = \\int_{a}^{b} \\pi (f(x))^2 dx", place = sol10, 
                    direction = DOWN, color = WHITE, 
                    font_size=45).shift(1.5*DOWN).align_to(sol10, LEFT)
        surrectf = self.create_rect(sol15,
                        fill_opacity=0,color=RED, stroke_width=3)
        fgroup = VGroup(sol15,surrectf)
        self.play(Create(surrectsol131))
        self.wait(5)
        
        self.play(FadeIn(sol15[0][7:10], target_position=sol13[0][0:11]))
        self.play(Write(sol15[0][0:7], run_time=2))
        self.wait(1.5) 
        self.play(Succession(
                        Transform(surrectsol131,surrectsol132),
                        FadeIn(sol15[0][10:], target_position=sol13[0][11:])
                        ))
        self.play(LaggedStart(
                            FadeOut(surrectsol131),
                            Circumscribe(sol15, 
                                    fade_out=False, color = RED),
                            lag_ratio=0.0
                            ))
        self.play(Create(surrectf, run_time=0.5))

          
        self.play(LaggedStart(
                    FadeOut(VGroup(sol0, sol1, sol3, sol4, sol5, 
                                sol6, sol7, sol10, sol11, sol13)),
                    fgroup.animate.next_to(copy1, UP),
                    lag_ratio=0.0
                    ))
        fgroup.add_updater(lambda m: fgroup.next_to(copy1, UP))
        self.play(copy1.animate.move_to(ORIGIN))
        self.wait(8) 
        self.play(FocusOn(sol15[0][11:18]))
        self.play(LaggedStart(
                            FocusOn(sol15[0][8]),
                            FocusOn(sol15[0][9]),
                            lag_ratio=0.0
                            ))
        self.wait(1.5)
        self.play(Wiggle(sol15[0][7:]))
        self.wait(2.5)
class lastPofSolidsOfRevolution(Scene):    
    def construct(self):

        text1 = Text("تمت كتابة وتحسين بعض أجزاء الكود لهذا الانيميشن ", 
                    font="Aldhabi",
                    font_size=50).set_color(YELLOW).to_edge(UR)
        text2 = Text("وذلك بمساعدة وضع الدردشة مايكروسوفت بينج", 
                    font="Aldhabi",
                    font_size=50).set_color(YELLOW).next_to(text1, DOWN).align_to(text1, RIGHT)
        text3 = Text("،الكود متاح على :", 
                    font="Aldhabi",
                    font_size=50).set_color(YELLOW).next_to(text2, LEFT)
        text4 = Text("GitHub", 
                    font="Aldhabi",
                    font_size=50).set_color(YELLOW).next_to(text3, 2*DOWN).align_to(text3, LEFT).shift(2*LEFT)
        self.play(Write(text1, reverse=True,remover=False, run_time=3))
        self.play(Write(text2, reverse=True,remover=False, run_time=2))
        self.play(Write(text3, reverse=True, remover=False))
        self.play(Write(text4, reverse=True, remover=False))


        self.wait()