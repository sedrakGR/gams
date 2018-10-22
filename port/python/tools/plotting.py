import matplotlib.pyplot as plt
import math
import data_reader_interface
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button
from datetime import datetime
import numbers

keys = []

class Plotter:
  #reader is the reader interface to be used to read data from stk file or kb

  # for subkeys we expect an array of mappings each value to another (this is for 2d maps)
  # if we want to set mapping to time, just setting the second index to -1
  # e.g. subkeys = []
  # subkeys.append(((0, 'x'), (1, 'y')))
  # subkeys.append(((2, 'z'), (-1, 'time')))
  # we expect second value always be a real index for subkeys
  # however first can be -1 so it can be plot against time

  # and pass this to the constructor
  # each value has a name to be shown as its axis name


  # frames_of_choice parameter is for gams frames only
  # it identifies the frames to load the tree, has a default value

  # points_per_plot indentifies the number of points to keep for plotting,
  # if 0, then no limit, it will keep all the retrieved polints

  def __init__(self, reader, key, subkeys = None, points_per_plot = 0, frames_of_choice=['geo', 'p1_base_stabilized']):
    if not reader or not key:
      print "Plotter is not constructed properly"
      return

    self.has_frames_key = False
    self.is_capnp_type = None
    print reader.get_keys()
    if key.startswith(data_reader_interface.frames_prefix):
      self.has_frames_key = True

    self.reader = reader
    self.name = key
    self.frames_of_choice=frames_of_choice

    self.plot_name = key
    # adjust key if reusing, to avoid plot collisions
    if key in keys:
      #this might be not a good solution, but at least we will skip collisions
      self.plot_name += ' ' * len(keys)
    keys.append(self.plot_name)

    self.subkeys = subkeys
    self.plot_3d = False
    self.number_of_points_per_plot = points_per_plot

    self.values = {}
    if subkeys:
      self.adjust_rows_and_columns(len(subkeys))

    else: # in this case plot the given key in one subplot
      self.number_of_rows = 1
      self.number_of_columns = 1

  def __del__(self):
    keys.remove(self.plot_name)



  # this function creates or updates the plot for the provided config of plotter
  def visualize(self):
    fig = plt.figure(self.plot_name)
    plt.clf()
    value, has_next = self.reader.get_current_value(self.name, self.frames_of_choice)
    if (value == None) or not has_next:
      return

    if self.is_capnp_type == None:
      self.is_capnp_type = isinstance(value, dict)


    if self.has_frames_key:
      new_values = [float(i) for i in value.to_string().split(',')]
      value = new_values

    if self.subkeys:
      for i in range(0, len(self.subkeys)):
        self.visualize_subkey(value, i)
    else:
      self.visualize_key(value, self.name)

    plt.pause(0.000000001)


  # visualizes a certain subkey
  # not to be called from outside
  def visualize_subkey(self, value, index):

    subkey = self.subkeys[index]

    # plot all of values inside subkey

    if self.is_capnp_type:
      self.visualize_capnp_value(value, subkey, index)
      return

    plt.subplot(self.number_of_rows, self.number_of_columns, index + 1, xlabel=subkey[0][1],
                  ylabel=subkey[1][1])

    # if the object is not capnp type it is not expected to be a dictionary

    if not (self.values.has_key(index)):
      self.values[index] = ([], [])

    if subkey[0][0] == -1:
      if self.has_frames_key:
        # simulate as current time
        current_time = int(
          (datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * data_reader_interface.nano_size)
        self.values[index][0].append(current_time)
        self.values[index][1].append(value[subkey[1][0]])
      else:
        self.values[index][0].append(value.toi())
        self.values[index][1].append(value.retrieve_index(subkey[1][0]).to_double())

    else:
      if self.has_frames_key:
        self.values[index][0].append(value[subkey[0][0]])
        self.values[index][1].append(value[subkey[1][0]])
      else:
        # self.values[index][0] and self.values[index][1] represent our x and y axes values
        # index for the x axes value in KR is the [0][0]
        self.values[index][0].append(value.retrieve_index(subkey[0][0]).to_double())
        # index for the y axes value in KR is [1][0]
        self.values[index][1].append(value.retrieve_index(subkey[1][0]).to_double())

    if self.number_of_points_per_plot > 0 and len(self.values[index][0]) > self.number_of_points_per_plot:
        self.values[index][0].pop(0)
        self.values[index][1].pop(0)
    plt.plot(self.values[index][0], self.values[index][1])



  # visualizing capnp is a bit different, parsing keys and setting into the
  def visualize_capnp_value(self, value, subkey, index):
    # the second one is always a valid value
    print subkey
    if not isinstance(subkey, tuple):
      subvalue = self.get_value_for_key(subkey, value)
      # in this case we expect only one subkey, so we visualize that
      self.visualize_key(subvalue, subkey[0])
      return

    subvalue_2 = self.get_value_for_key(subkey[1][0], value)

    #init values lists to be plotted
    if not (self.values.has_key(index)):
      self.values[index] = ([], [])

    if subkey[0][0] == -1:
      # in this case we plot against time and
      # since we don't have toi here, we plot against current time
      current_time = int(
        (datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * data_reader_interface.nano_size)

      self.values[index][0].append(current_time)
    else:
      # get the x axes value and append it to the appropriate array
      subvalue_1 = self.get_value_for_key(subkey[0][0], value)
      self.values[index][0].append(subvalue_1)
    self.values[index][1].append(subvalue_2)
    plt.subplot(self.number_of_rows, self.number_of_columns, index + 1, xlabel=subkey[0][1],
                ylabel=subkey[1][1])
    plt.plot(self.values[index][0], self.values[index][1])




  # visualizes a single key with no subkeys provided
  def visualize_key(self, value, key):
    if not (self.values.has_key(key)):
      self.values[key] = {}

    current_time = int(
      (datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * data_reader_interface.nano_size)
    # if dictionary (can happen for capnp types)
    if isinstance(value, dict):

      if (len(self.values[key]) == 0):
        self.adjust_rows_and_columns(len(value.keys()))
      else:
        self.adjust_rows_and_columns(len(self.values[key]))
      index = 1
      for curr_subkey in value.keys():
        curr_value = value[curr_subkey]

        # plot only number types
        if isinstance(curr_value, numbers.Number):
          if not (self.values[key].has_key(curr_subkey)):
            self.values[key][curr_subkey] = ([], [])
          self.values[key][curr_subkey][0].append(current_time)
          self.values[key][curr_subkey][1].append(curr_value)

          if self.number_of_points_per_plot > 0 and len( self.values[key][curr_subkey][0]) > self.number_of_points_per_plot:
            self.values[key][curr_subkey][0].pop(0)
            self.values[key][curr_subkey][1].pop(0)
          plt.subplot(self.number_of_rows, self.number_of_columns, index, xlabel='time', ylabel=curr_subkey)

          plt.plot(self.values[key][curr_subkey][0], self.values[key][curr_subkey][1])
          index += 1

    #if a list type
    elif isinstance(value, list):
      lenght = len(value)
      self.adjust_rows_and_columns(lenght)
      for i in range(0, lenght):
        if not (self.values[key].has_key(i)):
          self.values[key][i] = ([], [])
        y_label = (key + '.' + str(i))
        plt.subplot(self.number_of_rows, self.number_of_columns, i + 1, xlabel='time', ylabel=y_label)
        self.values[key][i][1].append(value[i])
        self.values[key][i][0].append(current_time)

        # remove additional values
        if self.number_of_points_per_plot > 0 and len( self.values[key][i][0]) > self.number_of_points_per_plot:
          self.values[key][i][0].pop(0)
          self.values[key][i][1].pop(0)

        plt.plot(self.values[key][i][0], self.values[key][i][1])
    # value is KR, check if array type
    # similar to above one, but rather need to read value in a bit different way
    elif value.is_array_type():
      # try to plot all the values of the array against time
      size = value.size()
      self.adjust_rows_and_columns(size)
      for i in range(0, size):
        if not (self.values[key].has_key(i)):
          self.values[key][i] = ([], [])
        y_label = (key + '.' + str(i))
        plt.subplot(self.number_of_rows, self.number_of_columns, i + 1, xlabel='time', ylabel=y_label)
        self.values[key][i][1].append(value.retrieve_index(i).to_double())
        self.values[key][i][0].append(value.toi())

        # remove additional values
        if self.number_of_points_per_plot > 0 and len( self.values[key][i][0]) > self.number_of_points_per_plot:
          self.values[key][i][0].pop(0)
          self.values[key][i][1].pop(0)

        plt.plot(self.values[key][i][0], self.values[key][i][1])


    else:
      # it should be a number type
      plt.subplot(self.number_of_rows, self.number_of_columns, 1, ylabel=key, xlabel='time')
      if not (self.values[key].has_key(key)):
        # looks redundant having same key in key, but this lets to keep the structure a bit more generic
        self.values[key][key] = ([], [])


      self.values[key][key][1].append(value.to_double())
      self.values[key][key][0].append(value.toi())

      if self.number_of_points_per_plot > 0 and len(self.values[key][key][0]) > self.number_of_points_per_plot:
        self.values[key][key][0].pop(0)
        self.values[key][key][1].pop(0)




  # adjust number of rows and columns according to the subplots lenght
  def adjust_rows_and_columns(self, lenght):

    rows = math.sqrt(lenght)
    self.number_of_rows = int(rows)
    self.number_of_columns = self.number_of_rows

    # try to make subplots plots in a square form grid
    # so all the subplots are visible in a better way
    # so adjust it twise if needed
    # first adjust
    if self.number_of_rows * self.number_of_columns < lenght:
      self.number_of_columns += 1
    # second adjust
    if self.number_of_rows * self.number_of_columns < lenght:
      self.number_of_rows += 1


  # for a capnp type objects parse the key and retrieve the value
  def get_value_for_key(self, key, value):
    # for dictionaries subkeys can be represented as
    # 'key1.[index1].key2.key3' it can has keys inside keys and indexes bounded by `[]`
    subkeys = key.split('.')
    if len(subkeys) == 0:
      # shall never happen
      return None

    # get the first value from map as subvalue_2
    if subkeys[0].startswith('[') and subkeys[0].endswith(']'):
      subvalue = value[int(subkeys[0][1:-1])]
    else:
      subvalue = value[subkeys[0]]

    for i in range(1, len(subkeys)):
      if subkeys[i].startswith('[') and subkeys[i].endswith(']'):
        subvalue = subvalue[int(subkeys[i][1:-1])]
      else:
        subvalue = subvalue[subkeys[i]]

    return subvalue