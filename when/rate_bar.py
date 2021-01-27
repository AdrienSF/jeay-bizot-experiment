from psychopy import visual, core, event
import random


class RateBar(object):
    def __init__(self, win, left_text="effortless", right_text="effortful"):
        self.window = win

        self.line = visual.ShapeStim( win=win, lineColor='black', vertices=((-.4, -.9), (.4,-.9)))
        self.marker = visual.ShapeStim( win=win, lineColor='black', vertices=((0, -1), (0,-.85)))

        self.left_text = visual.TextStim(win, text=left_text, pos=(-.7, -.9))
        self.right_text = visual.TextStim(win, text=right_text, pos=(.7, -.9))

        self.rating = .5
        self.scale_length = self.line.vertices[1][0] - self.line.vertices[0][0]


    def draw(self):
        # self.update_marker_pos()
        self.line.draw()
        self.marker.draw()
        self.left_text.draw()
        self.right_text.draw()


    def move_marker(self, direction=-1, dx=.02):
        self.rating += direction*dx
        self.update_marker_pos()


    def update_marker_pos(self):
        new_x = self.rating*self.scale_length + self.line.vertices[0][0]

        if new_x < self.line.vertices[0][0] or self.rating < 0:
            new_x = self.line.vertices[0][0]
            self.rating = 0
        elif new_x > self.line.vertices[1][0]or self.rating > 1:
            new_x = self.line.vertices[1][0]
            self.rating = 1

        self.marker.vertices = ((new_x, self.marker.vertices[0][1]), (new_x, self.marker.vertices[1][1]))


    def randomize_marker(self):
        self.rating = random.uniform(0,1)
        self.update_marker_pos()


    def get_user_rating(self):
        self.randomize_marker()

        keys_pressed = event.getKeys()
        while 'return' not in keys_pressed:
            if 'left' in keys_pressed:
                self.move_marker(-1)
            elif 'right' in keys_pressed:
                self.move_marker(1)
            
            keys_pressed = event.getKeys()

            self.draw()
            self.window.flip()

        return self.rating
