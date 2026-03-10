
import sqlalchemy
import asyncio
import aiomysql
import pymysql
from typing import List
from typing import Optional
from sqlalchemy import Column, insert, Integer, String, Date, DateTime, Boolean, create_engine, text, ForeignKey, UniqueConstraint, Engine, select, Table, ForeignKeyConstraint, func, cast, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload
from datetime import timedelta, date, datetime, timezone



import validation as validation



class Base (DeclarativeBase):
    pass


movie_genre = Table("movie_genre", Base.metadata, Column("movie_id", Integer, ForeignKey("movie.id", ondelete="CASCADE"), primary_key=True), Column("genre_id", Integer, ForeignKey("genre.id"), primary_key=True))

class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    overview: Mapped[str] = mapped_column(String(1000))
    poster_path: Mapped[str] = mapped_column(String(1000), nullable=True)
    backdrop_path: Mapped[str] = mapped_column(String(1000), nullable=True)
    release_date: Mapped[date] = mapped_column(Date, nullable=True)
    runtime: Mapped[int]= mapped_column(Integer, nullable=True)
    rating: Mapped[str] = mapped_column(String(20), nullable=True)
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
    sub: Mapped[str] = mapped_column(String(50))
    nickname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    tickets: Mapped[List["Ticket"]] = relationship(cascade="all, delete-orphan")
    bookings: Mapped[List["Booking"]] = relationship(cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("sub", name="unique_auth0_id"),)



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
    start_time: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(nullable=True, onupdate=datetime.now(timezone.utc))
    
    movie: Mapped["Movie"] = relationship(back_populates="screenings")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="screening", cascade="all, delete-orphan")
    theatre: Mapped["Theatre"] = relationship()

    __table_args__ = (UniqueConstraint("theatre_id", "start_time", name="yes"), )
    

class Booking(Base):
    __tablename__ = "booking"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    screening_id: Mapped[int] = mapped_column(ForeignKey("screening.id", ondelete="CASCADE"))
    total_price: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default='pending')

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    paid_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc)+timedelta(minutes=5))
    
    tickets: Mapped[List["Ticket"]] = relationship(order_by=lambda: (
            func.substr(Ticket.seat_id, 1, 1),               # letter
            cast(func.substr(Ticket.seat_id, 2), Integer)    # number
        ), cascade="all, delete-orphan")
    screening: Mapped["Screening"] = relationship()


class Ticket(Base):
    __tablename__ = "ticket"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("booking.id", ondelete="CASCADE"))
    screening_id: Mapped[int] = mapped_column(ForeignKey("screening.id"))
    seat_id: Mapped[str] = mapped_column(String(10))
    theatre_id: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default='pending')
    
    seat: Mapped[Seat] = relationship()
    booking: Mapped[Booking] = relationship()
    screening: Mapped[Screening] = relationship(back_populates="tickets",)
    
    __table_args__ = (
        UniqueConstraint("screening_id", "seat_id", name="yes"), 
        ForeignKeyConstraint(
            ["seat_id", "theatre_id"], ["seat.id", "seat.theatre_id"]
        ),
    )


jaws_db = "mysql+pymysql://gjisbozryr4hecgb:n1md8zcrm93ersbg@rmspavs8mpub7dkq.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/ycb7addrosdwlaip"

local_db = "mysql+pymysql://cinema:6P3AZdYtUaWb7tBxHQa%@127.0.0.1/cinema?charset=utf8mb4"

engine = create_engine(jaws_db,
echo = True)
