import sys
import os
from flask import render_template, make_response, request, Blueprint, redirect, url_for, flash
from sqlalchemy import select
from collections import defaultdict
from sqlalchemy.exc import OperationalError

from pywdbms.db.file import load_databases_from_file as load
from pywdbms.db.file import update_databases_to_file as update
from pywdbms.db.containers import DatabaseContainer, BindContainer
from pywdbms.utils.decorators import require_database_connection
from pywdbms.utils.checks import check_connection
from pywdbms.api.forms import DatabaseAddForm, SqlForm
from pywdbms.api.settings import DEFAULT_OFFSET, SUPPORTED_DRIVERS
from pywdbms.db.statements import StatementsChooser

blueprint = Blueprint('blueprint', __name__, template_folder="../templates")
load()


@blueprint.route('/')
def dashboard():
    resp = make_response(render_template('dashboard/main.html'), 200)
    return resp

##############################
########SERVER ROUTE##########
##############################
@blueprint.route('/servers/<string:host>/')
@blueprint.route('/servers/<string:host>/info/')
def server_view_info(host):
    return make_response(render_template(
                        'server/info.html',
                        host=host), 200)


@blueprint.route('/servers/<string:host>/databases/')
def server_view_databases(host):
    sorted_by_drivers = {}
    versions = {}

    for _driver in SUPPORTED_DRIVERS:
        sorted_by_drivers[_driver] = (DatabaseContainer.get_databases(host=host,
                                                                      drivername=_driver))
    return make_response(render_template(
                        'server/databases.html',
                        sorted_by_drivers=sorted_by_drivers,
                        host=host), 200)

