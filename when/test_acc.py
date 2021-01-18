from pylsl import StreamInlet, resolve_stream
from psychopy import visual, core, event, parallel
import statistics as stat


print("looking for stream...")
streams = resolve_stream('source_id', '17010768') 

inlet = StreamInlet(streams[0])
print('found')

samples = []
while True:
    sample, timestamp = inlet.pull_sample()
    samples.append(sample[65])

    print(stat.mean(samples))

    # clock = core.Clock()
    # samples = []
    # while clock.getTime() < .1:
    #     sample, timestamp = inlet.pull_sample()

    #     samples.append(sample[66]-210)


    # print( "".join([ '.' for i in range(int(stat.mean(samples)))]) )