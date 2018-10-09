import gams
import gams.pose as gp
import capnp
import os

rf = gp.ReferenceFrame()
kb = engine.KnowledgeBase()
fes = gp.FrameEvalSettings()

reader = engine.CheckpointReader(settings)

prefix = '.gams.frames'
prefix1 = '.gams.frames.p1_base_footprint'
prefix2 = '.gams.frames.p1_map'
prefix3 = '.gams.frames.p1_odom'
suffix = '.origin'
suffix1 = '.toi'
suffix2 = '.parent'



# Get KRs and make into list
TOIs = []
x = []
y = []
z = []
u = []
v = []
w = []
last_timestamp = 0

frame_of_choice = 'p1_base_footprint'

for key, value in reader: 
    if key.startswith(prefix) and not key.endswith(suffix1):
        # key = key.split('.')
        # key = key[3]
        # print(key, value.to_string())
        kb.set(key, value)

        if key.endswith(suffix2):
            # kb.print_knowledge()
            try:
                trans_frames = gp.ReferenceFrame.load_tree(kb, 
                    madara.from_pystrings(['geo',frame_of_choice]) , 18446744073709551615, fes )

                if trans_frames[1].timestamp() > last_timestamp:
                    coord = trans_frames[1].origin().transform_to(trans_frames[0])
                    print(trans_frames[1].timestamp(), ": ", coord.to_string())
                    last_timestamp = trans_frames[1].timestamp()
                    sleep(0.01)
            except:
                pass



def capnp_crunch(key, value):
    print 'yes'
    schema = key_to_capnpfile[key]
    print type(schema)
    print ('/home/stallone/shield_schemas/shield/'+ schema +'.capnp')
    schema_file = capnp.load('/home/stallone/shield_schemas/shield/'+ schema +'.capnp', 
            imports=[os.environ['CAPNP_ROOT'] + '/c++/src'])
    Any.register_class(schema, schema_file.schema)
    new_value = value.to_any().reader()
    return new_value

# fp = capnp.load("/home/stallone/shield_schemas/shield/IMU.capnp", 
#     imports=[os.environ["CAPNP_ROOT"] + "/c++/src"])
reader = engine.CheckpointReader(settings)

key_to_capnpfile = {}
key_to_capnpfile = {key: value.to_any().tag() for key, value in reader if value.is_any_type()}

# print key_to_capnpfile

reader = engine.CheckpointReader(settings)

for key, value in reader: 
    if value.is_any_type():
        # print(key, value.to_string(), value.to_any().tag())
        new_value = capnp_crunch(key, value)
        # new_value = value.to_any().reader()
        print(key, new_value)