# Experiment spec:
## Experiment structure:
Run trials until 15 min have passed.

## Trial spec:
Input elements:

sensor measuring the y (vertical) position of the subject’s finger

Graphical elements:
- Grey background
- black vertical centered bar always displayed: thick enough to be clearly visible, leave some top and bottom  margin (gap between bar and top/bottom of screen)
- alternating green “ON” word/ red “OFF” word: fits on right half of screen
- a “slider” circle: white, 10px radius, filled
- a “target” circle: red, 20px radius, not filled but thick enough line to be clearly visible

## Timing and location:
- display bar throughout trial, leave some top and bottom margin (gap between bar and top/bottom of screen)


at start of trial: 
- display “OFF”  on right half of screen, just above the bottom half of screen
- display “slider” at the bottom of the bar (on the bar)
- (don’t display ”target” or”OFF”)


after 1s:
- remove “OFF”
- display “ON” on right half of screen, just below top half of screen (just below “OFF)
- display “target” in a random location on the upper ⅔ of the bar


start monitoring the finger sensor:
- when y coordinates first increase (change of y in time is above threshold T), start recording
- when y coordinates stop increasing (change of y in time is below threshold T), stop recording


stop monitoring motion sensor
- remove “ON”, display “OFF”
- get average speed S of the recorded movement
- over the course of 700ms, move the “slider” up by a distance D proportional to S


wait 1s
end trial

## Logic and data collection:
Threshold T:

T should not pick up minor movements. Rather it should be such that only full finger movements (fingertip is displaced intentionally) are recorded. For instance, twitches etc. should all remain below T.

Distance D:

Travelled distance D should be set to:<br>
D = S\*max(S)/max(D)<br>
where max(S) is calibrated on a participant by participant basis at the start of each session and represents the maximal speed participants can achieve when instructed to maximize their finger’s speed (for now we can set this value to an arbitrary value of c) . And max(D) is equal to the bar length.
