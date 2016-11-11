class Blueprints(object):
	BLUEPRINTS = {}

	@staticmethod
	def add(name, blueprint):
		_BLUEPRINTS = getattr(Blueprints, "BLUEPRINTS")
		_BLUEPRINTS[name] = blueprint
		setattr(Blueprints, "BLUEPRINTS", _BLUEPRINTS)

	@staticmethod
	def get(name):
		return getattr(Blueprints, "BLUEPRINTS")[name]