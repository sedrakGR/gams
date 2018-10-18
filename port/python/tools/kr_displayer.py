from data_reader_interface import DataReaderFromFile
from data_reader_interface import DataReaderFromKB
from data_reader_interface import KnowledgeBaseCreator
from time import sleep
import madara
from madara.knowledge import Any
import madara.knowledge as engine
import capnp
import os
import yaml 
import sys

def yaml_loader(file_path):
    """ Loads a yaml file """
    with open(file_path, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def capnp_crunch(key, value):
    schema = key_to_capnpfile[key]
    schema_file = capnp.load(schemas + schema +'.capnp', 
            imports=[os.environ['CAPNP_ROOT'] + '/c++/src'])    
    Any.register_class(schema, getattr(schema_file, schema))
    new_value = value.to_any().reader()
    return new_value  

def print_dict(dictionary, ident = '', braces=1):
    """ Recursively prints nested dictionaries."""
    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print '%s%s%s%s' %(ident,braces*'[',key,braces*']') 
            print_dict(value, ident+'  ', braces+1)
        else:
            print ident+'%s = %s' %(key, value)


source_key = 'data_source'
capnp_schemas_location = 'schemas'

stk_file_source = 'stk_file'

kb_tranport_settings_key = 'transport'
kb_transport_type_key = 'transport_type'
kb_transport_hosts_key = 'hosts'
kb_name_key = 'kb_name'

queue_lenght_key = 'queue_length'
read_threads_key = 'read_threads'
thread_hertz_key = 'read_thread_hertz'

kr_key = 'knowledge_record'
subkeys_key = 'knowledge_record_subkeys'
frames_key = 'frame_types'
any_type_key = 'any_types'

valid_transports = ['UDP', 'ZMQ', 'BROADCAST', 'MULTICAST']
############################ Parse Source Configurations ############################

print sys.argv
if len(sys.argv) >= 2:
    # 1. Specify the path of the .yaml configuration file
    config_path = sys.argv[1]

    if os.path.isfile(config_path):
        user_specs = yaml_loader(config_path)
    else:
        sys.exit('\nError: Configuration file could not be loaded. Please check path')
    # print user_specs

    # 2. Grab schema file
    if user_specs[source_key][capnp_schemas_location]:
        if os.path.exists(user_specs[source_key][capnp_schemas_location]):
            schemas = user_specs[source_key][capnp_schemas_location]
        else: 
            sys.exit('\nError: You have specified an invalid schema directory.')
    else:
        sys.exit('\nError: You have not specified a schema directory.')


    # 3. Grab source from which to read data (.stk or live transport)
    # Checks to see what source is specified (For now cannot be both)
    transport_settings = user_specs[source_key][kb_tranport_settings_key]
    if user_specs[source_key][stk_file_source]:
        if os.path.isfile(user_specs[source_key][stk_file_source]):
            stk = user_specs[source_key][stk_file_source] 
            settings = engine.CheckpointSettings()
            settings.filename = stk
            reader = engine.CheckpointReader(settings)
        else: 
            sys.exit('\nError: Invalid .stk file')   
    elif transport_settings[kb_transport_type_key]:
        if transport_settings[kb_transport_type_key] in valid_transports:
            transport_type = transport_settings[kb_transport_type_key]
        else: 
            sys.exit('\nError: Invalid transport has been specified')
        #TODO: Add default hosts ports
        if transport_settings[kb_transport_hosts_key]:
            hosts = transport_settings[kb_transport_hosts_key]  
        else:
            sys.exit('\nError: No host ports have been specified')    
        if transport_settings[kb_name_key]:
            kb_name = transport_settings[kb_name_key]
        else: 
            sys.exit('\nError: No KB name has been specified')  
        queue_lenght = None
        thread_hertz = None
        read_threads = None 

        if transport_settings.has_key(queue_lenght_key):
            queue_lenght = transport_settings[queue_lenght_key]
        if transport_settings.has_key(read_threads_key):
            read_threads = transport_settings[read_threads_key]
        if transport_settings.has_key(thread_hertz_key):
            thread_hertz = transport_settings[thread_hertz_key]

        creator = KnowledgeBaseCreator(kb_name, transport_type, hosts, queue_lenght,
                            read_threads, thread_hertz)
        kb = creator.get_knowledge_base()
        reader = DataReaderFromKB(schemas, kb)

    else: 
        sys.exit('You have not specified a data source to read from.')

    # 3.1 Map capnp data types to respective capnp schema file
    # TODO: Find out how to do this for transport source
    key_to_capnpfile = {}
    key_to_capnpfile = {key: value.to_any().tag() for key, value in reader if value.is_any_type()}

    ################################ Display Knowledge Records ###############################

    # 1. Declare prefixes for filtering of knowledge records
    frame_prefix = '.gams.frames'
    any_prefix = 'sensors.camera.color_compressed'
    origin_suffix = '.origin'
    toi_suffix = '.toi'
    parent_suffix = '.parent'
    index_suffix = '.index'
    size_suffix = '.size'

    # Reader must be reset after each consumption
    reader = engine.CheckpointReader(settings)

    # 2. Create lists of available frame and Any type data
    # and display in the terminal
    any_KRs = []
    frame_KRs = []
    for key, value in reader:
        if (not key.endswith(index_suffix) and not key.endswith(size_suffix) and not
                            key.endswith(toi_suffix) and not key.endswith(parent_suffix)):
            # print key, type(value)
            if frame_prefix in key:
                key = key.split('.')
                key = key[3]
                # key = ('.').join(key[0:4])
                if key not in frame_KRs:
                    frame_KRs.append(key)
            else: 
                if key not in any_KRs:
                    any_KRs.append(key)

    any_KRs.sort()
    frame_KRs.sort()

    print ('\n---------------------------------Any Type Data-----------------------------------\n')

    if len(any_KRs) % 2 != 0:
        any_KRs.append(" ")

    split = len(any_KRs)/2
    l1 = any_KRs[0:split]
    l2 = any_KRs[split:]
    for key, value in zip(l1,l2):
        print "{0:<45s} {1}".format(key, value) 

    print ('\n---------------Frame Type Data---------------\n')

    if len(frame_KRs) % 2 != 0:
        frame_KRs.append(" ")

    split = len(frame_KRs)/2
    l1 = frame_KRs[0:split]
    l2 = frame_KRs[split:]
    for key, value in zip(l1,l2):
        print "{0:<30s} {1}".format(key, value) 

    ######################### Display Format of Desired Knowledge Records ######################

    # 1. Now that user has seen available knowledge records, parse in the desired 
    # knowledge records to view internal data format 

    # 1.1 Create lists of desired knowledge records
    if user_specs[kr_key][frames_key] and user_specs[kr_key][frames_key] != ['']:
        frame_lookup = user_specs[kr_key][frames_key]   # list
    else: 
        frame_lookup = []
    if user_specs[kr_key][any_type_key] and user_specs[kr_key][any_type_key] != ['']:
        any_lookup = user_specs[kr_key][any_type_key]     # list 
    else: 
        any_lookup = []

    # 1.2 Display internal contents of desired knowledge records
    if frame_lookup or any_lookup:
        lookup = frame_lookup + any_lookup 
        for kr in lookup:
            cnt = 0
            reader = engine.CheckpointReader(settings)
            for key, value in reader:
                if kr == key in key or kr in key:
                    if (value.is_any_type() and not key.endswith(index_suffix) 
                                and not key.endswith(size_suffix)):
                        new_value = capnp_crunch(key, value)
                        new_value = new_value.to_dict()
                        print ('\n>' + key + ' data format:\n')
                        print_dict(new_value)
                        cnt += 1
                    if (not value.is_any_type() and not key.endswith(parent_suffix) 
                                and not key.endswith(toi_suffix)):
                        key = key.split('.')
                        key = key[3] 
                        print ('\n>' + key + ' data format:\n')
                        print('     ' + value.to_string())
                        cnt += 1
                if cnt == 1:
                    break
            if cnt == 0:
                print('\nRequested key "' + kr + '" is not present in this KnowledgeBase')
                # cnt += 1
    else:    
        sys.exit('\nYou have not specified any knowledge records to view internally yet\n'
                    'Choose from above lists')





