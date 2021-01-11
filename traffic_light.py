from psychopy import visual, core, event

class TrafficLight(object):
    def __init__(self, win, pos=(250, 0), text_size=50):
        self.pos = pos
        self.text_size = text_size

        self.off_light = visual.TextStim(win, "OFF", pos=(pos[0], pos[1]+text_size/2), color='red', units='pix', height=text_size )
        self.on_light = visual.TextStim(win, "ON", pos=(pos[0], pos[1]-text_size/2), color='green', units='pix', height=text_size )

        self.is_green = None

    def draw(self):
        if self.is_green == None:
            self.off_light.draw()
            self.on_light.draw()
        elif self.is_green:
            self.on_light.draw()
        else:
            self.off_light.draw()
