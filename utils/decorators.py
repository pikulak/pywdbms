from flask import redirect, url_for
from pywdbms.db.containers import BindContainer
from functools import wraps


def require_database_connection(f):
	@wraps(f)
	def decorated_function(host, shortname, table_name=None):
		if BindContainer.get(shortname):
			if table_name == None:
				return f(host, shortname)
			return f(host, shortname, table_name)
		else:
			return redirect(url_for("blueprint.server_view_databases", host=host))
	return decorated_function
