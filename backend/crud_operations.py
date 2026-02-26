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
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, NoResultFound
from sqlalchemy import func, text
from datetime import timedelta

from models import engine, Base, movie_genre, Movie, User, Genre, Theatre, Ticket, Screening, Seat, Booking
import validation

import datetime

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


def add_booking(booking: validation.BookingAdd, auth_id: str):
    print("--------------------------------")
    print(booking, auth_id)
    print("--------------------------------")
    with Session(engine) as session:
        try:
            id = get_user_by_auth_id(auth_id).id
            created_tickets = []
            booking_id = session.execute(insert(Booking).values(user_id=id, screening_id=booking.screening_id, total_price=100*len(booking.seats), created_at=func.now(), expires_at=func.adddate(func.now(), text("INTERVAL 5 MINUTE"))).returning(Booking.id)).scalar()
            for seat in booking.seats:
                print("--------------------------------")
                print(seat)
                print("--------------------------------")
                #stmt = (insert(Ticket).values(user_id=id, screening_id=ticket.screening_id, created_at=func.now(), expires_at=func.adddate(func.now(), text("INTERVAL 5 MINUTE")), seat_id=seat["id"], theatre_id=seat["theatre_id"])).returning(Ticket)
                t = Ticket(user_id=id, booking_id=booking_id, screening_id=booking.screening_id, seat_id=seat["id"], theatre_id=seat["theatre_id"])
                created_tickets.append(t)
            session.add_all(created_tickets)
            session.flush()
            session.commit()
            return booking_id
        except IntegrityError as e:
            print("--Error--", e)
            session.rollback()
            print(e)
            raise DatabaseConflictError("Seat already booked") from e
        except SQLAlchemyError as e:
            session.rollback()
            print(e)
            raise DatabaseError("Database Insertion Failed") from e


# -- Users --
def get_user_by_id(id):
    with Session(engine) as session:
        try:
            result = session.get(User, id)
            return result
        except Exception as e:
            print("--Error--", e)
            session.rollback()

def get_user_by_auth_id(auth_id):
    with Session(engine) as session:
        try:
            return session.execute(select(User).where(User.auth_id==auth_id)).scalar()
        except Exception as e:
            print("--Error--", e)
            session.rollback()

def get_users_all():
    with Session(engine) as session:
        try:
            result = session.execute(select(User)).scalar()
            return result
        except Exception as e:
            print("--Error--", e)
            session.rollback()

def delete_user(user):
    with Session(engine) as session:
        try:
            user_obj = session.get(User, get_user_by_auth_id(user.sub).id) 
            if user_obj:
                session.delete(user_obj)
                session.commit()
            else:
                raise EntityNotFoundError(f"user with user_id:{user_obj.id} not found")
            return {"id": user.sub}
        except IntegrityError as e:
            print("--Error--", e)
            session.rollback()
            print(e)
            raise DatabaseConflictError("Conflict occured while deleting movie.") from e
        except SQLAlchemyError as e:
            session.rollback()
            print(e)
            raise DatabaseError("Database query Failed") from e
        except Exception as e:
            print("--Error--", e)
            session.rollback()

def add_user(user: validation.UserAuth):
    with Session(engine) as session:
        try:
            session.execute(insert(User).values(auth_id=user.sub, nickname=user.nickname, email=user.email))
            session.commit()
            return user
        except Exception as e:
            print("--Error--", e)
            session.rollback()

# -- Theatres --
def get_theatre(id):
    with Session(engine) as session:
        try:
            result = session.get(Theatre, id)
            return result
        except Exception as e:
            print(e)

def get_theatres_all():
    with Session(engine) as session:
        try:
            result = session.execute(select(Theatre)).scalars().all()
            return result
        except Exception as e:
            print(e)

def delete_theatre(screening):
    with Session(engine) as session:
        try:
            theatre_obj = session.get(Theatre, screening.id)
            session.delete(theatre_obj)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

def add_screening(theatre: validation.ScreeningAdd):
    with Session(engine) as session:
        try:
            theatre_obj = Screening(**theatre.dict())
            session.add(theatre_obj)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()


# -- Movies --
def get_movie(id):
    with Session(engine) as session:
        try:
            result = session.execute(select(Movie).where(Movie.id==id).options(selectinload(Movie.screenings), selectinload(Movie.genres))).scalars().first()
            return result
        except Exception as e:
            print(e)

def get_movies_all():
    with Session(engine) as session:
        try:
            result = session.execute(select(Movie).options(selectinload(Movie.screenings).selectinload(Screening.theatre))).scalars().all()
            return result
        except Exception as e:
            print(e)

def get_movies_upcoming():
    with Session(engine) as session:
        try:
            result = session.execute(select(Movie).where(Movie.release_date > func.now())).scalars().all()
            return result
        except Exception as e:
            print(e)

def delete_movie(movie):
    with Session(engine) as session:
        try:
            db_movie = session.get(Movie, movie.id)
            session.delete(db_movie)
            session.commit()
            return movie
        except IntegrityError as e:
            print("--Error--", e)
            session.rollback()
            print(e)
            raise DatabaseConflictError("Conflict occured while deleting movie.") from e
        except SQLAlchemyError as e:
            session.rollback()
            print(e)
            raise DatabaseError("Database query Failed") from e
