from psychopy import visual, core, event
from high_striker import HighStriker
from traffic_light import TrafficLight
from session import Session
from pylsl import StreamInlet, resolve_stream

print("looking for stream...")
streams = resolve_stream('source_id', '17010768') 

inlet = StreamInlet(streams[1])
print('found')


sess_id = input('enter session ID: ')
win = visual.Window(monitor='testMonitor', fullscr=True)
windowRect = win.size
# print(windowRect)
# exit(0)
light = TrafficLight(win)

striker = HighStriker(win, top_coords=(0, windowRect[1]/2-100), bottom_coords=(0, -1*(windowRect[1]/2-100)))

session = Session(win, striker, light, session_id=sess_id, sensor_input_stream=inlet)

session.run()

session.save_to_csv()



win.close()
core.quit()