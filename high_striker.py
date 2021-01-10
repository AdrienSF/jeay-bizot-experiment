from psychopy import visual, core, event
import random

class HighStriker(object):
    def __init__(self, win, top_coords: tuple, bottom_coords: tuple, target_radius=10, slider_radius=20):
        self.window = win
        self.top_coords = top_coords
        self.bottom_coords = bottom_coords
        self.line = visual.Line( win=win, start=top_coords, end=bottom_coords )
        self.target = visual.Circle(
            win=win,
            units="pix",
            radius=target_radius,
            fillColor=[1, 0, 0],
            lineColor=[1, 0, 0]
            )
        self.target.pos = top_coords

        self.slider = visual.Circle(
            win=win,
            units="pix",
            radius=slider_radius,
            # fillColor=[1, 1, 1],
            lineColor=[1, 1, 1]
            )
        self.slider.pos = bottom_coords

    def draw(self):
        self.line.draw()
        self.target.draw()
        self.slider.draw()

    def randomize_target(self):
        self.target.pos = (0, random.randrange(self.bottom_coords[1], self.top_coords[1]) )