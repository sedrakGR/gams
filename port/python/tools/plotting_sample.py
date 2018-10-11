from data_reader_interface import DataReaderFromFile
from plotting import Plotter

import time

source = ("/media/sedrak/OS/SET/projects/"
          "SAFE_reliability_rc_v3.4.0__pikachu-16-0004__2018-08-16-09-47-39.stk")

schemas_location = '/media/sedrak/OS/SET/projects/neo_code/common/shield_schema/shield/'

reader = DataReaderFromFile(schemas_location, source)

keys = reader.get_keys()

plt1 = Plotter(reader, 'agent.0.location', subkeys=[((0, 'x'), (1, 'y')), ((0, 'x'), (2, 'z')),
                                ((1, 'y'), (2, 'z')), ((-1, 'time'), (2, 'z'))], points_per_plot=10)
plt2 = Plotter(reader, 'agent.0.location')
#plt3 = Plotter(reader, '.gams.frames', subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=10)
#plt4 = Plotter(reader, '.gams.frames', frames_of_choice=['geo',knowledge_record])

#plt5 = Plotter(reader, '.sensors.px4.location.2', subkeys=[(('pose.position.x', 'x'), ('pose.position.y', 'y'))])
#plt6 = Plotter(reader, 'sensors.imu.6', subkeys=[(('angularVelocity.x', 'x'), ('angularVelocity.y', 'y'))])


while True:
  #print 'sss'
  plt1.visualize()
  #time.sleep(0.1)
  #plt2.visualize()
  #plt3.visualize()
  #plt4.visualize()
  #plt5.visualize()
  #plt6.visualize()

#plt.plot.show()