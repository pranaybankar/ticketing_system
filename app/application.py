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
import traceback


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
def theaters_seats(db: Session = Depends(get_db)):
    try:
        return db.query(models.Theater).all()
    except Exception as e:
        logger.info(f"Exception:{str(e)}")
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"message":str(e)})

@app.get("/theaters/{theater_id}/seats")
def theaters_seats(theater_id: int = 1, db: Session = Depends(get_db)):
    logger.info(f"theater_id: {theater_id}, db:{db}")
    try:
        cached_seats = get_seats_cache(theater_id)
        if cached_seats:
            logger.info(f"returning from cache:{cached_seats}")
            return cached_seats
        
        theater = get_theater(db, theater_id)
        logger.info(f"application theater:{theater}")
        if not theater:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, 
                                content={"message":"Theater not found"})

        seats = get_seats(db, theater_id)
        logger.info(f"application seats:{seats}")
        set_seats_cache(theater_id, seats)
        return seats
    except Exception as e:
        logger.info(f"Exception:{str(e)}")
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"message":str(e)})
    


# @app.post("/theaters/{theater_id}/book", response_model=schemas.Seat)
@app.post("/theaters/{theater_id}/book")
def book_seat(theater_id: int, seat_number: str, db: Session = Depends(get_db)):
    try:
        seats = get_seats(db, theater_id)
        seat = next((s for s in seats if s.seat_number == seat_number), None)
        if not seat:
            raise HTTPException(status_code=404, detail="Seat not found")
        if seat.is_booked:
            return seat

        booked_seat = book_seat(db, seat.id)
        set_seats_cache(theater_id, seats)  # Update cache
        return booked_seat
    except Exception as e:
        logger.info(f"Exception:{str(e)}")
        traceback.print_exc()
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, 
                            content={"message":str(e)})

@app.post("/theaters/{theater_id}/reserve")
def reserve_seat(theater_id: int, seat_number: str, db: Session = Depends(get_db)):
    try:
        seats = get_seats(db, theater_id)
        seat = next((s for s in seats if s.seat_number == seat_number), None)
        if not seat:
            raise HTTPException(status_code=404, detail="Seat not found")
        if seat.is_booked:
            raise HTTPException(status_code=400, detail="Seat already booked")

        reserved_seat = reserve_seat(db, seat.id)
        set_seats_cache(theater_id, seats)  # Update cache

        # Set reservation to expire
        redis.setex(f"reservation:{seat.id}", RESERVATION_TIMEOUT, seat.id)
        return reserved_seat
    except Exception as e:
        logger.info(f"Exception:{str(e)}")
        traceback.print_exc()
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