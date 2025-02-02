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
def get_seats_cache(theater_id: int, class_name):
    try:
        seats = redis.get(f"theater:{theater_id}:seats")
        if seats:
            list_of_objs = deserialize(seats, class_name)
            return list_of_objs
        else:
            return None
    except Exception as e:
        logger.error(f"Exception: Not able to get the seats cache. {str(e)}")

# convert the Json formated string to class object
def deserialize(serialised_data, class_name):
    return [class_name.from_dict(item) for item in json.loads(serialised_data)]


# set cache
def set_seats_cache(theater_id: int, seats):
    try:
        dict_str = serialize(seats)
        response = redis.set(f"theater:{theater_id}:seats", dict_str)
        logger.info(f"Cache is set. Response:{response}")
    except Exception as e:
        logger.error(f"Exception: Not able to set the seats cache. {str(e)}")

# convert the class object to Json formated string
def serialize(objects):
    # we will cache only those object which are not booked
    return json.dumps([obj.to_dict() for obj in objects if obj.is_booked is False])

