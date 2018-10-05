from data_reader_interface import DataReaderFromFile
import data_reader_interface as dri
import visualizer as vis
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
from time import sleep
import numpy as np
from stone_test_any import deserializer as dsrl
import madara
import madara.knowledge as engine
import gams.pose as gp

rf = gp.ReferenceFrame()
kb = engine.KnowledgeBase()
fes = gp.FrameEvalSettings()

# filename = ("/home/stallone/data/output/agent.0/"
#                         "SAFE_reliability_rc_v3.4.0__pikachu-16-0004__2018-08-16-09-47-39.stk")
# reader = DataReaderFromFile(filename)

# prefix1 = '.gams.frames.p1_base_footprint'
# suffix = '.origin'
# keys = reader.get_keys()

# pause = False

# def onClick(event):
#     global pause
#     pause ^= True

# x = []
# y = []
# z = []
# rx = []
# ry = []
# rz = []
# for key in keys:
#     if key.startswith(prefix1):
#         last_value = ''
#         count = 0
#         while True:
#             value, has_next = reader.get_current_value(key)
#             # if (value.to_string() == last_value):
#             #     sleep(1)
#             #     if not(has_next):
#             #         break
#             #     continue
#             kb.set(key, value.to_any())
            
#             # print key
#             # print value.to_string()
#             # print type(value)
#             # press = dsrl(value)
#             # print value.retrieve_index(0).to_double()
#             # print value.retrieve_index(1).to_double()
#             # print value.retrieve_index(2).to_double()
#             # x.append(value.retrieve_index(0).to_double())
#             # y.append(value.retrieve_index(1).to_double())
#             # z.append(value.retrieve_index(2).to_double())
#             # rx.append(value.retrieve_index(3).to_double())
#             # ry.append(value.retrieve_index(4).to_double())
#             # rz.append(value.retrieve_index(5).to_double())

#             # if not(value.to_string() == last_value):
#             #     last_value = value.to_string()
#             #     print last_value
#             # if not(has_next):
#             #     break
#         # print(value.retrieve_index(0).to_string(), value.retrieve_index(1).to_string(), value.retrieve_index(2).to_string(),
#             # value.retrieve_index(3).to_string(), value.retrieve_index(4).to_string(), value.retrieve_index(5).to_string())

#             #vis.plt.draw()

# #             vis.visualizer(x, y, z, rx, ry, rz)


settings = engine.CheckpointSettings()
# settings.prefixes('.gams.frames.p1_base_footprint')
settings.filename = ("/home/stallone/data/output/agent.0/"
                        "SAFE_reliability_rc_v3.4.0__pikachu-16-0004__2018-08-16-09-47-39.stk")

# # Read in if binary file 
# kb.load_context(settings.filename) 

reader = engine.CheckpointReader(settings)

# map = dict(list(reader))
# print map.values()[2].toi()

prefix = '.gams.frames'
prefix1 = '.gams.frames.p1_base_footprint'
prefix2 = '.gams.frames.p1_map'
prefix3 = '.gams.frames.p1_odom'
suffix = '.origin'
suffix1 = '.toi'
suffix2 = '.parent'

# Get KRs and make into list
TOIs = []
x = []
y = []
z = []
u = []
v = []
w = []

for key, value in reader: 
    if prefix in key and not suffix1 in key:
        # key = key.split('.')
        # key = key[3]
        # print(key, value.to_string())
        kb.set(key, value)

rf = gp.ReferenceFrame()

kb.print_knowledge()
trans_frames = gp.ReferenceFrame.load_tree(kb, 
    madara.from_pystrings(['geo','p1_map']) , 18446744073709551615, fes )

# trans_frames[0].origin().transform_to(trans_frames[1])
# vis.plt.show()