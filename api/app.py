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
default_offset = 25
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

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/')
def table_view(host, shortname, table_name, offset=None, page=None):
    offset = request.args.get("offset")
    page = request.args.get("page")

    if offset is None:
        offset = default_offset
    else:
        try:
            offset = int(offset)
        except ValueError:
            offset = default_offset

    if page is None:
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            page = 1
            
    if page <= 0:
        page = 1
    if page -1 <= 0:
        prev_ = False
    else:
        prev_ = page - 1

    table_url = "/servers/{}/databases/{}/tables/{}".format(host, shortname, table_name)
    offset_ = (offset * page) - offset
    databases = DatabaseContainer.get_databases(host=host)
    connection, meta, _ = BindContainer.get(shortname)
    table = meta.tables[table_name]
    result = connection.execute(table.select().limit(offset).offset(offset_))
    rows = result.fetchall()
    types = [col.type for col in result.context.compiled.statement.columns]

    if len(rows) < offset:
        next_ = False
    else:
        next_ = page + 1

    return make_response(render_template(
                        'table.html',
                        databases=databases,
                        table_name=table_name,
                        keys=result.keys(),
                        rows=rows,
                        types=types,
                        current_page=page,
                        table_url=table_url,
                        offset=offset,
                        prev=prev_,
                        next=next_), 200)
 

"""CONTEXT PROCESSORS"""   

@blueprint.context_processor
def utility_processor():
    def get_table_names(shortname):
        _, meta, _useless = BindContainer.get(shortname)
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