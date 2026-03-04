import sqlalchemy
import asyncio
import aiomysql
import pymysql
from typing import List
from typing import Optional
from sqlalchemy import Column, insert, Integer, String, Date, DateTime, Boolean, create_engine, text, ForeignKey, UniqueConstraint, Engine, select, Table, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from sqlalchemy import func, text
from datetime import timedelta

from models import engine, Base, movie_genre, Movie, User, Genre, Theatre, Ticket, Screening, Seat, Booking
import validation

import datetime
from contextlib import contextmanager


def create_session():
    with Session(engine) as session:
        with session.begin():
            try:
                yield session
            except Exception as e:
                print(e)
                raise



class DatabaseConflictError(Exception):
    pass

class DatabaseError(Exception):
    pass

class EntityNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return f"{self.message}"


def add_booking(booking: validation.BookingAdd, session, auth_id: str):
        try:
            id = get_user_by_auth_id(auth_id, session).id
            created_tickets = []
            booking_id = session.execute(insert(Booking).values(user_id=id, screening_id=booking.screening_id, total_price=100*len(booking.seats), created_at=func.now(), expires_at=func.adddate(func.now(), text("INTERVAL 5 MINUTE"))).returning(Booking.id)).scalar()
            for seat in booking.seats:
                t = Ticket(user_id=id, booking_id=booking_id, screening_id=booking.screening_id, seat_id=seat["id"], theatre_id=seat["theatre_id"])
                created_tickets.append(t)
            session.add_all(created_tickets)
            session.flush()
            return booking_id
        except IntegrityError as e:
            print("--Error--", e)
            print(e)
            raise DatabaseConflictError("Seat already booked") from e
        except SQLAlchemyError as e:
            print(e)
            raise DatabaseError("Database Insertion Failed") from e


# -- Users --
def get_user_by_id(id, session):
    try:
        result = session.get(User, id)
        return result
    except Exception as e:
        raise

def get_user_by_auth_id(auth_id, session):
    try:
        return session.execute(select(User).where(User.auth_id==auth_id)).scalar()
    except Exception as e:
        raise

def get_users_all(session):
    try:
        result = session.execute(select(User)).scalars().all()
        return result
    except Exception as e:
        raise

def search_user(query, session):
    try:
        results = session.execute(select(User).where(User.nickname.contains(query)).options(selectinload(User.bookings).selectinload(Booking.tickets), selectinload(User.bookings).selectinload(Booking.screening).selectinload(Screening.movie))).scalars().all()
        print(results)
        return results
    except Exception as e:
        raise

def delete_user(user, session):
    try:
        user_obj = session.get(User, get_user_by_auth_id(user.sub, session).id) 
        if user_obj:
            session.delete(user_obj)
        else:
            raise EntityNotFoundError(f"user with user_id:{user_obj.id} not found")
        return {"id": user.sub}
    except IntegrityError as e:
        print(e)
        raise DatabaseConflictError("Conflict occured while deleting movie.") from e
    except SQLAlchemyError as e:
        print(e)
        raise DatabaseError("Database query Failed") from e
    except Exception as e:
        print(e)
        raise

def add_user(user: validation.UserAuth, session):
    try:
        session.execute(insert(User).values(auth_id=user.sub, nickname=user.nickname, email=user.email))
        return user
    except Exception as e:
        print("--Error--", e)
        raise

# -- Theatres --
def get_theatre(id, session):
    try:
        result = session.get(Theatre, id)
        return result
    except Exception as e:
        print(e)
        raise

def get_theatres_all(session):
    try:
        result = session.execute(select(Theatre)).scalars().all()
        return result
    except Exception as e:
        print(e)
        raise

def delete_theatre(screening, session):
        try:
            theatre_obj = session.get(Theatre, screening.id)
            session.delete(theatre_obj)
        except Exception as e:
            print(e)
            raise

def add_screening(theatre: validation.ScreeningAdd, session):
    try:
        theatre_obj = Screening(**theatre.dict())
        session.add(theatre_obj)
    except Exception as e:
        print(e)
        raise


# -- Movies --
def get_movie(id, session):
    try:
        result = session.execute(select(Movie).where(Movie.id==id).options(selectinload(Movie.screenings), selectinload(Movie.genres))).scalars().first()
        return result
    except Exception as e:
        print(e)
        raise

