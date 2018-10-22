import config_parser
import matplotlib.pyplot as pltl
import sys


from data_reader_interface import DataReaderFromFile
from data_reader_interface import DataReaderFromKB
from data_reader_interface import KnowledgeBaseCreator
import data_reader_interface
from plotting import Plotter


if len(sys.argv) >= 2:

    #plotters = config_parser.create_plotters_from_config(sys.argv[1])
    # Visualize the data
    reader = DataReaderFromFile('/media/sedrak/OS/SET/projects/shield_schema/shield', '/media/sedrak/OS/SET/projects/SAFE_reliability_rc_v3.4.0__pikachu-16-0004__2018-08-16-09-47-39.stk')
    #plot1 = Plotter(reader, 'state_estimation.pose_initializer.robot_state', subkeys=[(('pose.pose.orientation.x', 'x'), ('pose.pose.orientation.y', 'y'))], points_per_plot=10)
    plot2 = Plotter(reader, 'agent.0.location', subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=100)

    while True:
        #for key in plotters:
        #    plotters[key].visualize()
        #plot1.visualize()
        plot2.visualize()
    plotters.plot.show()
else:
    print "Error! no config file specified"
