#!c:/python34/python.exe
import sys
import os
sys.path.insert(0, 'C:\\venvs\\flask')
from flask import render_template, make_response, request, Blueprint, redirect, url_for
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
    resp = make_response(render_template('dashboard/main.html'), 200)
    return resp

##############################
########SERVER ROUTE##########
##############################

@blueprint.route('/servers/<string:host>/')
@blueprint.route('/servers/<string:host>/databases/')
def server_view_databases(host):
    return make_response(render_template(
                        'server/databases.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/sql/')
def server_view_sql(host):
    return make_response(render_template(
                        'server/sql.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/users/')
def server_view_users(host):
    return make_response(render_template(
                        'server/users.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/export/')
def server_view_export(host):
    return make_response(render_template(
                        'server/export.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/import/')
def server_view_import(host):
    return make_response(render_template(
                        'server/import.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/operations/')
def server_view_operations(host):
    return make_response(render_template(
                        'server/operations.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

##############################
########DATABASE ROUTE########
##############################


@blueprint.route('/servers/<string:host>/databases/<string:shortname>/')
@blueprint.route('/servers/<string:host>/databases/<string:shortname>/structure/')
def database_view_structure(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/structure.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/sql/')
def database_view_sql(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/sql.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/search/')
def database_view_search(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/search.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/import/')
def database_view_import(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/import.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/export/')
def database_view_export(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/export.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/operations/')
def database_view_operations(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/operations.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/connect/')
def database_connect(host, shortname):
    BindContainer.add(shortname)
    return redirect(url_for('blueprint.database_view_structure', host=host, shortname=shortname))

##############################
##########TABLE ROUTE#########
##############################

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/')
@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/browse/')
def table_view_browse(host, shortname, table_name, offset=None, page=None):
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

    offset_ = (offset * page) - offset
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
                        'table/browse.html',
                        table_name=table_name,
                        keys=result.keys(),
                        rows=rows,
                        types=types,
                        current_page=page,
                        offset=offset,
                        prev=prev_,
                        next=next_,
                        host=host), 200)
 
@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/structure/')
def table_view_structure(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/structure.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/sql/')
def table_view_sql(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/sql.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/search/')
def table_view_search(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/search.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/add/')
def table_view_add(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/add.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/import/')
def table_view_import(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/import.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/export/')
def table_view_export(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/export.html',
                        binds=BindContainer.BINDS,
                        host=host), 200)


##############################
######CONTEXT PROCESSORS######
############################## 

@blueprint.context_processor
def utility_processor():
    def get_table_names(shortname):
        try:
            _, meta, _useless = BindContainer.get(shortname)
        except KeyError:
            return []
        return meta.sorted_tables

    def to_list(input):
        return list(input)

    def to_dict(input):
        return dict(input)

    def databases(host):
        databases = DatabaseContainer.get_databases(host=host)
        return databases

    def strreplace(from_, what, to):
        return from_.replace(what, to)

    def generate_db_nav_items(active, url, type_):
        if type_ == "database":
            items = ["STRUCTURE", "SQL", "SEARCH", "EXPORT", "IMPORT", "OPERATIONS"]
            icons = ["columns", "magic", "search", "download", "upload", "cogs"]
        if type_ == "server":
            items = ["DATABASES", "SQL", "USERS", "EXPORT", "IMPORT", "OPERATIONS"]
            icons = ["database", "magic", "user", "download", "upload", "cogs"]
        if type_ == "table":
            items = ["BROWSE", "STRUCTURE", "SQL", "SEARCH", "ADD", "EXPORT", "IMPORT"]
            icons = ["table", "columns", "magic", "search", "plus", "download", "upload"]
        ret = ""
        for i, item in enumerate(items):
            if item == active:
                ret += '<li class="nav-item active">'
            else:
                ret += '<li class="nav-item">'
            ret += '<a class="nav-link d_b" href="{}{}/">'.format(url, item.lower())
            ret += '<i class="fa fa-{}" aria-hidden="true"></i>'.format(icons[i])
            ret += " "
            ret += item
            ret += '</a>'
            ret += '</li>'
        return ret

    return dict(to_dict=to_dict,
                get_table_names=get_table_names,
                to_list=to_list,
                generate_db_nav_items=generate_db_nav_items,
                databases=databases,
                strreplace=strreplace)

@blueprint.context_processor
def hosts():
    hosts = DatabaseContainer.get_uniquehosts()
    return dict(hosts=hosts)

@blueprint.context_processor
def binds():
    binds = BindContainer.get_all()
    return dict(binds=binds)

@blueprint.context_processor
def request_():
    return dict(request=request)