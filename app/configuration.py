class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	TESTING = False
	SQLALCHEMY_DATABASE_URI = 'sqlite:///application.sqlite'
	SECRET_KEY = "TOFILL"
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	
class DebugConfig(Config):
	"""
	Configuration for debug purposes
	"""
	DEBUG = True