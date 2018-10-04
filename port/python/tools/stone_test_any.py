import sys
import os
import capnp
from madara.knowledge import *



# Any.register_int32("i32")



# a = Any("i32")

# a.assign(10)

# print(a.to_integer())

# reader = fp.FluidPressure.new_message()
# f.fluidPressure = 30.3
# # f.header = 'pressure'
# f.variance = 0.55


def deserializer(f):
    fp = capnp.load("/home/stallone/shield_schemas/shield/FluidPressure.capnp", 
         imports=[os.environ["CAPNP_ROOT"] + "/c++/src"])
    print f.is_any_type()
    Any.register_class("FluidPressure", fp.FluidPressure)
    new_frame = Any.transform_this_to(fp)
    # fluid = f.to_any()
    
    fluid_read = Any.reader(new_frame)

    press = fluid_read.fluidPressure
    # var = fluid_read.variance

    # print press, var

    return press
