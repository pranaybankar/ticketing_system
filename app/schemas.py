"""
    Date: 25/7/2024
    Author: Pranay Bankar
    ------------------------------------------------------------------------------------------------
    Define the structure of data for validation and serialization when handling API requests and responses.
    ------------------------------------------------------------------------------------------------
"""

from pydantic import BaseModel, field_validator

class SeatBase(BaseModel):
    seat_number: str
    is_booked: bool

    @field_validator('seat_number')
    def check_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Seat must be alphanumeric.')
        return v

class SeatCreate(SeatBase):
    pass

class Seat(SeatBase):
    id: int
    theater_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "seat_number": 1,
                "is_booked": False,
                "theater_id": 1
            }
        }

class TheaterBase(BaseModel):
    name: str

class TheaterCreate(TheaterBase):
    pass

class Theater(TheaterBase):
    id: int
    seats: list[Seat] = []

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Theater A",
                "seats": [
                    {"id": 1, "seat_number": "A1", "is_booked": False, "theater_id": 1},
                    {"id": 2, "seat_number": "A2", "is_booked": True, "theater_id": 1}
                ]
            }
        }
