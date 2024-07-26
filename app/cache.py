"""
    Date: 25/7/2024
    Author: Pranay Bankar
    ------------------------------------------------------------------------------------------------
    Handling redis cache
    ------------------------------------------------------------------------------------------------
"""

from redis import Redis
import json
import models
from database import logger

# create redis object
redis = Redis(host="redis", port=6379, db=0, decode_responses=True)

# get cache
def get_seats_cache(theater_id: int):
    try:
        seats = redis.get(f"theater:{theater_id}:seats")
        if seats:
            list_of_objs = deserialize(seats, models.Seat)
            logger.info(f"list_of_objs:{list_of_objs}")
            return list_of_objs
        else:
            return None
    except Exception as e:
        logger.info(f"Exception: Not able to get the seats cache. {str(e)}")

def deserialize(serialised_data, class_name):
    logger.info(f"serialised_data:{serialised_data}")
    logger.info(f"class_name:{class_name}")
    return [class_name.from_dict(item) for item in json.loads(serialised_data)]


# set cache
def set_seats_cache(theater_id: int, seats):
    try:
        dict_str = serialize(seats)
        logger.info(f"dict_str:{dict_str}")
        redis.set(f"theater:{theater_id}:seats", dict_str)
    except Exception as e:
        logger.info(f"Exception: Not able to set the seats cache. {str(e)}")

# To cache the object 
def serialize(objects):
    logger.info(f"serialize:{objects}")
    return json.dumps([obj.to_dict() for obj in objects])

