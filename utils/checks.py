from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.exc import OperationalError

def check_connection(db_properties):
    _url = url.URL(drivername=db_properties["drivername"],
                   username=db_properties["username"],
                   password=db_properties["password"],
                   host=db_properties["host"],
                   port=db_properties["port"],
                   database=db_properties["database"])
    try:
      create_engine(_url, encoding="utf8")
      return True
    except OperationalError:
      return False