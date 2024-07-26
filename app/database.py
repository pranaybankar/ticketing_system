"""
    Date: 25/7/2024
    Author: Pranay Bankar
    ------------------------------------------------------------------------------------------------
    Handling database
    ------------------------------------------------------------------------------------------------
"""

from os import environ as env 
import logging
import os.path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
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

# save theater data to sqlite db
def save_to_db(file):
    name = "theaters"
    if "seats" in file:
        name = "seats"
    try:
        if os.path.isfile(file):
            # create a data frame
            _df = pd.read_json(file)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"The {name}.json file is not available in app/data folder.")             
    except Exception as e:
        logger.error(f"Exception:{str(e)}")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
            content={
            "message":str(e)
            })

    try:
        # Bulk insert data
        with engine.connect() as connection:
            # save data from dataframe
            _df.to_sql(name, con=connection, if_exists='replace', index=False)
            logger.info(f"The {name} data inserted successfully.")
    except Exception as e:
        msg = f"Error. {name} data not inserted. Reason{str(e)}."
        logger.error(msg)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            content={
            "message":str(msg)
            })

save_to_db('data/theaters.json')
save_to_db('data/seats.json')
