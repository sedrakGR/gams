from data_reader_interface import DataReaderFromFile
import data_reader_interface as dri
# import visualizer as vis
from matplotlib.widgets import Button
import matplotlib.pyplot as plt
from time import sleep
import numpy as np
from stone_test_any import deserializer as dsrl
import madara
from madara.knowledge import Any
import madara.knowledge as engine
import gams
import gams.pose as gp
import capnp
import os

rf = gp.ReferenceFrame()
kb = engine.KnowledgeBase()
fes = gp.FrameEvalSettings()

def print_dict(dictionary, ident = '', braces=1):
    """ Recursively prints nested dictionaries."""

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print '%s%s%s%s' %(ident,braces*'[',key,braces*']') 
            print_dict(value, ident+'  ', braces+1)
        else:
            print ident+'%s = %s' %(key, value)

#---------------------------------------------------------------------------------------
# ReferenceFrame type doodling

settings = engine.CheckpointSettings()
# settings.prefixes('.gams.frames.p1_base_footprint')
settings.filename = ("/home/stallone/data/output/agent.0/"
                        "SAFE_reliability_rc_v3.4.0__pikachu-16-0004__2018-08-16-09-47-39.stk")

# # Read in if binary file 
# kb.load_context(settings.filename) 

reader = engine.CheckpointReader(settings)


# Get KRs and make into list
TOIs = []
last_timestamp = 0

# frame_of_choice = 'p1_base_footprint'

# for key, value in reader: 
#     if key.startswith(prefix) and not key.endswith(suffix1):
#         # key = key.split('.')
#         # key = key[3]
#         # print(key, value.to_string())
#         kb.set(key, value)

#         if key.endswith(suffix2):
#             # kb.print_knowledge()
#             try:
#                 trans_frames = gp.ReferenceFrame.load_tree(kb, 
#                     madara.from_pystrings(['geo',frame_of_choice]) , 18446744073709551615, fes )

#                 if trans_frames[1].timestamp() > last_timestamp:
#                     coord = trans_frames[1].origin().transform_to(trans_frames[0])
#                     print(trans_frames[1].timestamp(), ": ", coord.to_string())
#                     last_timestamp = trans_frames[1].timestamp()
#                     sleep(0.01)
#             except:
#                 pass


# # # vis.plt.show()

#------------------------------------------------------------------------------------
# Any type doodling

# fp = capnp.load("/home/stallone/shield_schemas/shield/IMU.capnp", 
#      imports=[os.environ["CAPNP_ROOT"] + "/c++/src"])

key_to_capnpfile = {}
key_to_capnpfile = {key: value.to_any().tag() for key, value in reader if value.is_any_type()}

# print key_to_capnpfile

def capnp_crunch(key, value):
    schema = key_to_capnpfile[key]
    # print ('Schema string:' + schema_str)
    # print ('/home/stallone/shield_schemas/shield/'+ schema +'.capnp')
    # parser = capnp.SchemaParser()
    # schema_file = parser.load('/home/stallone/shield_schemas/shield/'+ schema +'.capnp')
    # print getattr(schema_file, schema)
    # schema_name = capnp.load_schema('/home/stallone/shield_schemas/shield/'+ schema )
    schema_file = capnp.load('/home/stallone/shield_schemas/shield/'+ schema +'.capnp', 
            imports=[os.environ['CAPNP_ROOT'] + '/c++/src'])    

    Any.register_class(schema, getattr(schema_file, schema))
    new_value = value.to_any().reader()
    return new_value      

frame_prefix = '.gams.frames'
any_prefix = 'sensors.camera.color_compressed'
prefix2 = '.gams.frames.p1_map'
suffix = '.origin'
suffix1 = '.toi'
suffix2 = '.parent'

reader = engine.CheckpointReader(settings)

variables = []
for key, value in reader:
    if value.is_any_type() and not suffix1 in key:
        if key not in variables:
            variables.append(key)

# print variables   

reader = engine.CheckpointReader(settings)


for variable in variables[82:]:
    cnt = 0
    print variable
    reader = engine.CheckpointReader(settings)
    for key, value in reader: 
        if value.is_any_type() and key.startswith(variable) and not 'echo' in variable:
            new_value = capnp_crunch(key, value)
            new_value = new_value.to_dict()
            print(key, value.to_any().tag())
            print_dict(new_value)
            # list_choices1 = new_value.keys()
            # print new_value
            sleep(0.3)
            cnt += 1
        if cnt == 1:
            break

        # key_hierarchy = {key : value for key, value in new_value.items()}
        # print key_hierarchy
        # print new_value.keys()
        # print new_value['pose']['position']['x']
        # print new_value.values()[1].keys()
        # print new_value.values()[1].keys()[0].keys()
        # print new_value['pose']['pose']['position']['x']
        # first_level_keys = []
        # second_level_keys = []
        # third_level_keys = []


        # # for key, value in new_value.items():
        # #     first_level_keys.append(key)
        # #     if type(value) == dict:
        # #         sub_key = new_value
        # #         second_level_keys.append(new_value[key][key].keys())
        # #         for key, value in new_value[key].items():
        # #             if type(value) == dict: 
        # #                 third_level_keys.append(new_value[key].keys())

        # print list(new_value)

        # first_level_keys = new_value.keys()
        # for key, value in new_value.items(:)
        #     second_level_keys.append() = new_value[key].keys()
        #     for key, value in new_value[key].items()
        #         if 


        # print first_level_keys    
        # print second_level_keys
        # print third_level_keys
            
            #     first_level.append(value)
            #     for key, value in new_value[key]:
            #         if value.is_dict():
            #             for key, value in new_value[key]:

            # else:
            #     key_hierarchy[key] = value


        # myprint(new_value)
        # print new_value.get('pose')
        # print(key, new_value)
        # print new_value
        # print new_value.velocity.linear.x
        # sleep(0.1)
        
        # key = key.split('.')
        # key = key[3]
        # print(key, value.to_string())
        # sleep(0.3)

        # kb.set(key, value)
        # c = kb.get('sensors.baro')


# kb.print_knowledge()



# Any.register_class("IMU", fp.IMU)



#    


# trans_frames = gams.from_pyframes(gp.ReferenceFrame.load_tree(kb, 
#     madara.from_pystrings(['geo','p1_base_link']) , 18446744073709551615, fes ))

# trans_frames[1].origin().transform_to(trans_frames[0])
# vis.plt.show()





# def dict_generator(indict, pre=None):
#     pre = pre[:] if pre else []
#     if isinstance(indict, dict):
#         for key, value in indict.items():
#             if isinstance(value, dict):
#                 for d in dict_generator(value, [key] + pre):
#                     yield d
#             elif isinstance(value, list) or isinstance(value, tuple):
#                 for v in value:
#                     for d in dict_generator(v, [key] + pre):
#                         yield d
#             else:
#                 yield pre + [key, value]
#     else:
#         yield indict

# def myprint(d):
#   for k, v in d.iteritems():
#     if isinstance(v, dict):
#       myprint(v)
#     else:
#       print "{0} : {1}".format(k, v)

# key_hierarchy = {}

# list_KRs = []
# for key, value in reader:
#         if value.is_any_type() and key not in list_KRs:
#                 list_KRs.append(key)

# print list_KRs

# list_KRs = np.c_[list_KRs]
# # list_KRs = enum(list_KRs)
# user_input = raw_input('What KR would you like to plot?\n' + str(list_KRs))
# print user_input