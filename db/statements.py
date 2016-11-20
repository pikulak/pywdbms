import abc

class StatementsBaseAbstract(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_database_encoding(database):
        raise NotImplementedError('You must define get_database_encoding method.')

    @abc.abstractmethod
    def get_server_version():
        raise NotImplementedError('You must define get_server_version method.')

    @abc.abstractmethod
    def get_server_users():
        raise NotImplementedError('You must define get_serveR_users method.')

class PostgresqlStatements(StatementsBaseAbstract):

    @staticmethod
    def get_database_encoding(database):
        stmt = "SELECT pg_encoding_to_char(encoding) FROM pg_database WHERE datname='{}';".format(database)
        return stmt

    @staticmethod
    def get_server_version():
        stmt = "SELECT version();"
        return stmt

    @staticmethod
    def get_server_users():
        stmt = "SELECT * from pg_user;"
        return stmt

class StatementsChooser(object):
    
    for_ = {"postgresql+psycopg2": PostgresqlStatements}
