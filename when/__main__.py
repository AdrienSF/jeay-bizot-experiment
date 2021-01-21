from psychopy import visual, core, event
from high_striker import HighStriker
from traffic_light import TrafficLight
from session import Session
from pylsl import StreamInlet, resolve_stream
from calibrate import Calibrator


print("looking for stream...")
streams = resolve_stream('source_id', 'myuid323457') # for ActiChamp - 17010768

inlet = StreamInlet(streams[0], max_buflen=1) # for ActiChamp (I think streams[1])
print('found')


sess_id = input('enter session ID: ')
win = visual.Window(monitor='testMonitor', fullscr=True)
windowRect = win.size

light = TrafficLight(win)

calibrator = Calibrator(win, light, inlet)

acc_thresh, max_acc = calibrator.calibrate()

safe_thresh = .1*(max_acc - acc_thresh) + acc_thresh
safe_max = max_acc - .2*(max_acc - acc_thresh)


striker = HighStriker(win, top_coords=(0, windowRect[1]/2-100), bottom_coords=(0, -1*(windowRect[1]/2-100)))

session = Session(win, striker, light, session_id=sess_id, sensor_input_stream=inlet, acc_thresh=safe_thresh, max_acc=safe_max)

session.run()

session.save_to_csv()



win.close()
core.quit()