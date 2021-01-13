from psychopy import visual, core, event
from high_striker import HighStriker
from traffic_light import TrafficLight
from session import Session
from pylsl import StreamInlet, resolve_stream

print("looking for stream...")
streams = resolve_stream('type', '???') # what kind of stream is the motion sensor using? do we connect to it via an ID no.?

inlet = StreamInlet(streams[0])

win = visual.Window(monitor='testMonitor', fullscr=True)
windowRect = win.size
# print(windowRect)
# exit(0)
light = TrafficLight(win)

striker = HighStriker(win, top_coords=(0, windowRect[1]/2-100), bottom_coords=(0, -1*(windowRect[1]/2-100)))


session = Session(win, striker, light, inlet)# not supposed to be mouse but instead an input stream from sensor

session.run()

core.wait(3)



win.close()
core.quit()