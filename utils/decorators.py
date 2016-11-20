from flask import redirect, url_for, make_response, render_template
from functools import wraps
from sqlalchemy.exc import OperationalError

from pywdbms.db.containers import BindContainer, DatabaseContainer
from pywdbms.utils.checks import check_connection

def require_database_connection(f):
    @wraps(f)
    def decorated_function(host, shortname, table_name=None, section=None):
        if BindContainer.get(shortname):

            if not check_connection(DatabaseContainer.get(shortname)):
                BindContainer.delete(shortname)
            else:
                if table_name == None:
                    return f(host, shortname)
                return f(host, shortname, table_name)

        url = url_for("blueprint.database_connect", host=host, shortname=shortname)
        return make_response(render_template("database/error.html",
                                                     host=host,
                                                     url=url), 200)
    return decorated_function
