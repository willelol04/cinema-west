from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


# -- Movie --
class MovieBase(BaseModel):
    id: int

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
    
# -- User --
class UserBase(BaseModel):
    id: int

class UserAuth(BaseModel):
    sub: str

# -- Screening --
class ScreeningBase(BaseModel):
    id: int

class Screening(ScreeningBase):
    movie_id: int
    theatre_id: int
    start_time: str

# -- Theatre --
class TheatreBase(BaseModel):
    id: int

# -- Ticket --
class TicketBase(BaseModel):
    id: int

class Theatre(TheatreBase):
    name: str

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

    






