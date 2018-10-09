import yaml 

def yaml_loader(filepath):
    """ Loads a yaml file """
    with open(file_path, 'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data


def yaml_dump(filepath, data):
    """ Dumps data to a yaml file """
    with open(file_path, 'w') as file_descriptor:
        yaml.dump(data, file_descriptor)






if __name__ == '__main__':
    file_path = 'port/python/tools/config.yaml'
    data = yaml_loader(file_path)
    print data

    # items = data.get('items')
    # for item_name, item_value in items.iteritems():
    #     print item_name, item_value
