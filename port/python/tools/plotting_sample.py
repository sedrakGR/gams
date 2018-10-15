from data_reader_interface import DataReaderFromFile
from plotting import Plotter
import matplotlib.pyplot as plt
import yaml
import sys

def yaml_loader(filepath):
    """ Loads a yaml file """
    with open(file_path, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

file_path = 'port/python/tools/config.yaml'
user_specs = yaml_loader(file_path)
# print user_specs

    # items = data.get('items')
    # for item_name, item_value in items.iteritems():
    #     print item_name, item_value

# Read in the file. Checks to see if each type is present 
if user_specs['data_source']['stk_file']:
    source = user_specs['data_source']['stk_file']      # string
elif user_specs['data_source']['transport']:
    source = user_specs['data_source']['transport']    # string
else:
    print('You have not specified a data source to read from!')
    sys.exit()

# Parse data for schema file
if user_specs['data_source']['schemas']:
    schemas = user_specs['data_source']['schemas']
else:
    print('You have not specified schema files!')
    sys.exit()

reader = DataReaderFromFile(schemas, source)

# Determine what KRs the user would like to be plotted
if user_specs['knowledge_record_subkeys']['frame_types']:
    f_type_dict = user_specs['knowledge_record_subkeys']['frame_types']   # list
else: 
    f_type_dict = {}
if user_specs['knowledge_record_subkeys']['any_types']:
    a_type_dict= user_specs['knowledge_record_subkeys']['any_types']     # list
else: 
    a_type_dict = {}

if not(a_type_dict or f_type_dict):
    print('You have not specified any knowledge records!')
    sys.exit()

######################## Frame type data parsing ##########################
frame_KRs = user_specs['knowledge_record_subkeys']['frame_types']

for key, value in frame_KRs.items():
    sub_plot_list = []
    print key, value
    # print value.keys()
    if not value: 
        plt2 = Plotter(reader, '.gams.frames.'+ key)
        continue
    if 'reference_frame' in value.keys():
        reference_frames = frame_KRs[key]['reference_frame']
        for subkey in value.keys():
            if 'plot' in subkey:
                sub_plot_list.append(frame_KRs[key][subkey].items())
                plt7 = Plotter(reader, '.gams.frames.' + key, frames_of_choice=reference_frames,
                            subkeys=sub_plot_list, points_per_plot=10)
            else: 
                plt4 = Plotter(reader, '.gams.frames' + key, frames_of_choice=['geo','p1_base_footprint'])
    else: 
        for subkey in value.keys():
            if 'plot' in subkey:
                sub_plot_list.append(frame_KRs[key][subkey].items())
                print sub_plot_list
            plt3 = Plotter(reader, '.gams.frames.' + key, 
                            subkeys=sub_plot_list, points_per_plot=10)


######################## Any type data parsing ##########################   
any_KRs = user_specs['knowledge_record_subkeys']['any_types']

for key, value in any_KRs.items():
    sub_plot_list = []
    print key, value
    # if type(value) is list:
    #     print value, 'in1'
    #     new_key = ('.').join([key, value[0]])
    #     print new_key
    #     plt2 = Plotter(reader, key, subkeys=[(value[0].x, 'x', value[0].y, 'y',  value[0].z, 'z')])
    #     continue
    for subkey, value in value.items():
        print subkey, value
        if 'plot' in subkey:
            sub_plot_list.append(sorted(any_KRs[key][subkey].items()))
            # sub_plot_list = value
            print sub_plot_list
            # print sub_plot_list[0]
            # print sub_plot_list[0][0]
            # if not -1 in sub_plot_list[0][0]:
            #     sub_plot_list = sorted(sub_plot_list)
            # print sorted(sub_plot_list[0])
            # print sub_plot_list.sort()
            plt6 = Plotter(reader, key, subkeys=sub_plot_list)



#plt1 = Plotter(reader, 'agent.0.location', subkeys=[((0, 'x'), (1, 'y')), ((0, 'x'), (2, 'z')),
#                                ((1, 'y'), (2, 'z')), ((-1, 'time'), (2, 'z'))], points_per_plot=50)
# plt2 = Plotter(reader, '.gams.frames.'+ knowledge_record)
# plt3 = Plotter(reader, '.gams.frames.p1_laser_stabilized', subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=10)
# plt4 = Plotter(reader, '.gams.frames', frames_of_choice=['geo','p1_base_footprint'])

# plt5 = Plotter(reader, '.sensors.px4.location.2', subkeys=[(('pose.position.x', 'x'), ('pose.position.y', 'y'))])
# plt6 = Plotter(reader, 'sensors.baro', subkeys=[((-1, 'time'), ('fluidPressure', 'pp'))])


while True:
# #   # plt1.visualize()
    plt2.visualize()
    plt3.visualize()
    plt4.visualize()
# # # #   plt5.visualize()
    plt6.visualize()
    plt7.visualize()

plt.plot.show()