def add_movie(movie):
    print(movie)
    with Session(engine) as session:
        try:
            movie_obj = Movie(id=movie.id, 
                             title=movie.title, 
                             overview=movie.overview, 
                             poster_path=movie.poster_path, 
                             language=movie.original_language, 
                             release_date=movie.release_date)
            session.add(movie_obj)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
    
    if movie.genre_ids:
        with engine.connect() as conn:
            try:
                for g_id in movie.genre_ids:
                    conn.execute(insert(movie_genre).values(genre_id=g_id, movie_id=movie.id))
                conn.commit()
            except Exception as e:
                print(e)
                conn.rollback()
    



# -- Screenings --
def get_screening(id):
    with Session(engine) as session:
        try:
            screening = session.execute(select(Screening).where(Screening.id==id).options(selectinload(Screening.movie), selectinload(Screening.theatre).selectinload(Theatre.seats))).scalars().first()
            screening.booked_seat_ids = session.execute(select(Ticket.seat_id).where(Ticket.screening_id==id, Ticket.status!="cancelled")).scalars().all()
            return screening
        except Exception as e:
            print(e)

def get_screenings_all():
    with Session(engine) as session:
        try:
            result = session.execute(select(Screening)).scalars().all()
            return result
        except Exception as e:
            print(e)

def patch_screening(screening):
    with Session(engine) as session:
        try:
            screening_obj = session.get(Screening, screening.id)
            if screening_obj:
                screening_obj.start_time = screening.start_time
                session.commit()
                return "Successful update"
            else:
                session.rollback()
                raise EntityNotFoundError(f"No screening_id with id:{screening.id}")
        except IntegrityError as e:
            print("--Error--", e)
            session.rollback()
            print(e)
            raise DatabaseConflictError("Conflict occured while deleting movie.") from e
        except SQLAlchemyError as e:
            session.rollback()
            print(e)
            raise DatabaseError("Database query Failed") from e

def delete_screening(screening):
    with Session(engine) as session:
        try:
            screening_obj = session.get(Screening, screening.id)
            if screening_obj:
                session.delete(screening_obj)
                session.commit()
            else:
                session.rollback()
                raise EntityNotFoundError(f"No screening_id with id:{screening.id}")
        except Exception as e:
            print(e)
            session.rollback()

def add_screening(screening):
    with Session(engine) as session:
        try:
            for time in screening.start_times:
                session.add(Screening(movie_id=screening.movie_id, start_time=time, theatre_id=screening.theatre_id))
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
    
# -- genres --

def post_genres(genres):
    with Session(engine) as session:
        try: 
            print(genres)
            session.execute(insert(Genre), genres,)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

def get_genres_all():
    with Session(engine) as session:
        try: 
            return session.execute(select(Genre).options(selectinload(Genre.movies)),).scalars().all()
        except Exception as e:
            print(e)

def create_theatre(id, name, per_row, rows):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    seats = [ {"id": alphabet[a]+str(n), "theatre_id": id} for a in range(rows) for n in range(1, per_row + 1)]
    for seat in seats:
        print(seat["id"], seat["theatre_id"])

    with Session(engine) as session:
        try: 
            print(f"inserting theatre with name: {name}, seats_per_row: {per_row}, number of rows: {rows}")
            session.execute(insert(Theatre).values(id=id, name=name, seats_per_row=per_row, number_of_rows=rows))
            session.execute(insert(Seat), seats)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()


# seats
def get_selected_seats(id):
    return get_screening(id).booked_seat_ids

def clean_pending_bookings():
    with Session(engine) as session:
        try:
            session.execute(delete(Booking).where(Booking.expires_at <= func.now(), Booking.status=="pending"))
            session.commit()
        except SQLAlchemyError as e:
            raise DatabaseError from e

# booking

def get_booking(id):
    with Session(engine) as session:
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

def confirm_booking(booking_id):
    with Session(engine) as session:
        try:
            booking = session.get(Booking, booking_id)
            if booking:
                booking.status='complete'
                session.commit()
            else:
                raise EntityNotFoundError(f"No booking with id:{booking_id}")
            return {"status": "successful", "booking": booking}
            
        except SQLAlchemyError as e:
            raise DatabaseError from e

def delete_booking(booking):
    with Session(engine) as session:
        try:
            booking_obj = session.get(Booking, booking.id)
            if booking_obj:
                for ticket in booking_obj.tickets:
                    session.delete(ticket)
                session.delete(booking_obj)
                session.commit()
            else:
                raise EntityNotFoundError(f"No booking with id:{booking.id}")
        except IntegrityError as e:
            print("--Error--", e)
            session.rollback()
            print(e)
            raise DatabaseConflictError("Conflict occured while deleting booking.") from e
        except SQLAlchemyError as e:
            session.rollback()
            print(e)
            raise DatabaseError("Database query Failed") from e


# tickets
def get_user_tickets(auth_id):
    with Session(engine) as session:
        try:
            result = session.execute(select(Ticket).where(Ticket.user_id==get_user_by_auth_id(auth_id).id).options(selectinload(Ticket.seat).selectinload(Seat.theatre), selectinload(Ticket.screening).selectinload(Screening.movie), selectinload(Ticket.booking))).scalars().all()
            print(result)
            return result
        except Exception as e:
            print(e)



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


        

