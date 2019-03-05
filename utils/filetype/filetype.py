import json
import os

file_types = ['directory', 'image', 'video', 'audio', 'document', 'zip', 'other']

current_pwd = os.path.split(__file__)[0]
with open(current_pwd + os.sep + "filetype.json", 'r') as f:
    TYPE_LIST = json.loads(f.read())


def check_file_type(file_name):
    arr = file_name.split('.')
    if(len(arr) < 2):
        return "other"

    ext_name = arr[-1].lower()
    for typename in TYPE_LIST:
        if(ext_name in TYPE_LIST[typename]):
            return typename

    return "other"
