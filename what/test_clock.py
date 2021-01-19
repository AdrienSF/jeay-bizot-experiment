from psychopy import visual, core, event
from clock_stim import ClockStim

win = visual.Window(monitor='testMonitor', fullscr=True)

libet_clock = ClockStim(win)

libet_clock.randomize_dot()
libet_clock.randomize_target() 

while not event.getKeys():
    libet_clock.rotate()
    libet_clock.draw()
    win.flip()


win.close()
core.quit()
