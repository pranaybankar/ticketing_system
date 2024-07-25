from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Theater(Base):
    __tablename__ = "theaters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    seats = relationship("Seat", back_populates="theater")

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, index=True)
    is_booked = Column(Boolean, default=False)
    theater_id = Column(Integer, ForeignKey("theaters.id"))

    theater = relationship("Theater", back_populates="seats")
