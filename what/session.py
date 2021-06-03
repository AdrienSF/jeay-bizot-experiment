from psychopy import visual, core, event   
from clock_stim import ClockStim
import random
import json
import csv
import pandas as pd

class Session(object):
    def __init__(self, win, sess_id, comp_device, experiment_execution):
        self.window = win
        self.id = sess_id
        self.frame_period = win.monitorFramePeriod
        self.port_ysno = (comp_device == 's')
        self.execution = experiment_execution
        self.cross = visual.TextStim(self.window, text='+', units='pix', height=50)
        if self.port_ysno:
            from psychopy import parallel
            self.port = parallel.ParallelPort(address=0xDFF8) 


    def run(self):
        for block_num in range(len(self.execution)):
            self.run_intermission(block_num=block_num)
            for trial_num in range(len(self.execution[block_num])):
                self.run_intermission(block_num=block_num, trial_num=trial_num)

                self.run_trial(block_num, trial_num)

        self.close()


    def run_intermission(self, block_num: int, trial_num=None):
        if trial_num != None: # then run trial intermission
            print('run_intermission() stub')
        else: # then run block intermission
            print('run_intermission() stub')


    def run_trial(self, block_num: int, trial_num: int):
        trial_type = self.execution[block_num][trial_num]['trial_type']

        if trial_type == 'A':
            print('run_trial() stub')
        elif trial_type == 'B':
            print('run_trial() stub')
        elif trial_type == 'C':
            print('run_trial() stub')
        else:
            print('trialNotFoundException')
            raise Exception()


    def close(self):
        # save session info to json and csv
        self.save_to_json()
        self.save_to_csv()
        
    def save_to_json(self):
        with open(str(self.id) + '.json', 'w') as json_file:
            to_save = {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key) and self.is_jsonable(value)}
            json_file.write(json.dumps(to_save))

    def save_to_csv(self): # the output of this usually doesn't make sense
        with open(str(self.id) + '.csv', 'w') as csv_file:
            to_save = {key:value for key, value in self.__dict__.items() if not key.startswith('__') and not callable(key) and self.is_jsonable(value)}
            csv_file.write(pd.DataFrame(to_save).to_csv())


    def is_jsonable(self, x):
        try:
            json.dumps(x)
            return True
        except (TypeError, OverflowError):
            return False

    def abort(self):
        self.aborted = True
        self.close()
        # close psychopy window
        self.window.close()
        raise KeyboardInterrupt('Session aborted')














