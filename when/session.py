from high_striker import HighStriker
from traffic_light import TrafficLight
# from speedometer import Speedometer [DEPRECATED]
from psychopy import visual, core, event, parallel
import math
import csv
import statistics as stat


class Session(object):
    def __init__(self, win, striker: HighStriker, light: TrafficLight, sensor_input_stream=None, session_id=None, acc_thresh = None, max_acc = None):
        self.window = win
        self.striker = striker
        self.light = light
        self.session_id = session_id
        self.stream_inlet = sensor_input_stream

        self.block_duration = 5 * 60
        self.current_block = 0
        self.current_trial = 0
        # self.total_blocks = 2
        # self.mouse = sensor_input_stream # not supposed to be mouse but instead an input stream from sensor

        self.acc_thresh = acc_thresh 
        self.max_acc = max_acc

        self.clock = None
        self.post_pulse_time = None
        self.history = {}

        self.instructions = {True: 'Launch the slider to wherever you want, and whenever, but try to space out the launches in time.',
                            False: 'Launch the slider as precisely as possible into the randomly appearing red target. You have a limited number of tries so make every shot count.'
                            }
        self.start_message = '\npress any key to start'
        # set which trial type for each block. 
        self.block_order = ['A', 'B', 'C']


        self.cross = visual.TextStim(self.window, text='+', units='pix', height=50)
        self.rate_scale = visual.RatingScale(
            win, 
            showValue=False, 
            labels=0, 
            precision=100, 
            low=0, 
            high=100, 
            tickHeight=0.0,
            size=2,
            scale='Effortless                        Effortful'
        )
    
    def run_trial(self, trial_type: str):
        is_type_A = trial_type == 'A'

        self.current_trial += 1
        self.history[self.current_block][self.current_trial] = {}


        self.light.is_green = False
        self.light.draw()
        self.striker.draw(no_target=True)
        self.cross.draw()

        self.window.flip()

        core.wait(1)

        self.light.is_green = True
        if trial_type == 'C':
            # always place target in center for C trials
            self.striker.target.pos = (0, 0)
            self.history[self.current_block][self.current_trial]['target_y_pos'] = self.striker.target.pos
        else:
            y_pos = self.striker.randomize_target()
            self.history[self.current_block][self.current_trial]['target_y_pos'] = y_pos

        self.light.draw()
        self.striker.draw(no_target=is_type_A)
        self.cross.draw()
        self.window.flip()
        # record time when light turned on
        self.history[self.current_block][self.current_trial]['ON_disp_time'] = self.clock.getTime()

        # start listening to self.input_stream
        # do recording stuff
        dist = self.get_dist()
        # print('dist: ' + str(dist))
        # stop listening
        self.light.is_green = False
        self.light.draw()
        self.striker.draw(no_target=is_type_A)
        self.cross.draw()
        self.window.flip()

        self.striker.slide_up(dist, auto_draw=[self.light, self.cross], no_target=is_type_A)

        if trial_type == 'C':
            while ratingScale.noResponse:
                self.light.draw()
                self.striker.draw(no_target=is_type_A)
                self.cross.draw()
                ratingScale.draw()
                win.flip()
            rating = ratingScale.getRating()
            self.history[self.current_block][self.current_trial]['rating'] = rating
        else:
            self.history[self.current_block][self.current_trial]['rating'] = None

        core.wait(1)
        self.striker.reset_slider()
        self.window.flip()




        

    def get_dist(self, dt=.020):
        # mouse = event.Mouse(win=self.window)
        # clock = core.Clock()
        # speedometer = Speedometer(mouse, clock)
        # interval = []
        acc = 0
        while acc < self.acc_thresh:
            acc, sensor_time = self.get_acc(return_time=True)
            # print(speed)
        # record start of movement
        self.history[self.current_block][self.current_trial]['movement_onset'] = self.clock.getTime()
        self.history[self.current_block][self.current_trial]['movement_onset_sensor_time'] = sensor_time
        
        # reset clock and speedometer
        # clock = core.Clock()
        # speedometer = Speedometer(mouse, clock)
        acc = math.inf
        acc_hist = []
        while acc > self.acc_thresh:
            acc = self.get_acc()
            acc_hist.append(acc)
        # record end of movement        
        self.history[self.current_block][self.current_trial]['movement_end'] = self.clock.getTime()

        mean_acc = stat.mean(acc_hist)
        self.history[self.current_block][self.current_trial]['acceleration'] = mean_acc

        return abs(((mean_acc - self.acc_thresh) / (self.max_acc - self.acc_thresh)) * (self.striker.top_coords[1] - self.striker.bottom_coords[1]))

    def run_block(self, trial_type: str):
        self.current_block += 1
        self.current_trial = 0
        self.history[self.current_block] = {}

        self.display_instructions(is_type_A)
        block_start = self.clock.getTime()
        while self.clock.getTime() < self.block_duration + block_start:
            self.run_trial(trial_type)

    # [NOTE]: add correct port address or the damn thing will never send triggers
    def run(self):
        # port = parallel.ParallelPort(address='0xDFF8')
        self.clock = core.Clock()
        # insert pulse to EEG
        # port.setData(1)
        self.post_pulse_time = self.clock.getTime()
        for trial_type in self.block_order:
            self.run_block(trial_type)


    def save_to_csv(self):
        top = ['session_ID: ' + str(self.session_id), 'post_pulse_time: ' + str(self.post_pulse_time)]
        header = list(['block_num', 'trial_num'] + list(list(list(self.history.values())[0].values())[0].keys()))

        contents = [ [block_num, trial_num] + list(self.history[block_num][trial_num].values()) for block_num in self.history for trial_num in self.history[block_num] ]

        with open(str(self.session_id) + '.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            csvwriter.writerow(top)
            csvwriter.writerow(header)
            csvwriter.writerows(contents)



    def display_instructions(self, is_type_A):
        message = visual.TextStim(self.window, text=self.instructions[is_type_A]+self.start_message, units='pix', height=50)
        message.draw()
        self.window.flip()
        
        while not event.getKeys():
            core.wait(.1)


    def get_acc(self, return_time=False):
        sample, timestamp = self.stream_inlet.pull_sample()

        # sample[11] for portable, sample[64] for actichamp
        if return_time:
            return sample[64], timestamp
        else:
            return sample[64]