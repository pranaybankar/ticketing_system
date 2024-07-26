"""
    Date: 25/7/2024
    Author: Pranay Bankar
    ------------------------------------------------------------------------------------------------
    Handling database
    ------------------------------------------------------------------------------------------------
"""

from os import environ as env 
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s:      %(asctime)s : %(message)s')
logger = logging.getLogger(__name__)

# get and set environment variables so if you need to do
# any changes then that will be only in the docker-compose file.
SQLALCHEMY_DATABASE_URL = env.get("DATABASE_URL")
RESERVATION_TIMEOUT = env.get("RESERVATION_TIMEOUT")

# setup the DB realted variables
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Load JSON data into DataFrames
theaters_df = pd.read_json('data/theaters.json') 
seats_df = pd.read_json('data/seats.json')

try:
    # Bulk insert theaters data
    with engine.connect() as connection:
        theaters_df.to_sql('theaters', con=connection, if_exists='replace', index=False)
        logger.info("Theater data inserted successfully.")
except Exception as e:
    logger.info(f"Error. Theater data not inserted. Reason{str(e)}.")

try:
    # Bulk insert seats data
    with engine.connect() as connection:
        seats_df.to_sql('seats', con=connection, if_exists='replace', index=False)
        logger.info("Seat data inserted successfully.")
except Exception as e:
    logger.info(f"Error. Seat data not inserted. Reason{str(e)}.")

