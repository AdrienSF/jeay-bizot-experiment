from psychopy import visual, core, event
from session import Session

# win = visual.Window([800, 600], monitor='testMonitor')

# mouse = event.Mouse(win=win)

# while not event.getKeys():
#     print(mouse.getPos())

win = visual.Window([800, 600], monitor='testMonitor')

sess = Session(win, None, None)

sess.mouse_test()