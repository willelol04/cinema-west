from __future__ import annotations
from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

# -- Genre --
class GenreBase(BaseModel):
    id: int

class Genre(GenreBase):
    name: str

# -- Theatre --
class TheatreBase(BaseModel):
    id: int

class Theatre(TheatreBase):
    name: str

# -- Screening --

class ScreeningBase(BaseModel):
    id: int

class ScreeningsMovieResponse(ScreeningBase):
    start_time: datetime
    theatre: Theatre

class ScreeningPatchRequest(ScreeningBase):
    start_time: datetime

class ScreeningAdd(BaseModel):
    movie_id: int
    theatre_id: int
    start_times: list[datetime]

class ScreeningResponse(BaseModel):
    id: int
    start_time: datetime
    movie: MovieDisplayDetailed

# -- Movie --
class MovieBase(BaseModel):
    id: int

class MovieDisplay(MovieBase):
    title: str
    poster_path: str

class MovieDisplayDetailed(MovieDisplay):
    release_date: datetime
    overview: str

class MovieDetails(MovieDisplayDetailed):
    runtime: Optional[int] = None
    genres: Optional[list[Genre]] = None
    language: Optional[str] = None
    rating: Optional[str] = None
    backdrop_path: Optional[str] = None

    screenings: list[ScreeningsMovieResponse] = None

class MovieSchedule(BaseModel):
    today: list[MovieDisplay]
    tomorrow: list[MovieDisplay]
    upcoming: list[MovieDisplayDetailed]


# -- User --
class UserBase(BaseModel):
    id: int

class UserAdd(BaseModel):
    sub: str
    nickname: str
    email: str
    is_admin: bool



# -- Ticket --
class TicketBase(BaseModel):
    id: int

class TicketResponse(TicketBase):
    status: str
    booking: BookingTicketResponse
    screening: ScreeningResponse
    seat: SeatResponse

    

# -- Seat --
class SeatBase(BaseModel):
    id: str

class SeatResponse(SeatBase):
    theatre: Theatre


# -- Booking --

class BookingBase(BaseModel):
    id: int
    user_id: int
    screening_id: int
    total_price: float
    status: str
    created_at: datetime
    expires_at: datetime

class ScreeningYesResponse(BaseModel):
    id: int
    start_time: datetime
    movie: MovieDetails
    theatre: Theatre

class BookingResponse(BaseModel):
    id: int
    user_id: int
    screening_id: int
    total_price: float
    status: str
    created_at: datetime
    expires_at: datetime
    
    tickets: list[TicketResponse]
    screening: ScreeningYesResponse

class BookingAdd(BaseModel):
    seats: list
    screening_id: int

class BookingRemove(BaseModel):
    id: int
    screening_id: int

class BookingTicketResponse(BaseModel):
    id: int
    expires_at: datetime
    status: str


# -- Payment --

class PaymentRequest(BaseModel):
    booking_id: int
    username: str
    password: str
    from_account: int
    amount: float

# -- User --

class UserRemove(BaseModel):
    sub: str

class UserAdmin(BaseModel):
    sub: str
    id: int
    nickname: str
    email: str
    bookings: list[BookingResponse]


class Filters(BaseModel):
    genres: list[Genre]
    ratings: list[str]