def get_movies_all(title, genre, rating, session):
    try:
        stmt = select(Movie)        
        if title:
            stmt = stmt.where(Movie.title.contains(title))
        if rating:
            stmt = stmt.where(Movie.rating!=None).where(Movie.rating==rating)
        if genre:
            stmt = stmt.join(Movie.genres).where(Genre.id == genre)

        result = session.execute(stmt.options(selectinload(Movie.screenings).selectinload(Screening.theatre))).scalars().all()

        return result
    except Exception as e:
        print(e)
        raise

def get_movies_schedule(session):
    try:
        now = datetime.datetime.today()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        tomorrow_start = today_start + timedelta(hours=24)
        tomorrow_end = today_end + timedelta(hours=24)

        todays_screenings = session.execute(select(Screening).where(Screening.start_time >= today_start).where(Screening.start_time <= today_end).options(selectinload(Screening.movie))).scalars().all()
        todays_movies = [screening.movie for screening in todays_screenings]

        tomorrows_screenings = session.execute(select(Screening).where(Screening.start_time >= tomorrow_start).where(Screening.start_time <= tomorrow_end).options(selectinload(Screening.movie))).scalars().all()
        tomorrows_movies = [screening.movie for screening in tomorrows_screenings]
        print("\n\n\n\n\n")
        print(now)
        print(today_start)
        print(today_end)
        print(tomorrow_start)
        print(tomorrow_end)
        print(todays_movies)
        print("\n\n\n\n\n")
        return {"today": todays_movies, "tomorrow": tomorrows_movies}
    except Exception as e:
        print(e)
        raise

def get_movies_upcoming(session):
    try:
        result = session.execute(select(Movie).where(Movie.release_date > func.now())).scalars().all()
        return result
    except Exception as e:
        print(e)
        raise

def delete_movie(movie, session):
    try:
        db_movie = session.get(Movie, movie.id)
        session.delete(db_movie)
        return movie
    except IntegrityError as e:
        print("--Error--", e)
        raise DatabaseConflictError("Conflict occured while deleting movie.") from e
    except SQLAlchemyError as e:
        print(e)
        raise DatabaseError("Database query Failed") from e

def add_movie(movie, session):
    try:
        rating = None
        for country in movie['releases']['countries']:
            if country["iso_3166_1"] == "US" and country["certification"] != '':
                rating = country["certification"]
                
        movie_obj = Movie(id=movie["id"], 
                         title=movie["title"], 
                         overview=movie["overview"], 
                         runtime=movie["runtime"],
                         poster_path=movie["poster_path"], 
                         rating=rating,
                         language=movie["original_language"], 
                         release_date=movie["release_date"])
        session.add(movie_obj)
        session.flush()

        for genre in movie["genres"]:
            print("\n\n\n\n--------------", genre, "\n\n\n\n\n")
            print(genre)
            session.execute(insert(movie_genre).values(genre_id=genre["id"], movie_id=movie["id"]))
    except Exception as e:
        print(e)
        raise
    
    
    



# -- Screenings --
def get_screening(id, session):
    try:
        screening = session.execute(select(Screening).where(Screening.id==id).options(selectinload(Screening.movie), selectinload(Screening.theatre).selectinload(Theatre.seats))).scalars().first()
        screening.booked_seat_ids = session.execute(select(Ticket.seat_id).where(Ticket.screening_id==id, Ticket.status!="cancelled")).scalars().all()
        return screening
    except Exception as e:
        print(e)
        raise

def get_screenings_all(session):
    try:
        result = session.execute(select(Screening)).scalars().all()
        return result
    except Exception as e:
        print(e)
        raise

def patch_screening(screening, session):
    try:
        screening_obj = session.get(Screening, screening.id)
        if screening_obj:
            screening_obj.start_time = screening.start_time
            return "Successful update"
        else:
            raise EntityNotFoundError(f"No screening_id with id:{screening.id}")
    except IntegrityError as e:
        print("--Error--", e)
        raise DatabaseConflictError("Conflict occured while deleting movie.") from e
    except SQLAlchemyError as e:
        print(e)
        raise DatabaseError("Database query Failed") from e

def delete_screening(screening, session):
    try:
        screening_obj = session.get(Screening, screening.id)
        if screening_obj:
            session.delete(screening_obj)
        else:
            raise EntityNotFoundError(f"No screening_id with id:{screening.id}")
    except Exception as e:
        print(e)
        raise

def add_screening(screening, session):
    try:
        for time in screening.start_times:
            session.add(Screening(movie_id=screening.movie_id, start_time=time, theatre_id=screening.theatre_id))
    except Exception as e:
        print(e)
        raise
    
# -- genres --

def post_genres(genres, session):
    try: 
        print(genres)
        session.execute(insert(Genre), genres)
    except Exception as e:
        print(e)
        raise

