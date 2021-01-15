from traffic_light import TrafficLight
from psychopy import visual, core, event, parallel 

class Calibrator(object):
    def __init__(self, win, light: TrafficLight, sensor_input_stream=None):
        self.stream_inlet = sensor_input_stream
        self.window = win
        self.light = light

    def calibrate(self):
        msg = visual.TextStim(win = self.window, text = "After this message 'OFF' signal will appear, while OFF is displayed do not move - after a while, ON will be displayed, while ON is displayed, make movements that are as fast as possible. When you are ready, please press any key")
        msg.draw()
        self.window.flip()
        while not event.getKeys():
            core.wait(0.1)
        
        self.light.is_green = False
        self.light.draw()
        self.window.flip()
        data_OFF = []
        clock = core.Clock()
        while clock.getTime() < 30:
            sample, timestamp = self.stream_inlet.pull_sample()
            data_OFF.append(sample[64])
        
        self.light.is_green = True
        self.light.draw()
        self.window.flip()
        data_ON = []
        clock = core.Clock()
        while clock.getTime() < 30:
            sample, timestamp = self.stream_inlet.pull_sample()
            data_ON.append(sample[64])

        return max(data_OFF), max(data_ON) # acc_thr and upper limit for dist calc      
        