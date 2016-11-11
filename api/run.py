#!c:/python34/python.exe
import sys
import os
sys.path.insert(0, 'C:\\venvs\\flask')
from flask import Flask
from pywdbms.api.app import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)