# import libs
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse

# import dependent files
import models
import schemas
from crud import (book_seat, get_seats, get_theater, reserve_seat)
from cache import (get_seats_cache, set_seats_cache, redis)
from database import (RESERVATION_TIMEOUT, engine, SessionLocal, logger)


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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/theaters")
def all_theaters(db: Session = Depends(get_db)):
    try:
        data = db.query(models.Theater).all()
        if len(data) > 0:
            return data
        else: 
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={
                "message":f"No Theaters data available."
                f" Please check Database or"
                f" The theaters.json file is available in app/data folder or not."})
    except Exception as e:
        logger.error(f"Exception:{str(e)}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"message":str(e)})

@app.get("/theaters/{theater_id}/seats")
def theaters_seats(theater_id: int = 1, db: Session = Depends(get_db)):
    try:
        cached_seats = get_seats_cache(theater_id)
        if cached_seats:
            logger.debug(f"returning from cache:{cached_seats}")
            return cached_seats
        
        theater = get_theater(db, theater_id)
        if not theater:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                                content={"message":"Theater not found"})

        seats = get_seats(db, theater_id)
        set_seats_cache(theater_id, seats)
        return seats
    except Exception as e:
        logger.error(f"Exception:{str(e)}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"message":str(e)})
    

@app.post("/theaters/{theater_id}/book")
def book_seats(theater_id: int, seat_number: str, db: Session = Depends(get_db)): 
    try:
        seats = get_seats(db, theater_id)
        seat = next((s for s in seats if s.seat_number == seat_number), None)
        if not seat:
            no_seat(seats, theater_id)
        if seat.is_booked:
            is_already_booked(seat) # idempotent operation

        booked_seat = book_seat(db, seat.id)
        logger.info(f"The seat is booked:{booked_seat}")
        set_seats_cache(theater_id, seats)  # Update cache
        return JSONResponse(status_code=status.HTTP_201_CREATED,
            content={f"message":f"The {booked_seat.seat_number} is booked in theater_id:{theater_id}."})
    except Exception as e:
        logger.error(f"Exception:{str(e)}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"message":str(e)})

@app.post("/theaters/{theater_id}/reserve")
def reserve_seats(theater_id: int, seat_number: str, db: Session = Depends(get_db)):
    try:
        already_reservation = redis.get(f"reservation:{seat_number}")
        if already_reservation:
            return JSONResponse(status_code=status.HTTP_409_CONFLICT,
            content={f"message":f"The seat:{seat_number} "
                     f"is already reserved in theater_id:{theater_id}. "
                     f"Please book it asap."})
            
        seats = get_seats(db, theater_id)
        seat = next((s for s in seats if s.seat_number == seat_number), None)
        if not seat:
            no_seat(seats, theater_id)
        if seat.is_booked:
            is_already_booked(seat) # idempotent operation

        reserved_seat = reserve_seat(db, seat.id)
        set_seats_cache(theater_id, seats)  # Update cache

        # Set reservation to expire
        redis.setex(f"reservation:{seat.seat_number}", RESERVATION_TIMEOUT, seat.id)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
            content={f"message":f"The {reserved_seat.seat_number} "
                     f"is reserved in theater_id:{theater_id}."})
    except Exception as e:
        logger.error(f"Exception:{str(e)}")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"message":str(e)})

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def default_page():
    """
        This is just a place holder route to open the swager UI
    """
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

def no_seat(seats, theater_id):
    msg = f"No seats available for booking."
    available_seats = [seat.seat_number for seat in seats if seat.is_booked is False]
    if available_seats:
        msg = (f"Wrong seat number provided. "
            f"Try these available seats:{available_seats} in theater id: {theater_id}.")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

def is_already_booked(seat, theater_id):
    msg = f"The seat:{seat.seat_number} is already booked in theater_id:{theater_id}."
    logger.debug(msg)
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
        content={f"message":msg})