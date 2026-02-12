from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class MovieBase(BaseModel):
    id: Optional[int] = None

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

class UserCreate(BaseModel):
    f_name: str
    l_name: str
    email: str
    password: str

class UserResponse(BaseModel):
    f_name: str
    l_name: str
    email: str
    
class Screening(BaseModel):
    movie_id: int
    theatre_id: int
    start_time: str


class Theatre(BaseModel):
    id: int
    name: str

class Genre(BaseModel):
    id: int
    name: str

class authUser(BaseModel):
    sub: str
    email: str

