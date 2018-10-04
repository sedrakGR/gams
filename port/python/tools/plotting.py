import matplotlib.pyplot as plt
import math
import data_reader_interface
from mpl_toolkits.mplot3d import Axes3D



cnt = 1
pause = False

class Plotter:
  def __init__(self, reader):
    #TODO: maybe add some better naming for plot.figure, e.g. retrieve in constructor
    if not reader:
      return
    self.plot = plt

    # init empty keys
    self.keys_to_values = {}
    self.reader = reader

  def init(self):
    fig = self.plot.figure(str(self))

    # TODO: handle initialization of type and labels here based on the type
    index = 1
    self.axes = {}
    self.plot_indexes = {}

    # length of keys to be plotted
    lenght = len(self.keys_to_values)
    if lenght <= 2:
      self.number_of_rows = 1
      self.number_of_columns = lenght
    elif lenght < 7:
      self.number_of_rows = 2
      self.number_of_columns = (lenght + 1)/ 2
    else:
      self.number_of_rows = 3
      self.number_of_columns = (lenght + 2)/ 3
    for key in self.keys_to_values.keys():
      #ax2 = fig.add_subplot(2, (len(self.keys_to_values) + 1)/ 2, index)
      if self.reader.get_current_value(key)[0].retrieve_index(2).exists():
        ax = fig.add_subplot(self.number_of_rows, self.number_of_columns, index, projection='3d')
        ax.set_title(key)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        self.plot.pause(0.00001)

      elif self.reader.get_current_value(key)[0].retrieve_index(1).exists():
        ax = fig.add_subplot(self.number_of_rows, self.number_of_columns, index)
        ax.set_title(key)
        ax.set_xlabel('x')
        ax.set_ylabel('y')

      else:
        ax = fig.add_subplot(self.number_of_rows, self.number_of_columns, index)
        ax.set_title(key)
        ax.set_xlabel("time")
        ax.set_ylabel(key)
      #self.axes[key] = ax
      self.plot_indexes[key] = index
      index += 1

  def set_key_to_plot(self, key):
    # not keeping keys until it has the reader of data
    if not self.reader:
      return

    # init key for the first time, so that it can identify how to plot
    if not key in self.keys_to_values:
      self.keys_to_values[key] = None


  def visualize(self):
    self.plot.figure(str(self))
    for key in self.keys_to_values:
      value, has_next = self.reader.get_current_value(key)
      if not value:
        continue
      first = False
      if not self.keys_to_values[key]:
        first = True
      if self.reader.get_current_value(key)[0].retrieve_index(2).exists():
      #TODO: the correct checking is possibly checking is_array_type
      # if value.is_array_type():
      #
      #   #TODO: don't know how this can be plotted for now, revisit this
        #
        if self.reader.get_current_value(key)[0].retrieve_index(2).exists():
          if first:
            self.keys_to_values[key] = [[value.retrieve_index(0).to_double()],
                              [value.retrieve_index(1).to_double()],
                              [value.retrieve_index(2).to_double()]]
          else:
            self.keys_to_values[key][0].append(value.retrieve_index(0).to_double())
            self.keys_to_values[key][1].append(value.retrieve_index(1).to_double())
            self.keys_to_values[key][2].append(value.retrieve_index(2).to_double())


          #self.plot.subplots()[key]
          ax = self.plot.subplot(self.number_of_rows, self.number_of_columns, self.plot_indexes[key], projection='3d')
          ax.set_title(key)
          ax.set_xlabel('x')
          ax.set_ylabel('y')
          ax.set_zlabel('z')
          self.plot.plot(self.keys_to_values[key][0], self.keys_to_values[key][1], self.keys_to_values[key][2])
      elif self.reader.get_current_value(key)[0].retrieve_index(1).exists():
        if first:
          self.keys_to_values[key] = [[value.retrieve_index[0].to_double()], [value.retrieve_index[1].to_double()]]
        else:
          self.keys_to_values[key][0].append(value.retrieve_index[0].to_double())
          self.keys_to_values[key][1].append(value.retrieve_index[1].to_double())

        self.plot.subplot(self.number_of_rows, self.number_of_columns, self.plot_indexes[key])
        self.plot.plot(self.keys_to_values[key][0], self.keys_to_values[key][1])
      #TODO: plot ANY type
      # elif anytype
      else:
        if first:
          self.keys_to_values[key] = [value.to_double()]
        else:
          self.keys_to_values[key].append(value.to_double())
        self.plot.subplot(self.number_of_rows, self.number_of_columns, self.plot_indexes[key])
        self.plot.plot(self.keys_to_values[key])

    self.plot.pause(0.00001)