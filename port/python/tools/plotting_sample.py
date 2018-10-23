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
    plot1 = Plotter(reader, 'state_estimation.pose_initializer.robot_state', subkeys=[
        [('pose.pose.orientation.y', 'y'), ('pose.pose.orientation.x', 'x'), (('pose.pose.orientation.z', 'z'))]],
                    points_per_plot=100, plot_to_3d=True)
    plot11 = Plotter(reader, 'state_estimation.pose_initializer.robot_state', subkeys=[
        'pose.pose.orientation'],
                    points_per_plot=100, plot_to_3d=True)
    plot12 = Plotter(reader, 'state_estimation.pose_initializer.robot_state', subkeys=[
        'pose.pose.orientation'],
                     points_per_plot=100)
    # plot2 = Plotter(reader, 'agent.0.location', plot_to_3d=False)#, subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=100)
    # plot3 = Plotter(reader, 'agent.0.location', plot_to_3d=True)  # , subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=100)
    # plot4 = Plotter(reader, 'agent.0.location',
    #                 plot_to_3d=False, subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=100)
    # plot5 = Plotter(reader, 'agent.0.location',
    #                 plot_to_3d=True, subkeys=[((0, 'x'), (1, 'y'))], points_per_plot=100)
    # plot6 = Plotter(reader, 'agent.0.location',
    #                 plot_to_3d=True, subkeys=[[(0, 'x'), (1, 'y'), (2, 'z')]], points_per_plot=100)
    plot3 = Plotter(reader, 'sensors.bottom_laser.raw.size')#, subkeys=['magHeading'])

    while True:
        #for key in plotters:
        #    plotters[key].visualize()

        plot1.visualize()
        plot11.visualize()
        #plot12.visualize()

        # agent location with different inputs
        # plot2.visualize()
        # plot3.visualize()
        # plot4.visualize()
        # plot5.visualize()
        # plot6.visualize()

        # a single value against time
        plot3.visualize()
    plotters.plot.show()
else:
    print "Error! no config file specified"
