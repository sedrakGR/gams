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
import yaml 
import sys

# Specify file path where the .yaml file is located
file_path = 'port/python/tools/config.yaml'

def yaml_loader(filepath):
    """ Loads a yaml file """
    with open(file_path, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def capnp_crunch(key, value):
    schema = key_to_capnpfile[key]
    schema_file = capnp.load('/home/stallone/shield_schemas/shield/'+ schema +'.capnp', 
            imports=[os.environ['CAPNP_ROOT'] + '/c++/src'])    
    Any.register_class(schema, getattr(schema_file, schema))
    new_value = value.to_any().reader()
    return new_value  

def print_dict(dictionary, ident = '', braces=1):
    """ Recursively prints nested dictionaries."""
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print '%s%s%s%s' %(ident,braces*'[',key,braces*']') 
            print_dict(value, ident+'  ', braces+1)
        else:
            print ident+'%s = %s' %(key, value)



user_specs = yaml_loader(file_path)
print user_specs

if user_specs['data_source']['stk_file']:
    source = user_specs['data_source']['stk_file']      # string
elif user_specs['data_source']['transport']:
    source = user_specs['data_source']['transport']    # string
else: 
    print('You have not specified a data source to read from!')
    sys.exit()

settings = engine.CheckpointSettings()
settings.filename = source
reader = engine.CheckpointReader(settings)

key_to_capnpfile = {}
key_to_capnpfile = {key: value.to_any().tag() for key, value in reader if value.is_any_type()}

# reader = DataReaderFromFile(source)

# print user_specs

# Display all knowledge records--------------------------------------------------

frame_prefix = '.gams.frames'
any_prefix = 'sensors.camera.color_compressed'
origin_suffix = '.origin'
toi_suffix = '.toi'
parent_suffix = '.parent'
index_suffix = '.index'
size_suffix = '.size'

reader = engine.CheckpointReader(settings)

any_KRs = []
frame_KRs = []
for key, value in reader:
    if (not key.endswith(index_suffix) and not key.endswith(size_suffix) and not
                        key.endswith(toi_suffix) and not key.endswith(parent_suffix)):
        # print key, type(value)
        if frame_prefix in key:
            key = key.split('.')
            key = key[3]
            # key = ('.').join(key[0:4])
            if key not in frame_KRs:
                frame_KRs.append(key)
        else: 
            if key not in any_KRs:
                any_KRs.append(key)

any_KRs.sort()
frame_KRs.sort()

print ('\n---------------------------------Any Type Data-----------------------------------\n')

if len(any_KRs) % 2 != 0:
    any_KRs.append(" ")

split = len(any_KRs)/2
l1 = any_KRs[0:split]
l2 = any_KRs[split:]
for key, value in zip(l1,l2):
    print "{0:<45s} {1}".format(key, value) 

print ('\n---------------Frame Type Data---------------\n')

if len(frame_KRs) % 2 != 0:
    frame_KRs.append(" ")

split = len(frame_KRs)/2
l1 = frame_KRs[0:split]
l2 = frame_KRs[split:]
for key, value in zip(l1,l2):
    print "{0:<30s} {1}".format(key, value) 

#------------------------------------------------------------------
# View KR data format 

# Determine what KRs the user would like to be plotted 

if user_specs['knowledge_record']['frame_types']:
    frame_lookup = user_specs['knowledge_record']['frame_types']   # list
else: 
    frame_lookup = []
if user_specs['knowledge_record']['any_types']:
    any_lookup = user_specs['knowledge_record']['any_types']     # list 
else: 
    any_lookup = []


if frame_lookup or any_lookup:
    lookup = frame_lookup + any_lookup 
    for kr in lookup:
        cnt = 0
        reader = engine.CheckpointReader(settings)
        for key, value in reader:
            if kr == key in key or kr in key:
                if (value.is_any_type() and not key.endswith(index_suffix) 
                            and not key.endswith(size_suffix)):
                    # print(key, value.to_any().tag())
                    new_value = capnp_crunch(key, value)
                    new_value = new_value.to_dict()
                    print ('\n' + key + ' data format:\n')
                    print_dict(new_value)
                    cnt += 1
                if (not value.is_any_type() and not key.endswith(parent_suffix) 
                            and not key.endswith(toi_suffix)):
                    cnt += 1
                    key = key.split('.')
                    key = key[3] 
                    print ('\n' + key + ' data format:\n')
                    print('     ' + value.to_string())
            if cnt == 1:
                break

else:    
    print('You have not specified any knowledge records!')
    sys.exit()
