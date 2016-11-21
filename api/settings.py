from pywdbms.api.operations import delete_server

SUPPORTED_DRIVERS = ['postgresql+psycopg2']
DEFAULT_OFFSET = 25
COMMANDS = {
	"delete_server" : delete_server}