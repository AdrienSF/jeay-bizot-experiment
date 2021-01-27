from psychopy import visual, core, event
from rate_bar import RateBar

win = visual.Window(monitor='testMonitor', fullscr=True)

rater = RateBar(win)

rater.draw()
win.flip()

print(rater.get_user_rating())

win.close()
core.quit()

