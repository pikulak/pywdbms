from containers import Databases
from file import load_databases_from_file as load
load()
print(Databases.databases)