from redis import Redis
from database import logger

# create redis object
redis = Redis(host="redis", port=6379, db=0, decode_responses=True)

logger.info(f"2222222: redis:{redis}")

# get cache
async def get_seats_cache(theater_id: int):
    seats = await redis.get(f"theater:{theater_id}:seats")
    return seats

# set cache
async def set_seats_cache(theater_id: int, seats):
    await redis.set(f"theater:{theater_id}:seats", seats)
