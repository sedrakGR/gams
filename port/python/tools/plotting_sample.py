from data_reader_interface import DataReaderFromFile
from plotting import Plotter

# put the stk file location correctly or set a new stk file and put the appropriate keys
filename = ("/media/sedrak/OS/SET/projects/"
                        "SAFE_reliability_rc_v3.4.0__pikachu-16-0004__2018-08-16-09-47-39.stk")
reader = DataReaderFromFile(filename)

keys = reader.get_keys()
#print keys

plt1 = Plotter(reader, 'agent.0.location', subkeys=[((0, 'x'), (1, 'y')), ((0, 'x'), (2, 'z')), ((1, 'y'), (2, 'z')), ((-1, 'time'), (2, 'z'))], points_per_plot=50)
plt2 = Plotter(reader, 'agent.0.location')


#TODO: points_per_plot worked for 3d, but seems to be not working for 2d/1d however values list is being updated
plt3 = Plotter(reader, '.gams.frames', subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=10)
plt4 = Plotter(reader, '.gams.frames', frames_of_choice=['geo','p1_base_link'])

while True:
    plt1.visualize()
    #plt2.visualize()
    plt3.visualize()
    #plt4.visualize()
plt.plot.show()