from urllib.parse import quote_plus
from sqlalchemy import Column, Integer, String, create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

parametros = (os.getenv('SQLAZURECONNSTR_AUTHSERVICES_CONN'))

url_db = quote_plus(parametros)
engine = create_engine('mssql+pyodbc:///?odbc_connect=%s' % url_db)
Session = sessionmaker(bind=engine)
Base = declarative_base()
