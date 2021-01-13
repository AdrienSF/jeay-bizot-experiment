from psychopy import visual, core, event

class Speedometer(object):
    def __init__(self, clock, stream_inlet):
        # self.mouse = mouse
        self.clock = clock
        self.stream_inlet = stream_inlet
        
        self.sliding_window = []
        self.history = []

    def init_sliding_window(self, dt):
        start = self.clock.getTime()
        while self.clock.getTime() - start < dt:            
            # event.getKeys() # idk why but mouse pos doesn't update if I don't call this
            data = self.stream_inlet.pull_sample()
            self.sliding_window.append( data )
            self.history.append( data )
            # core.wait(.001)

    def get_speed(self, dt):
        self.init_sliding_window(dt)
        # event.getKeys()

        current_pos, current_time = self.stream_inlet.pull_sample()

        self.sliding_window.append( (current_pos, current_time) )
        self.history.append( (current_pos, current_time) )
        # sliding window interval
        self.sliding_window = [ pos for pos in self.sliding_window if pos[1] > (current_time - dt) ]
        start_pos, start_time = self.sliding_window[0]
        end_pos, end_time = self.sliding_window[-1]
        speed = (end_pos - start_pos)/(end_time - start_time)
        
        return abs(speed)


    def get_mean_speed(self):
        start_pos, start_time = self.history[0]
        end_pos, end_time = self.history[-1]
        speed = (end_pos - start_pos)/(end_time - start_time)

        return abs(speed)
