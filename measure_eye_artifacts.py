from psychopy import visual, core, event
import random
import numpy as np
from psychopy import parallel

port = parallel.ParallelPort(address=0xDFF8) 
sess_id = input('enter sess_id: ')
win = visual.Window(monitor='testMonitor', fullscr=True)
delay = 1
iterations = 150
eye_blink_time = 60 * 2


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
port.setData(6)
for pos in positions:
    stim.pos = pos
    stim.draw()
    win.flip()
    core.wait(delay)
    stim.pos = (0,0)
    stim.draw()
    win.flip()
    core.wait(delay)
    port.setData(7)
port.setData(6)


# Do eyeblinks
message = "Do eyeblinks every 2 seconds now"
instr = visual.TextStim(
    win=win,
    color='white',
    text=message
)

instr.draw()
win.flip()
core.wait(3)
port.setData(5)
stim.pos = (0,0)
stim.draw()
win.flip()
core.wait(eye_blink_time)
port.setData(5)


win.close()
core.quit()