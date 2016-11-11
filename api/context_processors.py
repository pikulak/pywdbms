from pywdbms.db.containers import BindContainer
from pywdbms.api.blueprints import Blueprints

blueprint = Blueprints.get("blueprint")
@blueprint.context_processor
def get_table_names(shortname):
	_, meta = BindContainer.get(shortname)
	return meta.tables.keys()