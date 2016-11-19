import os
import json
import codecs
from pywdbms.db.containers import DatabaseContainer
default_dir = os.path.dirname(os.path.realpath(__file__))

def load_databases_from_file(filename='databases.json', dir=default_dir):
    with codecs.open(os.path.join(dir, filename), mode='r', encoding="utf-8") as f:
        json_str = f.read()
        DatabaseContainer.load_databases(json.loads(json_str))

def update_databases_to_file(filename='databases.json', dir=default_dir):
    with codecs.open(os.path.join(dir, filename), mode='w+', encoding="utf-8") as f:
        json_str = json.dumps(DatabaseContainer.get_databases(), indent=4, sort_keys=True)
        f.write(json_str)
