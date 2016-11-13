import abc

class StatementsBaseAbstract(metaclass=abc.ABCMeta):
	@staticmethod
	@abc.abstractmethod
	def get_database_encoding(database):
		raise NotImplementedError('You must define get_server_encoding method')

	@staticmethod
	@abc.abstractmethod
	def get_server_version():
		raise NotImplementedError('You must define get_server_encoding method')

class PostgresqlStatements(StatementsBaseAbstract):

	def get_database_encoding(database):
		stmt = "SELECT pg_encoding_to_char(encoding) FROM pg_database WHERE datname='{}'".format(database)
		return stmt

	def get_server_version():
		stmt = "SELECT version()"
		return stmt

class StatementsChooser(object):
	for_ = {"postgresql+psycopg2": PostgresqlStatements}
