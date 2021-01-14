from psychopy import visual, core, event
import random

class HighStriker(object):
    def __init__(self, win, top_coords: tuple, bottom_coords: tuple, target_radius=20, slider_radius=10):
        self.window = win
        self.top_coords = top_coords
        self.bottom_coords = bottom_coords
        self.line = visual.ShapeStim( win=win, lineColor='black', vertices=(bottom_coords, top_coords), units='pix')
        self.target = visual.Circle(
            win=win,
            units="pix",
            radius=target_radius,
            # fillColor=[1, 0, 0],
            lineColor='red'
            )
        self.target.pos = top_coords

        self.slider = visual.Circle(
            win=win,
            units="pix",
            radius=slider_radius,
            fillColor=[1, 1, 1],
            lineColor=[1, 1, 1]
            )
        self.slider.pos = bottom_coords


        self.slider_travel_time = .7
        self.timestep = 1/60

    def draw(self, no_target=False):
        if no_target:
            self.line.draw()
            self.slider.draw()
        else:
            self.line.draw()
            self.target.draw()
            self.slider.draw()
            

    def randomize_target(self):
        lower_bound = int(self.bottom_coords[1] + (self.top_coords[1] - self.bottom_coords[1])/3)
        y_pos = random.randrange(lower_bound, self.top_coords[1])
        self.target.pos = (0, y_pos )
        return y_pos


    def slide_up(self, to_slide: int, auto_draw=[], no_target=False):
        initial_pos = self.slider.pos[1]
        clock = core.Clock()
        while clock.getTime() < self.slider_travel_time:
            core.wait(self.timestep)
            for e in auto_draw:
                e.draw()
            progress = (clock.getTime()/self.slider_travel_time)*to_slide
            self.slider.pos = (0, initial_pos + progress)
            self.draw(no_target=no_target)
            self.window.flip()

    def reset_slider(self):
        self.slider.pos = self.bottom_coords
            