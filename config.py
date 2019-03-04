import os
import json

root = os.path.dirname(os.path.realpath(__file__))
with open('./config.json') as fp:
    config = json.load(fp)

DB_URL = os.environ.get('DB_URL') or config['db']['url'].format(root=root)
