import matplotlib.pyplot as plt
import math
import data_reader_interface
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button
from datetime import datetime

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

    if subkeys:
      lenght = len(subkeys)

      rows = math.sqrt(lenght)
      self.number_of_rows = int(rows)
      self.number_of_columns = self.number_of_rows

      #try to make subplots plots in a square form grid
      # so all the subplots are visible in a better way
      # so adjust it twise if needed
      # first adjust
      if self.number_of_rows * self.number_of_columns < lenght:
        self.number_of_columns += 1
      #second adjust
      if self.number_of_rows * self.number_of_columns < lenght:
        self.number_of_rows += 1

      self.values = []

      # each subplot to have its values by index
      for i in range(0, lenght):
        # since it's 2d it has two arrays
        self.values.append(([], []))



    else: # in this case plot the given key in one subplot
      self.number_of_rows = 1
      self.number_of_columns = 1
      self.values = []
      result = self.reader.get_current_value(key, frames_of_choice)

      if isinstance(result[0], dict):
        print "for capnp types you must provide subkeys to plot"
        exit()

      # if reference frames are not provided with certain subkeys, than plot as 3d
      # or if the result is an array of 3 or more values, plot as 3d
      if self.has_frames_key or \
        (not (result[0] == None) and result[0].retrieve_index(2).exists()):
        self.plot_3d = True
        self.values.append([])
        self.values.append([])
        self.values.append([])
      else:
        # twice so
        self.values.append([])
        self.values.append([])

  def __del__(self):
    keys.remove(self.plot_name)



  # this function creates or updates the plot for the provided config of plotter
  def visualize(self):
    # pause = False
   # def onClick(event):
   #   global pause
   #   pause ^= True  

   # if not pause:
    plt.figure(self.plot_name)
    value, has_next = self.reader.get_current_value(self.name, self.frames_of_choice)
    if not value or not has_next:
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
      if self.plot_3d:
        self.visualize_3d(value)
      else:
        if self.has_frames_key:
          # shall never reach here, because we will plot in 3d by default
          return
        else:
          self.values[0].append(value.toi())
          self.values[1].append(value.to_double())

        if self.number_of_points_per_plot > 0 and len(self.values[0]) > self.number_of_points_per_plot:
          self.values[0].pop(0)
          self.values[1].pop(0)
        plt.subplot(self.number_of_rows, self.number_of_columns, 1, xlabel='toi')
        plt.plot(self.values[0], self.values[1])
       #   axpause = plt.axes([0.7, 0.05, 0.1, 0.075])
       #   bpause = Button(axpause,'Pause/Play')
        #  bpause.on_clicked(onClick)


    plt.pause(0.000000001)


  # visualizes a certain subkey
  # not to be called from outside
  def visualize_subkey(self, value, index):

   # global pause
   # pause = False

   # def onClick(event):
     # global pause
    #  pause ^= True  
       
    # print pause 
   # if not pause:
    subkey = self.subkeys[index]

    plt.subplot(self.number_of_rows, self.number_of_columns, index + 1, xlabel=subkey[0][1],
                ylabel=subkey[1][1])

    if self.is_capnp_type:
#      print value
#      print value['header']
      self.visualize_capnp_value(value, subkey, index)

    elif subkey[0][0] == -1:
      if self.has_frames_key:
        # simulate as current time
        self.values[index][0].append(datetime.now().microsecond * 1000)
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
     # axpause = plt.axes([0.7, 0.05, 0.1, 0.075])
     # bpause = Button(axpause,'Pause/Play')
     # bpause.on_clicked(onClick)

      


  # visualizes 3d plot
  # not to be called from outside
  def visualize_3d(self, value):
    if self.has_frames_key:
      self.values[0].append(value[0])
      self.values[1].append(value[1])
      self.values[2].append(value[2])
    else:
      self.values[0].append(value.retrieve_index(0).to_double())
      self.values[1].append(value.retrieve_index(1).to_double())
      self.values[2].append(value.retrieve_index(2).to_double())
    if self.number_of_points_per_plot > 0 and len(self.values[0]) > self.number_of_points_per_plot:
      self.values[0].pop(0)
      self.values[1].pop(0)
      self.values[2].pop(0)

    ax = plt.subplot(self.number_of_rows, self.number_of_columns, 1, projection='3d')
    plt.plot(self.values[0], self.values[1], self.values[2])

  # visualizing capnp is a bit different, parsing keys and setting into the
  def visualize_capnp_value(self, value, subkey, index):
    #print value
    # the second one is always a valid value
    subkey_list2 = subkey[1][0].split('.')
    if len(subkey_list2) == 0:
      # shall never happen
      return


    # get the first value from map as subvalue_2
    if subkey_list2[0].startswith('[') and subkey_list2[0].endswith(']'):
      subvalue_2 = value[int(subkey_list2[0])]
    else:
      subvalue_2 = value[subkey_list2[0]]

    for i in range(1, len(subkey_list2)):
      if subkey_list2[i].startswith('[') and subkey_list2[i].endswith(']'):
        subvalue_2 = subvalue_2[int(subkey_list2[i])]
      else:
        subvalue_2 = subvalue_2[subkey_list2[i]]

    if subkey[0][0] == -1:
      # in this case we plot against time and
      # since we don't have toi here, we plot against current time
      self.values[index][0].append(datetime.now().microsecond * 1000)
    else:
      # get the x axes value and append it to the appropriate array
      subkey_list1 = subkey[0][0].split('.')
      if subkey_list1[0].startswith('[') and subkey_list1[0].endswith(']'):
        subvalue_1 = value[int(subkey_list1[0])]
      else:
        subvalue_1 = value[subkey_list1[0]]

        for i in range(1, len(subkey_list1)):
          if subkey_list1[i].startswith('[') and subkey_list1[i].endswith(']'):
            subvalue_1 = subvalue_1[int(subkey_list1[i])]
          else:
            subvalue_1 = subvalue_1[subkey_list1[i]]

      self.values[index][0].append(subvalue_1)
    self.values[index][1].append(subvalue_2)