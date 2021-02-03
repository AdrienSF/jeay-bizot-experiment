from psychopy import visual, core, event
from rate_bar import RateBar

win = visual.Window(monitor='testMonitor', fullscr=True)

ratingScale = visual.RatingScale(
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
while ratingScale.noResponse:
    ratingScale.draw()
    win.flip()
rating = ratingScale.getRating()

print(rating)

win.close()
core.quit()

