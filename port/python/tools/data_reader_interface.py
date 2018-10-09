import madara.knowledge as engine
import madara
import gams.pose as gp

from datetime import datetime



from time import sleep

toi_key_suffix = ".toi"
frames_prefix = '.gams.frames'

fes = gp.FrameEvalSettings()


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

  def get_reference_frame(self, key, value):
    kb.set(key, value)



class DataReaderFromFile(DataReaderInterface):
  def __init__(self, file_name):
    self.settings = engine.CheckpointSettings()
    if not file_name:
      print "cannot init data reader, file name is not valid"
    self.settings.filename = (file_name)
    self.knowledge_base = engine.KnowledgeBase()

    #retrieve all (key, value)s that can be plotted
    # since in checkpoints reader all records are returned sorted by their toi,
    # we don't need to sort our values later
    self.all_values = {}
    self.current_indexes = {}

    # this will contain all the KRs with gams frames ordered by toi
    self.gams_frames = []
    first = True
    first_toi = 0
    for key, value in engine.CheckpointReader(self.settings):
      if key and self.check_type_for_plotting(key, value):
        #gams_frames data retriveing simulation is a bit different

        if key.startswith(frames_prefix):
          self.gams_frames.append((key, value))
          if first:
            # this is the starting time
            first_toi = value.toi()
            first = False
          if not self.current_indexes.has_key(frames_prefix):
            self.current_indexes[frames_prefix] = -1
          continue

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
      return None, False

    current_index = self.current_indexes[key]

    # in case already at the end, just return last value
    if current_index == len(self.all_values[key]) - 1:
      return self.all_values[key][current_index], False

    # select the current index and point to the value
    value_to_return = self.all_values[key][current_index]
    self.current_indexes[key] += 1
    return value_to_return, True

  #TODO: fix returning only value once data plotting interface is fixed
  # now returns a pair, which consists of current value (simulates as live) for the given key
  # and a flag indicatingif the value is already the latest

  #frames_of_choice are gams frame, to know which frames_of_choice to retrieve
  def get_current_value(self, key, frames_of_choice=['geo']):
    # relative current time representing the simulation time passed from the first toi
    relative_current_time = int((datetime.utcnow() -
                                 datetime.utcfromtimestamp(0)).total_seconds()
                                * nano_size) - self.time_diff
    if key.startswith(frames_prefix):
      return self.get_gams_frame(frames_of_choice, relative_current_time)



    if not self.all_values.has_key(key):
      return None, False


    current_index = self.current_indexes[key]

    values_list = self.all_values[key]
    last_index = len(values_list) - 1

    # in case already at the end, just return last value as current
    if current_index == last_index:
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

  def get_gams_frame(self, frames_of_choice, relative_current_time):
    length = len(self.gams_frames)

    if length == 0:
      return None, False

    #last_index = -1
    index = self.current_indexes[frames_prefix] + 1
    while index < length:
      #   # most left value can require different handling
      #   # for now let's send None if no frame already with relative_current_time appears
      #   return None

      # if already at the next point
      if self.gams_frames[index][1].toi() > relative_current_time:
        break

      index += 1

    # set index back by one and break
    index -= 1

    # fill kb until last index with current simulation time
    for i in range(self.current_indexes[frames_prefix] + 1, index + 1):
      self.knowledge_base.set(self.gams_frames[i][0], self.gams_frames[i][1])

    self.current_indexes[frames_prefix] = index
    #sleep(1)
    try:
      trans_frames = gp.ReferenceFrame.load_tree(self.knowledge_base,
                                                 madara.from_pystrings(frames_of_choice),
                                                 # this value represents -1 in python
                                                 18446744073709551615, fes)
      coord = trans_frames[1].origin().transform_to(trans_frames[0])
      if index == length - 1:
        return coord, False

      return coord, True

    except:
      # if exception, return None
      return None, True



  # return true when type is something that can be plot
  # for now we consider that integer, double, and their arrays, as well as any times containig such values can be plot
  # if the key is toi then this is not a value to plot
  def check_type_for_plotting(self, key, value):
    if key.endswith(toi_key_suffix):
      return False
    #TODO: check for Any type as well
    if key.startswith(frames_prefix) or value.is_integer_type() or value.is_double_type():
      return True
    return False