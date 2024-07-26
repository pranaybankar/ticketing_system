"""
    Date: 25/7/2024
    Author: Pranay Bankar
    ------------------------------------------------------------------------------------------------
    Define the structure of database tables and how data is stored and managed in the database.
    ------------------------------------------------------------------------------------------------
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Theater(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    seats = relationship("Seat", back_populates="theater")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name            
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    seat_number = Column(String, index=True)
    is_booked = Column(Boolean, default=False)
    theater_id = Column(Integer, ForeignKey("theaters.id"))

    theater = relationship("Theater", back_populates="seats")

    def to_dict(self):
        return {
            'id': self.id,
            'seat_number': self.seat_number,            
            'is_booked': self.is_booked,
            'theater_id': self.theater_id
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