@blueprint.route('/servers/<string:host>/sql/')
def server_view_sql(host):
    return make_response(render_template(
                        'server/sql.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/users/')
def server_view_users(host):
    sorted_by_drivers = {}
    users = {}
    headers = {}
    _BINDS = BindContainer.get_all()

    for _driver in SUPPORTED_DRIVERS:
        sorted_by_drivers[_driver] = (DatabaseContainer.get_databases(host=host,
                                                                      drivername=_driver))
        for drivername, databases in sorted_by_drivers.items():
            for database in databases:
                for shortname, db_properties in database.items():
                    if shortname in _BINDS:
                        connection = _BINDS[shortname][0] #connection
                        stmt = StatementsChooser.for_[drivername].get_server_users()
                        result = connection.execute(stmt)
                        headers[drivername] = result.keys()
                        users[drivername] = result.fetchall()
                        break
                else:
                    continue
                break

    return make_response(render_template(
                        'server/users.html',
                        host=host,
                        headers=headers,
                        users=users), 200)

@blueprint.route('/servers/<string:host>/export/')
def server_view_export(host):
    return make_response(render_template(
                        'server/export.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/import/')
def server_view_import(host):
    return make_response(render_template(
                        'server/import.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/operations/')
def server_view_operations(host):
    return make_response(render_template(
                        'server/operations.html',
                        host=host), 200)

##############################
########DATABASE ROUTE########
##############################


@blueprint.route('/servers/<string:host>/databases/<string:shortname>/')
@blueprint.route('/servers/<string:host>/databases/<string:shortname>/structure/')
@require_database_connection
def database_view_structure(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/structure.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/sql/', methods=["POST", "GET"])
@require_database_connection
def database_view_sql(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    form = SqlForm(request.form)
    result = False
    error = False
    if request.method == 'POST':
        if form.validate():
            stmt = form.data["stmt"]
            try:
                result_ = connection.execute(stmt)
                result = {}
                result["labels"] = result_.keys()
                result["query_result"] = result_.fetchall()
            except Exception as e:
                error = e
        else:
            error = "Can't validate form."
    return make_response(render_template(
                        'database/sql.html',
                        host=host,
                        result=result,
                        form=form,
                        error=error), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/search/')
@require_database_connection
def database_view_search(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/search.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/import/')
@require_database_connection
def database_view_import(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/import.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/export/')
@require_database_connection
def database_view_export(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/export.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/operations/')
@require_database_connection
def database_view_operations(host, shortname):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'database/operations.html',
                        host=host), 200)

@blueprint.route('/databases/add/', methods=["POST", "GET"])
def database_add():
    error = False
    form = DatabaseAddForm(request.form)
    if request.method == 'POST':
        if form.validate():
            if check_connection(form.data):
                DatabaseContainer.add(form.data)
                update()
                return redirect(url_for("blueprint.dashboard"))
            else:
                error = "Unable connect to database. Maybe you provided bad data?"
        else:
            if len(form.shortname.errors) > 0:
                error = "Shortname already exists. Please specify another one."
            if len(form.database.errors) > 0:
                error = "Specifed database already exists."
            else:
                error = "Please provide correct data."
    return make_response(render_template(
                        'database/add.html',
                         form=form,
                         error=error), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/connect/')
def database_connect(host, shortname):
    try:
        BindContainer.add(shortname)
    except OperationalError:
        pass
    if request.args.get("next") != None:
        print(request.args.get("next"))
        return redirect(request.args.get("next"))
    return redirect(url_for('blueprint.database_view_structure', host=host,
                                                                shortname=shortname))

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/disconnect/')
@require_database_connection
def database_disconnect(host, shortname):
    BindContainer.delete(shortname)
    return redirect(url_for('blueprint.server_view_info', host=host))
##############################
##########TABLE ROUTE#########
##############################

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/')
@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/browse/')
@require_database_connection
def table_view_browse(host, shortname, table_name, offset=None, page=None):
    offset = request.args.get("offset")
    page = request.args.get("page")

    if offset is None:
        offset = DEFAULT_OFFSET
    else:
        try:
            offset = int(offset)
        except ValueError:
            offset = DEFAULT_OFFSET

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
@require_database_connection
def table_view_structure(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/structure.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/search/')
@require_database_connection
def table_view_search(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/search.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/add/')
@require_database_connection
def table_view_add(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/add.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/import/')
@require_database_connection
def table_view_import(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/import.html',
                        host=host), 200)

@blueprint.route('/servers/<string:host>/databases/<string:shortname>/tables/<string:table_name>/export/')
@require_database_connection
def table_view_export(host, shortname, table_name):
    connection, meta, _ = BindContainer.get(shortname)
    return make_response(render_template(
                        'table/export.html',
                        host=host), 200)


##############################
######CONTEXT PROCESSORS######
############################## 

@blueprint.context_processor
def utility_processor():
    def get_table_names(shortname):
        _temp = BindContainer.get(shortname)
        if _temp:
            # _temp[1] = meta
            return _temp[1].sorted_tables
        else:
            return []

    def to_list(input):
        return list(input)

    def to_dict(input):
        return dict(input)

    def databases(host):
        databases = list(DatabaseContainer.get_databases(host=host))
        return databases

    def strreplace(from_, what, to):
        return from_.replace(what, to)

    def generate_db_nav_items(active, url, type_):
        if type_ == "database":
            items = ["STRUCTURE", "SQL", "SEARCH", "EXPORT", "IMPORT", "OPERATIONS"]
            icons = ["columns", "magic", "search", "download", "upload", "cogs"]
        if type_ == "server":
            items = ["INFO", "DATABASES", "USERS", "EXPORT", "IMPORT", "OPERATIONS"]
            icons = ["info", "database", "user", "download", "upload", "cogs"]
        if type_ == "table":
            items = ["BROWSE", "STRUCTURE", "SEARCH", "ADD", "EXPORT", "IMPORT"]
            icons = ["table", "columns", "search", "plus", "download", "upload"]
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
    hosts = sorted(DatabaseContainer.get_uniquehosts())
    return dict(hosts=hosts)

@blueprint.context_processor
def binds():
    binds = BindContainer.get_all()
    return dict(binds=binds)

@blueprint.context_processor
def request_():
    return dict(request=request)