class WhatSession(Session):
    def __init__(self, win, sess_id, comp_device):
        trial_types = ['C'] #['A', 'C','A', 'C','A', 'C','A', 'C','A', 'C','A', 'C','A', 'C','A', 'C','A', 'C','A', 'C']
        trials_per_block = 2 #20# to 20
        experiment_execution = [ [{'trial_type': trial_type} for i in range(trials_per_block)] for trial_type in trial_types ]

        super().__init__(win, sess_id, comp_device, experiment_execution)

        self.clock_stim = ClockStim(self.window)

        self.failure_message = visual.TextStim(win, 'Too slow!', units='pix', height=40)

        self.start_string = ''
        self.intermission_strings = {
            'A': 'Instructed: ',
            'B': 'Choose now',
            'C': 'Spontaneous'
            }



        # self.port = parallel.ParallelPort(address='0xDFF8')


    def run_trial(self, block_num: int, trial_num: int):
        # send trigger for start of trial
        # self.port.setData(1)
        if self.port_ysno:
            self.port.setData(5)
        clock = core.Clock()

        self.clock_stim.randomize_dot()
        while clock.getTime() < random.uniform(0.5, 1):
            self.cross.draw()
            self.clock_stim.draw(draw_target=False)
            self.clock_stim.rotate(self.frame_period) # make sure the timestep for rotating the clock dot is the refresh rate
            self.window.flip()

        self.clock_stim.randomize_target()
        if self.port_ysno:
            self.port.setData(6)
        self.execution[block_num][trial_num]['target_pos'] = str(self.clock_stim.target.pos)
        key_pressed = [None]
        collision_time = None
        log_failure = ''
        event.clearEvents()
        while not ('q' in key_pressed or 'p' in key_pressed):
            self.cross.draw()
            self.clock_stim.draw()
            self.clock_stim.rotate(self.frame_period) # make sure the timestep for rotating the clock dot is the refresh rate
            self.window.flip()

            key_pressed = event.getKeys()
            if 'escape' in key_pressed:
                self.core.quit()
            self.execution[block_num][trial_num]['button_press_time'] = clock.getTime()

            if collision_time:
                if clock.getTime() > collision_time + 1:
                    self.failure_message.draw()
                    self.window.flip()
                    log_failure = ' (failure)'
                    break
            elif clock.getTime() > 2.5 and abs(self.clock_stim.target.pos[0] - self.clock_stim.dot.pos[0]) < 4 and abs(self.clock_stim.target.pos[1] - self.clock_stim.dot.pos[1]) < 4:
                collision_time = clock.getTime()
        # Run spontaneity scale if type B        
        if (self.execution[block_num][trial_num]['trial_type'] == 'C'):
            ratingScale = visual.RatingScale(
                self.window, high=3, respKeys = ['1','2','3'], showAccept = True, scale = None, labels = ['Not at all', 'A little bit', 'Very'], 
                acceptPreText = "Select using: 1, 2 and 3 on the keyboard", acceptText = "\n Press ENTER to confirm", acceptSize = 3
                )
            item = visual.TextStim(self.window, "How spontaneous was your movement?", units='pix', height=40, wrapWidth=750)
            while ratingScale.noResponse:
                item.draw()
                ratingScale.draw()
                self.window.flip()
            rating = ratingScale.getRating()
            self.execution[block_num][trial_num]['spontaneous_rating'] = str(rating)
        # get time of button press
        self.execution[block_num][trial_num]['final_dot_pos'] = str(self.clock_stim.dot.pos) + log_failure
        self.execution[block_num][trial_num]['frame_radius'] = str(self.clock_stim.frame.radius)
        self.execution[block_num][trial_num]['button_pressed'] = str(key_pressed)
        # Get button ordered to be pressed
        self.execution[block_num][trial_num]['button_instructed'] = str(self.side_num)
        # send trigger for button press
        # self.port.setData(2)
        if self.port_ysno:
            self.port.setData(7)
        core.wait(0.5)
        event.clearEvents()

    def run_intermission(self, block_num: int, trial_num=None):
        # print(trial_num)
        if trial_num != None: # only do anything for trial intermissions. if trial_num is None then it is a block intermission, which is never included in this experiment.
            trial_type = self.execution[block_num][trial_num]['trial_type']

            if trial_type == 'A':
                self.side_num = random.choice(['q', 'p'])
                to_display = self.intermission_strings['A'] + str(self.side_num) + self.start_string
            elif trial_type == 'B':
                self.side_num = float("NaN")
                to_display = self.intermission_strings['B'] + self.start_string
            elif trial_type == 'C':
                self.side_num = float("NaN")
                to_display = self.intermission_strings['C'] + self.start_string
            else:
                print('trialNotFoundException')
                raise Exception()

            message = visual.TextStim(self.window, to_display, units='pix', height=40, wrapWidth=750)
            message.draw()
            self.window.flip()
            while not event.getKeys():
                pass


    def save_to_csv(self):
        top_info = ['id: ' + str(self.id), 'frame_period: ' + str(self.frame_period)]
        header = ['block_num', 'trial_num'] + list( self.execution[0][0].keys() )
        contents = [ [block_num+1, trial_num+1] + list(self.execution[block_num][trial_num].values()) for block_num in range(len(self.execution)) for trial_num in range(len(self.execution[block_num])) ]
        # 'trial_type', 'target_pos', 'final_dot_pos', 'button_press_time', 'button_pressed']


        with open(str(self.id) + '.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            csvwriter.writerow(top_info)
            csvwriter.writerow(header)
            csvwriter.writerows(contents)
