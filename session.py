from high_striker import HighStriker
from traffic_light import TrafficLight
from speedometer import Speedometer
from psychopy import visual, core, event
import math



class Session(object):
    def __init__(self, win, striker: HighStriker, light: TrafficLight, sensor_input_stream=None):
        self.window = win
        self.striker = striker
        self.light = light
        # self.input_stream = sensor_input_stream
        # self.mouse = sensor_input_stream # not supposed to be mouse but instead an input stream from sensor

        self.speed_thresh = 10 # a hundred what? [NOTE]: need to check this
    
    def run_trial(self):
        self.light.is_green = False
        self.light.draw()
        self.striker.draw(no_target=True)

        self.window.flip()

        core.wait(1)

        self.light.is_green = True
        self.striker.randomize_target()
        self.light.draw()
        self.striker.draw()
        self.window.flip()

        # start listening to self.input_stream
        # do recording stuff
        dist = self.get_dist()
        print('dist: ' + str(dist))
        # stop listening
        self.light.is_green = False
        self.light.draw()
        self.striker.draw()
        self.window.flip()

        self.striker.slide_up(dist, auto_draw=[self.light])

        core.wait(1)
        self.striker.reset_slider()
        self.window.flip()
        

    def get_dist(self, dt=.020):
        mouse = event.Mouse(win=self.window)
        clock = core.Clock()
        speedometer = Speedometer(mouse, clock)
        interval = []
        speed = 0
        while speed < self.speed_thresh:
            speed = speedometer.get_speed(dt)
            print(speed)
        # reset clock and speedometer
        clock = core.Clock()
        speedometer = Speedometer(mouse, clock)
        speed = math.inf
        while speed > self.speed_thresh:
            speed = speedometer.get_speed(dt)
        

        # print(speedometer.history)
        return speedometer.get_mean_speed() * 10


    def run(self):
        clock = core.Clock()
        while clock.getTime() < 60:
            self.run_trial()


