from sqlalchemy.engine import url
from sqlalchemy import create_engine

def connect(db_properties):
	url = url.URL()