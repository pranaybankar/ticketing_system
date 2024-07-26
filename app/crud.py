"""
    Date: 25/7/2024
    Author: Pranay Bankar
    ------------------------------------------------------------------------------------------------
    Here we are having methods for CRUD operation
    ------------------------------------------------------------------------------------------------
"""
from sqlalchemy.orm import Session
import models
import json

def get_theater(db: Session, theater_id: int):
    return db.query(models.Theater).filter(models.Theater.id == theater_id).first()

def get_seats(db: Session, theater_id: int):
    return db.query(models.Seat).filter(models.Seat.theater_id == theater_id).all()

def book_seat(db: Session, seat_id: int):
    seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if seat:
        seat.is_booked = True
        db.commit()
        db.refresh(seat)
    return seat

def reserve_seat(db: Session, seat_id: int):
    seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if seat:
        seat.is_booked = False
        db.commit()
        db.refresh(seat)
    return seat
