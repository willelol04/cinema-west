from datetime import date, datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


# -- Movie --
class MovieBase(BaseModel):
    id: int

class TheatreMovieResponse(BaseModel):
    id: int
    name: str

class ScreeningsMovieResponse(BaseModel):
    id: int
    start_time: datetime
    theatre: TheatreMovieResponse

class Movie(MovieBase):
    adult: Optional[bool] = None
    backdrop_path: Optional[str] = None
    genre_ids: Optional[list] = None
    original_language: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    release_date: Optional[date] = None
    title: Optional[str] = None
    video: Optional[bool] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None


class MovieAdmin(MovieBase):
    adult: Optional[bool] = None
    backdrop_path: Optional[str] = None
    genre_ids: Optional[list] = None
    original_language: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    release_date: Optional[date] = None
    title: Optional[str] = None
    video: Optional[bool] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None

    screenings: list[ScreeningsMovieResponse] = None
    
# -- User --
class UserBase(BaseModel):
    id: int

class UserAuth(BaseModel):
    sub: str
    nickname: str
    email: str

# -- Screening --
class ScreeningBase(BaseModel):
    id: int
    
class ScreeningPatchRequest(BaseModel):
    id: int
    start_time: datetime
    
class ScreeningPatchResponse(BaseModel):
    id: int
    start_time: datetime
    

class ScreeningAdd(BaseModel):
    movie_id: int
    theatre_id: int
    start_times: list[datetime]


# -- Theatre --
class TheatreBase(BaseModel):
    id: int

# -- Ticket --
class TicketBase(BaseModel):
    id: int



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

class ScreeningResponse(BaseModel):
    id: int
    start_time: datetime
    movie: Movie

class Theatre(TheatreBase):
    name: str

class SeatResponse(TicketBase):
    id: str
    theatre: Theatre

class TicketBooking(BaseModel):
    id: int
    seat: SeatResponse

class TicketResponse(TicketBase):
    id: int
    status: str
    booking: BookingTicketResponse
    screening: ScreeningResponse
    seat: SeatResponse

    

# -- Seat --
class SeatBase(BaseModel):
    id: int

# -- MovieGenre --
class MovieGenreBase(BaseModel):
    id: int
    

# -- Genre --
class GenreBase(BaseModel):
    id: int

class Genre(GenreBase):
    name: str

    
    
#booking 

class BookingBase(BaseModel):
    id: int
    user_id: int
    screening_id: int
    total_price: float
    status: str
    created_at: datetime
    expires_at: datetime


# payment

class PaymentRequest(BaseModel):
    booking_id: int
    username: str
    password: str
    from_account: int
    amount: float





# user

class AuthUserRemove(BaseModel):
    sub: str
    email: str