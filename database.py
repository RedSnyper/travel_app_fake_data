import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

database_hostname = os.environ.get('DATABASE_HOSTNAME')
database_username = os.environ.get('DATABASE_USERNAME')
database_port = os.environ.get('DATABASE_PORT')
database_password = os.environ.get('DATABASE_PASSWORD')
database_name = os.environ.get('DATABASE_NAME')


SQLALCHEMY_DATABASE_URL = f'postgresql://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

