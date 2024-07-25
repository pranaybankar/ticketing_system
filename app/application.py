# import libs
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

# import dependent files
import models
import schemas
from crud import book_seat, get_seats, get_theater, reserve_seat
from cache import get_seats_cache, set_seats_cache, redis
from database import RESERVATION_TIMEOUT, databases, engine, logger, SessionLocal

# initiating app
app = FastAPI(
    title="Ticketing App",
    description="You can perform CRUD operation by using this API",
    version="1.0.0"
)

# create DB engine
models.Base.metadata.create_all(bind=engine)

# Dependency
# setup DB connection for a local session
def get_db():
    """
    Yeald the DB session when ever it is required
    """
    try:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error while getting db:{str(e)}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await databases.connect()
    # use from cache file
    redis.ping()
    yield
    # Shutdown
    await databases.disconnect()
    # use from cache file
    await redis.close()

app = FastAPI(lifespan=lifespan)

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def default_page():
    return """
    <html>
        <head>
            <title>Ticket Booking</title>
        </head>
        <body>
            <h3>Hi, Welcome to Ticket Booking application</h3>
            <p>To use the UI please <a href="http://127.0.0.1:8000/docs">click here!</a></p>
        </body>
    </html>
    """

@app.get("/theaters/{theater_id}/seats", response_model=list[schemas.Seat])
async def get_seats(theater_id: int, db: Session = Depends(get_db)):
    cached_seats = await get_seats_cache(theater_id)
    if cached_seats:
        return cached_seats

    theater = get_theater(db, theater_id)
    if not theater:
        raise HTTPException(status_code=404, detail="Theater not found")

    seats = get_seats(db, theater_id)
    await set_seats_cache(theater_id, seats)
    return seats

@app.post("/theaters/{theater_id}/book", response_model=schemas.Seat)
async def book_seat(theater_id: int, seat_number: str, db: Session = Depends(get_db)):
    seats = get_seats(db, theater_id)
    seat = next((s for s in seats if s.number == seat_number), None)
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    if seat.is_booked:
        return seat

    booked_seat = book_seat(db, seat.id)
    await set_seats_cache(theater_id, seats)  # Update cache
    return booked_seat

@app.post("/theaters/{theater_id}/reserve", response_model=schemas.Seat)
async def reserve_seat(theater_id: int, seat_number: str, db: Session = Depends(get_db)):
    seats = get_seats(db, theater_id)
    seat = next((s for s in seats if s.number == seat_number), None)
    if not seat:
        raise HTTPException(status_code=404, detail="Seat not found")
    if seat.is_booked:
        raise HTTPException(status_code=400, detail="Seat already booked")

    reserved_seat = reserve_seat(db, seat.id)
    await set_seats_cache(theater_id, seats)  # Update cache

    # Set reservation to expire
    await redis.setex(f"reservation:{seat.id}", RESERVATION_TIMEOUT, seat.id)
    return reserved_seat
