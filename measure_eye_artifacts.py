from psychopy import visual, core, event
import random
import numpy as np

sess_id = input('enter sess_id: ')
win = visual.Window(monitor='testMonitor', fullscr=True)
delay = 1
iterations = 10


stim = visual.TextStim(
    win=win,
    color='white',
    text='+'
)


# generate and save list of positions
positions = [ (np.random.choice([-0.8,0, 0.8]), np.random.choice([-0.8,0, 0.8])) for _ in range(iterations) ]
with open(str(sess_id)+'.csv', 'w') as f:
    f.write('delay='+str(delay)+'\n')
    for pos in positions:
        f.write(str(pos)+'\n')



# loop through a list of positions
for pos in positions:
    stim.pos = pos
    stim.draw()
    win.flip()
    core.wait(delay)
    stim.pos = (0,0)
    stim.draw()
    win.flip()
    core.wait(delay)


win.close()
core.quit()