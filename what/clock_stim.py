from psychopy import visual, core, event
import math
import numpy as np
import random

class ClockStim(object):
    def __init__(self, win, frame_radius=200, period=5):
        self.period = period
        self.window = win

        self.frame = visual.Circle(
            win=win,
            units="pix",
            radius=frame_radius,
            # fillColor=[1, 0, 0],
            lineColor='white',
            edges=128
            )

        self.dot = visual.Circle(
            win=win,
            units="pix",
            radius=10,
            fillColor=[1, 1, 1],
            # lineColor='red'
            )
        self.dot.pos = (0, frame_radius)

        self.target = visual.Circle(
            win=win,
            units="pix",
            radius=15, #was 11
            # fillColor=[1, 1, 1],
            lineColor='red',
            lineWidth=6
            )
        self.target.pos = (0, -frame_radius)

    
    def randomize_dot(self):
        # get random angle (between 0 and 2pi)
        rand_angle = random.uniform(0, 2*math.pi)
        self.dot.pos = ( self.frame.radius * math.cos(rand_angle), self.frame.radius * math.sin(rand_angle))

    def randomize_target(self):
        rand_angle = random.uniform(0, math.pi)

        rotation_matrix = np.array([
            [math.cos(rand_angle), math.sin(rand_angle)],
            [-math.sin(rand_angle), math.cos(rand_angle)]
        ])

        shifted_pos = np.dot(np.array(self.dot.pos), rotation_matrix)

        self.target.pos = tuple(shifted_pos)



    def rotate(self, timestep=.01):
        # spin the dot another 2pi*timestep/period
        to_rotate = 2*math.pi*timestep/self.period
        rotation_matrix = np.array([
            [math.cos(to_rotate), -math.sin(to_rotate)],
            [math.sin(to_rotate), math.cos(to_rotate)]
        ])

        new_pos = np.dot(np.array(self.dot.pos), rotation_matrix)

        self.dot.pos = tuple(new_pos)

        core.wait(timestep)


    def draw(self, draw_target=True):
        if draw_target:
            self.frame.draw()
            self.dot.draw()
            self.target.draw()
        else:
            self.frame.draw()
            self.dot.draw()

        