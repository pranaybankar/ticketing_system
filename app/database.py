
from os import environ as env 
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Databases gives you simple asyncio support for a range of databases.
from databases import Database

logger = logging.getLogger(__name__)

# get and set environment variables so if you need to do
# any changes then that will be only in the docker-compose file.
SQLALCHEMY_DATABASE_URL = env.get("DATABASE_URL")
RESERVATION_TIMEOUT = env.get("RESERVATION_TIMEOUT")

logger.info(f"11111111: SQLALCHEMY_DATABASE_URL:{SQLALCHEMY_DATABASE_URL}")
logger.info(f"11111111: RESERVATION_TIMEOUT:{RESERVATION_TIMEOUT}")

# setup the DB realted variables
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
databases = Database(SQLALCHEMY_DATABASE_URL)


