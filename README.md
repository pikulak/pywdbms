# pywdbms
Python-based Web Database Management System written in flask:
* localhost
* multiple server sessions (you can log-in as different users ; ) )
* multiple database sessions
* remember sessions

Instalation:
* go to api/run.py
 * change or delete shebang (i have to do this due to my setup)
 * python3 run.py

In progress:
* 70% back-end
* 30% front-end
* 20% security tweaks

Changelog:
* 2016-11-17
  * Manual testing (added another server for test multiple server sessions)
  * Added: disconnect/connect
  * Sidebar > now we can see if database is connected or not (by color) (https://github.com/pikulak/pywdbms/tree/master/screenshots)
  * Added: require_database_connection DECORATOR
  * Added: database add form + validation and connection checks

TODO:
* views and mechanics for all sections(server, database, table)

