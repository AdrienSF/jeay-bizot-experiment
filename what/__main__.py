from psychopy import visual, core, event
from session import WhatSession

sess_id = input('enter session ID: ')
comp_device = input('are you on the stimulus comp (s) or at home (h): ')
win = visual.Window(monitor='testMonitor', fullscr=True)
windowRect = win.size

session = WhatSession(win, sess_id, comp_device)

try:
    session.run()
except KeyboardInterrupt:
    session.abort()


win.close()
core.quit()