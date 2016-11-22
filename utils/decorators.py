from flask import redirect, url_for, make_response, render_template, abort
from functools import wraps
from sqlalchemy.exc import OperationalError

from pywdbms.db.containers import BindContainer, DatabaseContainer
from pywdbms.utils.checks import check_connection

def require_database_connection(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not DatabaseContainer.get(kwargs["shortname"]):
            abort(404)
        if BindContainer.get(kwargs["shortname"]):

            if not check_connection(DatabaseContainer.get(kwargs["shortname"])):
                BindContainer.delete(kwargs["shortname"])
            else:
                return f(*args, **kwargs)

        url = url_for("blueprint.database_connect", host=kwargs["host"],
                                                   shortname=kwargs["shortname"])
        return make_response(render_template("database/error.html",
                                                     host=kwargs["host"],
                                                     url=url), 200)
    return decorated_function

def require_host_or_404(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        host = kwargs["host"]
        if len(DatabaseContainer.get_databases(host=host)) <=0:
            return abort(404)
        else:
            return f(*args, **kwargs)
    return decorated_function