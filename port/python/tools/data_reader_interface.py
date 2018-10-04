import madara.knowledge as engine

from datetime import datetime



from time import sleep

toi_key_suffix = ".toi"


nano_size = 1000000000

class DataReaderInterface:

# get all keys in a list
  def get_keys(self):
    pass

  # retrieve current value from current reader
  # returns either (key, value)
  # if no appropriate value found, return None

  def get_current_value(self, key):
    pass




class DataReaderFromFile(DataReaderInterface):
  def __init__(self, file_name):
    self.settings = engine.CheckpointSettings()
    if not file_name:
      print "cannot init data reader, file name is not valid"
    self.settings.filename = (file_name)

    #retrieve all (key, value)s that can be plotted
    # since in checkpoints reader all records are returned sorted by their toi,
    # we don't need to sort our values later
    self.all_values = {}
    self.current_indexes = {}
    first = True
    for key, value in engine.CheckpointReader(self.settings):
      if key and self.check_type_for_plotting(key, value):
        if key.startswith(".gams"):
          #TODO: this requires more accurate handling
          # or making sure this is accurate
          subkeys = key.split('.')
          if (len(subkeys) > 2):
            key = ''
            for i in range(0, len(subkeys) -2):
              if subkeys[i] != '':
                key += '.'
                key += subkeys[i]
        if first:
          # this is the starting time
          first_toi = value.toi()
          first = False
        if self.all_values.has_key(key):
          self.all_values[key].append(value)
        else:
          # init the first value
          self.all_values[key] = [value]

           # set the current index which is read
        if not self.current_indexes.has_key(key):
          self.current_indexes[key] = 0

    # current time in nanoseconds from utc(0)
    #TODO: check if there's a way to retrieve time in nanoseconds instead of multiplying by nano dimension
    self.init_time = int((datetime.utcnow() - datetime.utcfromtimestamp(0)).total_seconds() * nano_size)
    self.time_diff = self.init_time - first_toi

  def get_keys(self):
    return self.all_values.keys()

  def get_next_value(self, key):
    if not self.all_values.has_key(key):
      return None

    current_index = self.current_indexes[key]

    # in case already at the end, just return last value
    if current_index == len(self.all_values[key]) - 1:
      print "reached to the end already"
      return self.all_values[key][current_index], False

    # select the current index and point to the value
    value_to_return = self.all_values[key][current_index]
    self.current_indexes[key] += 1
    return value_to_return, True

  #TODO: fix returning only value once data plotting interface is fixed
  def get_current_value(self, key):
    if not self.all_values.has_key(key):
      return None

    # relative current time representing the simulation time passed from the first toi
    relative_current_time = int((datetime.utcnow() -
                                 datetime.utcfromtimestamp(0)).total_seconds()
                                * nano_size) - self.time_diff
    current_index = self.current_indexes[key]

    values_list = self.all_values[key]
    last_index = len(values_list) - 1

    # in case already at the end, just return last value as current
    if current_index == last_index:
      #print "already reached to the last value of simulation"
      return values_list[last_index], False

    # last argument is the relative current time
    index, value  = self.find_next_value(values_list, current_index, last_index, relative_current_time)
    self.current_indexes[key] = index

    return value, True





  # get the index of the value and the value that corresponds to the simluation current time
  def find_next_value(self, values_list, first_index, last_index, relative_current_time):
    if values_list[first_index].toi() >= relative_current_time:
      return first_index, values_list[first_index]

    if values_list[last_index].toi() <= relative_current_time:
      return last_index, values_list[last_index]



    # iterate over all the elements other than last one and first one
    for current_index in range(first_index, last_index - 1):

      if values_list[current_index + 1].toi() >= relative_current_time:
        return current_index, values_list[current_index]

    #again if not found, return the last one
    return last_index, values_list[last_index]





  # return true when type is something that can be plot
  # for now we consider that integer, double, and their arrays, as well as any times containig such values can be plot
  # if the key is toi then this is not a value to plot
  def check_type_for_plotting(self, key, value):
    if key.endswith(toi_key_suffix) or not value:
      return False
    #TODO: check for Any type as well
    if value.is_integer_type() or value.is_double_type():
      return True
    return False