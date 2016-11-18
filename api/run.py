#!c:/python34/python.exe
import sys
import os
dir_ = os.path.dirname(os.path.join(os.path.realpath(__file__), "../../../"))
sys.path.insert(0, dir_)
from flask import Flask
from pywdbms.api.app import blueprint

app = Flask(__name__)
app.secret_key = 'some_secret'
app.register_blueprint(blueprint)
app.run()