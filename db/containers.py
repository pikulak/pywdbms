from sqlalchemy.engine import url
from sqlalchemy.schema import MetaData
from sqlalchemy import create_engine
from pywdbms.utils.custom_dict_filter import custom_dict_filter as c_d_f
from pywdbms.db.statements import StatementsChooser

class HostsContainer(object):
    HOSTS = {}

    @staticmethod
    def add(host, port, drivername):
        _HOSTS = getattr(HostsContainer, "HOSTS")
        _HOSTS[host] = {drivername: port}
        setattr(HostsContainer, "HOSTS", _HOSTS)

    @staticmethod
    def get(value):
        try:
            return getattr(HostsContainer, "HOSTS")[value]
        except KeyError:
            return False

    @staticmethod
    def get_all():
        return getattr(HostsContainer, "HOSTS")

class DatabaseContainer(object):
    DATABASES = {}
    UNIQUE_HOSTS = []

    @staticmethod
    def get_databases(**kwargs):
        _DATABASES = getattr(DatabaseContainer, "DATABASES")
        if len(kwargs) <= 0:
            return _DATABASES
        else:
            return [{shortname: properties}
                    for shortname, properties
                     in _DATABASES.items()
                      if c_d_f(properties, kwargs) is True]

    @staticmethod
    def get_uniquehosts():
        return getattr(DatabaseContainer, "UNIQUE_HOSTS")

    @staticmethod
    def get(shortname):
        try:
            return getattr(DatabaseContainer, "DATABASES")[shortname]
        except KeyError:
            return False

    @staticmethod
    def add(properties):
        UNIQUE_HOSTS = getattr(DatabaseContainer, "UNIQUE_HOSTS")
        if properties["host"] not in UNIQUE_HOSTS:
            UNIQUE_HOSTS.append(properties["host"])
        _databases = getattr(DatabaseContainer, "DATABASES")
        _databases[properties["shortname"]] = properties
        setattr(DatabaseContainer, "DATABASES", _databases)

    @staticmethod
    def delete(shortnames=[]):
        _DATABASES = getattr(DatabaseContainer, "DATABASES")
        for shortname in shortnames:
            del _DATABASES[shortname]
        setattr(DatabaseContainer, "DATABASES", _DATABASES)

    @staticmethod
    def load_databases(databases={}):
        for _, properties in databases.items():
            properties["shortname"] = _
            DatabaseContainer.add(properties)



class BindContainer(object):
    BINDS = {}

    @staticmethod
    def get_all():
        return getattr(BindContainer, "BINDS")

    @staticmethod
    def get(shortname):
        try:
            return getattr(BindContainer, "BINDS")[shortname]
        except KeyError:
            return False

    @staticmethod
    def add(shortname):
        _db_properties = DatabaseContainer.get(shortname)
        _url = url.URL(drivername=_db_properties["drivername"],
                   username=_db_properties["username"],
                   password=_db_properties["password"],
                   host=_db_properties["host"],
                   port=_db_properties["port"],
                   database=_db_properties["database"])
        _engine = create_engine(_url, encoding="utf8")
        _connection = _engine.connect()
        _meta = MetaData()
        _meta.reflect(bind=_engine, autoload=True)
        _BINDS = getattr(BindContainer, "BINDS")
        _BINDS[shortname] = (_connection,
                             _meta, 
                             StatementsChooser.for_[_db_properties["drivername"]])
        setattr(BindContainer, "BINDS", _BINDS)

    @staticmethod
    def delete(shortnames):
        _BINDS = getattr(BindContainer, "BINDS")
        for shortname in shortnames:
            try:
                _BINDS[shortname][0].close() #connection
                del _BINDS[shortname]
            except KeyError:
                pass
        setattr(BindContainer, "BINDS", _BINDS)



