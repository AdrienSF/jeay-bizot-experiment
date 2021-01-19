from psychopy import visual, core, event, parallel
from clock_stim import ClockStim
import random
import json
import csv
import pandas as pd

class Session(object):
    def __init__(self, win, sess_id, experiment_execution):
        self.window = win
        self.id = sess_id
        self.frame_period = win.monitorFramePeriod

        self.execution = experiment_execution
        self.cross = visual.TextStim(self.window, text='+', units='pix', height=50)


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















class WhatSession(Session):
    def __init__(self, win, sess_id):
        trial_types = ['A', 'B', 'C']
        trials_per_block = 1
        experiment_execution = [ [{'trial_type': trial_type} for i in range(trials_per_block)] for trial_type in trial_types ]

        super().__init__(win, sess_id, experiment_execution)

        self.clock_stim = ClockStim(self.window)

        self.failure_message = visual.TextStim(win, 'damn, to slow you loser', units='pix', height=40)

        self.start_string = '\n\nWhen you are ready to start, press any key.'
        self.intermission_strings = {
            'A': 'When the clock\'s hand reaches the target (red circle) press ',
            'B': 'Decide for button between Left and Right now and press it when the clock\'s hand reaches the target (red circle).',
            'C': 'Withold any decision about Left or Right button press and make this decision as spontaneously as possible once the clock\'s hand reaches the target (red circle).'
            }



        # self.port = parallel.ParallelPort(address='0xDFF8')


    def run_trial(self, block_num: int, trial_num: int):
        # send trigger for start of trial
        # self.port.setData(1)
        clock = core.Clock()

        self.clock_stim.randomize_dot()
        while clock.getTime() < random.uniform(1.5, 2.5):
            self.cross.draw()
            self.clock_stim.draw(draw_target=False)
            self.clock_stim.rotate()
            self.window.flip()

        self.clock_stim.randomize_target()
        self.execution[block_num][trial_num]['target_pos'] = str(self.clock_stim.target.pos)
        key_pressed = [None]
        collision_time = None
        log_failure = ''
        event.clearEvents()
        while not ('q' in key_pressed or 'p' in key_pressed):
            self.cross.draw()
            self.clock_stim.draw()
            self.clock_stim.rotate(self.frame_period/2) # make sure the timestep for rotating the clock dot is less than the refresh rate
            self.window.flip()

            key_pressed = event.getKeys()
            self.execution[block_num][trial_num]['button_press_time'] = clock.getTime()

            if collision_time:
                if clock.getTime() > collision_time + 1:
                    self.failure_message.draw()
                    self.window.flip()
                    log_failure = ' (failure)'
                    break
            elif clock.getTime() > 2.5 and abs(self.clock_stim.target.pos[0] - self.clock_stim.dot.pos[0]) < 4 and abs(self.clock_stim.target.pos[1] - self.clock_stim.dot.pos[1]) < 4:
                collision_time = clock.getTime()

        # get time of button press
        self.execution[block_num][trial_num]['final_dot_pos'] = str(self.clock_stim.dot.pos) + log_failure
        self.execution[block_num][trial_num]['button_pressed'] = str(key_pressed)
        # send trigger for button press
        # self.port.setData(2)
        core.wait(2)


    def run_intermission(self, block_num: int, trial_num=None):
        # print(trial_num)
        if trial_num != None: # only do anything for trial intermissions. if trial_num is None then it is a block intermission, which is never included in this experiment.
            trial_type = self.execution[block_num][trial_num]['trial_type']

            if trial_type == 'A':
                to_display = self.intermission_strings['A'] + str(random.choice(['q', 'p'])) + self.start_string
            elif trial_type == 'B':
                to_display = self.intermission_strings['B'] + self.start_string
            elif trial_type == 'C':
                to_display = self.intermission_strings['C'] + self.start_string
            else:
                print('trialNotFoundException')
                raise Exception()

            message = visual.TextStim(self.window, to_display, units='pix', height=40)
            message.draw()
            self.window.flip()
            while not event.getKeys():
                pass



    def save_to_csv(self):
        top_info = ['id: ' + str(self.id), 'frame_period: ' + str(self.frame_period)]
        header = ['block_num', 'trial_num'] + list( self.execution[0][0].keys() )
        contents = [ [block_num, trial_num] + list(self.execution[block_num][trial_num].values()) for block_num in range(len(self.execution)) for trial_num in range(len(self.execution[block_num])) ]
        # 'trial_type', 'target_pos', 'final_dot_pos', 'button_press_time', 'button_pressed']


        with open(str(self.id) + '.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            csvwriter.writerow(top_info)
            csvwriter.writerow(header)
            csvwriter.writerows(contents)
