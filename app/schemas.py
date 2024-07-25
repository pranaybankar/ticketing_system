from pydantic import BaseModel

class SeatBase(BaseModel):
    number: str
    is_booked: bool

class SeatCreate(SeatBase):
    pass

class Seat(SeatBase):
    id: int
    theater_id: int

    class Config:
        orm_mode = True

class TheaterBase(BaseModel):
    name: str

class TheaterCreate(TheaterBase):
    pass

class Theater(TheaterBase):
    id: int
    seats: list[Seat] = []

    class Config:
        orm_mode = True
