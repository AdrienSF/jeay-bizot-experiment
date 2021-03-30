from psychopy import visual, core, event
from session import WhatSession

sess_id = input('enter session ID: ')
win = visual.Window(monitor='testMonitor', fullscr=True)
windowRect = win.size

session = WhatSession(win, sess_id)

try:
    session.run()
except KeyboardInterrupt:
    session.abort()


win.close()
core.quit()