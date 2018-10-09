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


def yaml_dump(filepath, user_specs):
    """ Dumps data to a yaml file """
    with open(file_path, 'w') as file_descriptor:
        yaml.dump(user_specs, file_descriptor)


if __name__ == '__main__':
    file_path = 'port/python/tools/config.yaml'
    user_specs = yaml_loader(file_path)
    print user_specs

    # items = data.get('items')
    # for item_name, item_value in items.iteritems():
    #     print item_name, item_value

# Read in the file. Checks to see if each type is present """

if user_specs['data_source']['stk_file']:
    source = user_specs['data_source']['stk_file']      # string
elif user_specs['data_source']['transport']:
    source = user_specs['data_source']['transport']    # string
else: 
    print('You have not specified a data source to read from!')
    sys.exit()

reader = DataReaderFromFile(source)

# Determine what KRs the user would like to be plotted 

if user_specs['knowledge_record']['frame_types']:
    f_type_list = user_specs['knowledge_record']['frame_types']   # list
elif user_specs['knowledge_record']['any_types']:
    a_type_list = user_specs['knowledge_record']['any_types']     # list
else: 
    print('You have not specified any knowledge records!')
    sys.exit()

# print user_specs['knowledge_record']['frame_types'][0]
knowledge_record = f_type_list[0]
print knowledge_record


keys = reader.get_keys()
#print keys

plt1 = Plotter(reader, 'agent.0.location', subkeys=[((0, 'x'), (1, 'y')), ((0, 'x'), (2, 'z')),
                                ((1, 'y'), (2, 'z')), ((-1, 'time'), (2, 'z'))], points_per_plot=50)
plt2 = Plotter(reader, 'agent.0.location')
plt3 = Plotter(reader, '.gams.frames', subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=10)
plt4 = Plotter(reader, '.gams.frames', frames_of_choice=['geo',knowledge_record])

while True:
    # plt1.visualize()
    # plt2.visualize()
    plt3.visualize()
    # plt4.visualize()
plt.plot.show()




# if not pause:




