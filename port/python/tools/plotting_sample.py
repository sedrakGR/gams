from plotting import Plotter
import config_parser
import matplotlib.pyplot as pltl
import sys


print sys.argv
if len(sys.argv) >= 2:
    plotters = config_parser.create_plotters_from_config(sys.argv[1])
    # Visualize the data
    while True:
        for key in plotters:
            plotters[key].visualize()
    plotters.plot.show()
else:
    print "Error! no config file specified"
