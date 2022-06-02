import json

def manifest_to_list(manifest_path):
    with open(manifest_path, 'r') as myfile:
        data = myfile.read()
    # parse file
    obj = json.loads(data)
    return obj