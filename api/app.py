#!c:/python34/python.exe
import sys
import os
sys.path.insert(0, 'C:\\venvs\\flask')
from flask import render_template, make_response, request, Blueprint
from pywdbms.db.file import load_databases_from_file as load
from pywdbms.db.file import update_databases_to_file as update
from pywdbms.db.containers import DatabaseContainer, BindContainer
from sqlalchemy import select


blueprint = Blueprint('blueprint', __name__, template_folder="../templates")
load()
BindContainer.add("short_db_name")

@blueprint.route('/')
def dashboard():
    resp = make_response(render_template('dashboard.html'), 200)
    return resp

@blueprint.route('/servers/<host>')
def server_view(host):
    databases = DatabaseContainer.get_databases(host=host)
    return make_response(render_template(
                        'server.html',
                        databases=databases, 
                        binds=BindContainer.BINDS), 200)

@blueprint.route('/servers/<host>/databases/<shortname>/tables/<table_name>')
def table_view(host, shortname, table_name):
    databases = DatabaseContainer.get_databases(host=host)
    connection, meta = BindContainer.get(shortname)
    table = meta.tables[table_name]
    result = connection.execute(table.select())
    return make_response(render_template(
                        'table.html',
                        databases=databases,
                        table_name=table_name,
                        keys=result.keys(),
                        rows=result.fetchall()), 200)

@blueprint.context_processor
def utility_processor():
    def get_table_names(shortname):
        _, meta = BindContainer.get(shortname)
        return meta.sorted_tables

    def to_list(input):
        return list(input)

    def to_dict(input):
        return dict(input)

    return dict(to_dict=to_dict,
                get_table_names=get_table_names,
                to_list=to_list)

@blueprint.context_processor
def hosts():
    hosts = DatabaseContainer.get_uniquehosts()
    return dict(hosts=hosts)