def get_genres_all(session):
    try: 
        return session.execute(select(Genre).options(selectinload(Genre.movies)),).scalars().all()
    except Exception as e:
        print(e)
        raise

def create_theatre(id, name, per_row, rows, session):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    seats = [ {"id": alphabet[a]+str(n), "theatre_id": id} for a in range(rows) for n in range(1, per_row + 1)]

    for seat in seats:
        print(seat["id"], seat["theatre_id"])

    try: 
        print(f"inserting theatre with name: {name}, seats_per_row: {per_row}, number of rows: {rows}")
        session.execute(insert(Theatre).values(id=id, name=name, seats_per_row=per_row, number_of_rows=rows))
        session.execute(insert(Seat), seats)
    except Exception as e:
        print(e)
        raise


# seats
def get_selected_seats(id, session):
    return get_screening(id, session).booked_seat_ids

def clean_pending_bookings():
    with Session(engine) as session:
        try:
            session.execute(delete(Booking).where(Booking.expires_at <= func.now(), Booking.status=="pending"))
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError from e

# booking

def get_booking(id, session):
    try:
        booking = session.get(Booking, id, options=[selectinload(Booking.tickets)])
        if booking:
            return booking
        else:
            raise EntityNotFoundError(f"No booking with id:{id}")
    except SQLAlchemyError as e:
        raise DatabaseError from e
    except Exception as e:
        print(e)
        raise

def confirm_booking(booking_id, session):
    try:
        booking = session.get(Booking, booking_id)
        if booking:
            booking.status='complete'
        else:
            raise EntityNotFoundError(f"No booking with id:{booking_id}")
        return {"status": "successful", "booking": booking}
        
    except SQLAlchemyError as e:
        raise DatabaseError from e

def delete_booking(booking, session):
    try:
        booking_obj = session.get(Booking, booking.id)
        if booking_obj:
            for ticket in booking_obj.tickets:
                session.delete(ticket)
            session.delete(booking_obj)
        else:
            raise EntityNotFoundError(f"No booking with id:{booking.id}")
    except IntegrityError as e:
        print("--Error--", e)
        raise DatabaseConflictError("Conflict occured while deleting booking.") from e
    except SQLAlchemyError as e:
        print(e)
        raise DatabaseError("Database query Failed") from e


# tickets
def get_user_bookings(auth_id, session):
    print(auth_id)
    try:
        result = session.execute(select(Booking)
                                 .where(Booking.user_id==get_user_by_auth_id(auth_id, session).id)
                                 .options(
                                     selectinload(Booking.tickets).selectinload(Ticket.seat).selectinload(Seat.theatre), 
                                     selectinload(Booking.tickets).selectinload(Ticket.screening).selectinload(Screening.movie),
                                     selectinload(Booking.screening).selectinload(Screening.theatre) 
                                    )).scalars().all()
        print(result)
        return result
    except Exception as e:
        print(e)
        raise
    

def get_filters(session):
    try: 
        genres = session.execute(select(Genre).where(Genre.movies.any()).order_by(Genre.name)).scalars().all()
        ratings = session.execute(select(Movie.rating).where(Movie.rating != None).distinct()).scalars().all()
        print(ratings)
        print(genres)
        return {"genres": genres, "ratings": ratings}
    except Exception as e:
        print(e)
        raise



if __name__ == "__main__":

    with Session(engine) as session:

#        Ticket.__table__.drop(bind=engine, checkfirst=True)
#   Screening.__table__.drop(bind=engine, checkfirst=True)
#        Seat.__table__.drop(bind=engine, checkfirst=True)
#        Theatre.__table__.drop(bind=engine, checkfirst=True)
#        User.__table__.drop(bind=engine, checkfirst=True)
#       Movie.__table__.drop(bind=engine, checkfirst=True)
#        MovieGenre.__table__.drop(bind=engine, checkfirst=True)
##    
##

        #Genre.__table__.create(bind=engine, checkfirst=True)
        User.__table__.create(bind=engine, checkfirst=True)
        Movie.__table__.create(bind=engine, checkfirst=True)
        Theatre.__table__.create(bind=engine, checkfirst=True)
        Seat.__table__.create(bind=engine, checkfirst=True)
        Screening.__table__.create(bind=engine, checkfirst=True)
        create_theatre(2, "Salong B", 15, 5)
        Booking.__table__.create(bind=engine, checkfirst=True)
        Ticket.__table__.create(bind=engine, checkfirst=True)

        #some_user = session.get(User, 1)

        session.commit()
    
    
    
    Base.metadata.create_all(engine)


        

