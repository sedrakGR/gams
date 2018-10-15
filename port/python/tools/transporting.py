from data_reader_interface import DataReaderFromFile
import data_reader_interface as dri
# import visualizer as vis
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
from time import sleep
import sys
import numpy as np
import madara
from madara.knowledge import Any
import madara.knowledge as engine
import madara.transport as transport
import madara.filters as filters
import gams
import gams.pose as gp
import capnp
import os
import time
from madara.knowledge import Any
from madara.knowledge.containers import NativeCircularBufferConsumer
# from type_registry import CompressedMap

rf = gp.ReferenceFrame()
fes = gp.FrameEvalSettings()

# create transport settings for a multicast transport
if __name__ == "__main__":
    settings = transport.QoSTransportSettings()
    settings.hosts.append("tcp://127.0.0.1:40001")
    settings.hosts.append("tcp://127.0.0.1:40000")
    settings.type = transport.TransportTypes.ZMQ
    settings.queue_length = 100000000
    settings.read_threads = 1
    settings.read_thread_hertz = 1000

    # create a knowledge base with the multicast transport settings
    kb = engine.KnowledgeBase('', settings)
    # kb.attach_transport('', settings)
    # kb.activate_transport()
    # kb.wait_for_change()
    # set our id to 0 and let the other agent know that we are ready
    # kb.set(".id", 0)
    # kb.set("agent{.id}.ready", 1)

    kb.print_knowledge()
    # kb.to_map()


    # save_to_file = False
    # path = '/home/shobhit/map_data/'

    frame_counter = 0
    while True:
        print 'hi'
        record = kb.get(
            'sensors.imu')

        if record.exists():
            compressed_map = record.to_any().reader()
            print("Got record at time ", compressed_map.header.tov)
            kb.print_knowledge()

            # Construct a buffer
            arr = np.array(compressed_map.data, dtype=np.uint8)

            # # Construct frame from bytes
            # frame = cv2.imdecode(arr, -1)
            # frame = numpy.reshape(
            #     frame, (compressed_map.width, compressed_map.height), order='C')
            # numpy.place(frame, frame == 255, 128)

            # resized_frame = cv2.resize(frame, (1000, 1000))

            # cv2.imshow('Map', resized_frame)
            # cv2.waitKey(10)

            # frame_counter = frame_counter + 1
            # if save_to_file:
            #     cv2.imwrite(path + '{0:05d}'.format(frame_counter), frame)
        time.sleep(1 / 5)



# settings = engine.CheckpointSettings()
# settings.prefixes('.gams.frames.p1_base_footprint')
# kb.to_map()