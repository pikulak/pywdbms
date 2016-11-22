from pywdbms.db.containers import DatabaseContainer, BindContainer
from pywdbms.db.file import update_databases_to_file as update

def delete_server(host=""):
	databases = DatabaseContainer.get_databases(host=host)
	shortnames = [list(database.keys())[0] for database in databases]
	DatabaseContainer.delete(shortnames)
	BindContainer.delete(shortnames)
	DatabaseContainer.UNIQUE_HOSTS.remove(host)
	update()
	return True

def delete_database(shortname="", host=""):
	DatabaseContainer.delete([shortname])
	BindContainer.delete([shortname])
	if len(DatabaseContainer.get_databases(host=host)) <= 0:
		DatabaseContainer.UNIQUE_HOSTS.remove(host)
		return True
	update()
	return False