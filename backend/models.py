
import sqlalchemy
import asyncio
import aiomysql
import pymysql
from typing import List
from typing import Optional
from sqlalchemy import Column, insert, Integer, String, Date, DateTime, Boolean, create_engine, text, ForeignKey, UniqueConstraint, Engine, select, Table, ForeignKeyConstraint, func, cast
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from datetime import timedelta



import validation as validation



class Base (DeclarativeBase):
    pass


movie_genre = Table("movie_genre", Base.metadata, Column("movie_id", Integer, ForeignKey("movie.id", ondelete="CASCADE"), primary_key=True), Column("genre_id", Integer, ForeignKey("genre.id"), primary_key=True))

class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    overview: Mapped[str] = mapped_column(String(1000))
    poster_path: Mapped[str] = mapped_column(String(1000))
    release_date: Mapped[str] = mapped_column(Date, default="2024-01-01")
    language: Mapped[str] = mapped_column(String(10))

    screenings: Mapped[List["Screening"]] = relationship(back_populates="movie", order_by="Screening.start_time", cascade="all, delete-orphan")

    genres: Mapped[List["Genre"]] = relationship(secondary=movie_genre, back_populates="movies")

class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    movies: Mapped[List["Movie"]] = relationship(secondary=movie_genre, back_populates="genres")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    auth_id: Mapped[str] = mapped_column(String(50))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    tickets: Mapped[List["Ticket"]] = relationship()

    __table_args__ = (UniqueConstraint("auth_id", name="unique_auth0_id"),)



class Theatre(Base):
    __tablename__ = "theatre"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    seats_per_row: Mapped[int] = mapped_column(Integer)
    number_of_rows: Mapped[int] = mapped_column(Integer)

    seats: Mapped[List["Seat"]] = relationship(back_populates="theatre",
            order_by=lambda: (
            func.substr(Seat.id, 1, 1),               # letter
            cast(func.substr(Seat.id, 2), Integer)    # number
        ))
    
class Seat(Base):
    __tablename__ = "seat"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    theatre_id: Mapped[int] = mapped_column(ForeignKey("theatre.id"), primary_key=True)

    theatre: Mapped["Theatre"] = relationship(back_populates="seats")
    

class Screening(Base):
    __tablename__ = "screening"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id", ondelete="CASCADE"))
    theatre_id: Mapped[int] = mapped_column(ForeignKey("theatre.id"))
    start_time: Mapped[str] = mapped_column(DateTime)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)
    
    movie: Mapped["Movie"] = relationship(back_populates="screenings")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="screening", cascade="all, delete-orphan")
    theatre: Mapped["Theatre"] = relationship()

    __table_args__ = (UniqueConstraint("theatre_id", "start_time", name="yes"), )
    

class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    screening_id: Mapped[int] = mapped_column(ForeignKey("screening.id", ondelete="CASCADE"))
    seat_id: Mapped[str] = mapped_column(String(10))
    theatre_id: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[str] = mapped_column(DateTime)
    expires_at: Mapped[str] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(10), default='registered')
    
    seat: Mapped[Seat] = relationship()
    screening: Mapped[Screening] = relationship(back_populates="tickets",
        )
    
    __table_args__ = (
        UniqueConstraint("screening_id", "seat_id", name="yes"), 
        ForeignKeyConstraint(
            ["seat_id", "theatre_id"], ["seat.id", "seat.theatre_id"]
        ),
        )


engine = create_engine(
"mysql+pymysql://cinema:6P3AZdYtUaWb7tBxHQa%@127.0.0.1/cinema?charset=utf8mb4",
echo = True)

