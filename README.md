# WHEN Experiment spec:
## Experiment structure:
Run 2 blocks of 5 minutes. 

For the first block the subject is instructed to launch the slider wherever and whenever, as many times as wanted during the 5 minutes (as long as the on signal is displayed). First block runs 5 minutes of A trials.

For the second block the subject is instructed to aim for the target. Second block runs 5 minutes of B trials


## B Trial spec:
Input elements:

sensor measuring the y (vertical) position of the subject’s finger

Graphical elements:
- Grey background
- black vertical centered bar always displayed: thick enough to be clearly visible, leave some top and bottom  margin (gap between bar and top/bottom of screen)
- alternating green “ON” word/ red “OFF” word: fits on right half of screen
- a “slider” circle: white, 10px radius, filled
- a “target” circle: red, 20px radius, not filled but thick enough line to be clearly visible

### Timing and position:
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

### Logic and data collection:
Threshold T:

T should not pick up minor movements. Rather it should be such that only full finger movements (fingertip is displaced intentionally) are recorded. For instance, twitches etc. should all remain below T.

Distance D:

Travelled distance D should be set to:<br>
D = S\*max(S)/max(D)<br>
where max(S) is calibrated on a participant by participant basis at the start of each session and represents the maximal speed participants can achieve when instructed to maximize their finger’s speed (for now we can set this value to an arbitrary value of c) . And max(D) is equal to the bar length.

## A Trial spec:
Same as B but never display the "target" circle.


# WHAT Experiment spec:
## Experiment structure:
Run 3 blocks of 10 trials each. 

For the first block the subject is instructed at the start of each trial to press a left or right button once the clock's hand reaches a randomly positioned target.

For the second block the subject is instructed to decide before the start of each trial to press the left or right button once the clock's hand reaches a randomly positioned target.

For the third block the subject is instructed to spontaneously press the left or right button once the clock's hand reaches a randomly positioned target. The participants are specifically instructed to NOT make their decisions until the very last moment. 

## A Trial spec:
Input elements:
- input from two keyboard keys (one on the left-side of the keyboard: Q and one on the right-side of the keyboard: P)
- input from spacebar

Graphical elements:
- Grey background
- Libet type clock (a white circle along which a clock hand rotates)
- Clock hand ( a white dot, 10 pix, that rotates around the Libet type clock in a 5s period)
- A "target" ( a red circle, 20 pix, that appears randomly positioned along the Libet type clock circle and stays fixed for the whole trial)
	- the "target" must appear randomly within a 1.5s to 2.5s range after the start of the trial (uniformly distributed)
	- the "target" must appear in the half circle that precedes the clock hand at the time of appearance

Instructions: "When the clock's hand reaches the target (red circle) press the $ button" (where $ is randomly picked amongst {Left, Right}). When you are ready to start, press the spacebar"

### B Trial spec:

Same as Trial A except for instructions

Instructions: "Decide for button between Left and Right now and press it when the clock's hand reaches the target (red circle). When you are ready to start, press the spacebar" 

### C Trial spec:

Same as Trial A except for instructions

Instructions: "Withold any decision about Left or Right button press and make this decision as spontaneously as possible once the clock's hand reaches the target (red circle). When you are ready to start, press the spacebar"

### Timing and position:
- display clock circle throughout trial, clock diameter should be about a third of the screen's height.


before the start of trial:
- display condition instruction until 'spacebar is pressed'
 
start of trial:
- display clock with the clock hand (random initial position) - the clock hand should be rotating straight away (at the pace of 1 full rotation per 5 seconds)

end of trial:
- once a button has been pressed stop the clock hand at its current position wait 1s and move on to the next trial

### Data collection:

Record for each trial:
- trial type
- block number
- target position
- position at time of button press
- time of button press with respect to trial start (target appearance)
- button pressed (left - right)
