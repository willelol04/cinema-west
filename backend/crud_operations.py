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

from models import engine, Base, movie_genre, Movie, User, Genre, Theatre, Ticket, Screening, Seat
import validation

import datetime

class DatabaseConflictError(Exception):
    pass

class DatabaseError(Exception):
    pass



def add_tickets(ticket: validation.TicketAdd, auth_id: str):
    print("--------------------------------")
    print(ticket, auth_id)
    print("--------------------------------")
    with Session(engine) as session:
        try:
            id = get_user_by_auth_id(auth_id).id
            for seat in ticket.seats:
                print("--------------------------------")
                print(seat)
                print("--------------------------------")
                session.execute(insert(Ticket).values(user_id=id, screening_id=ticket.screening_id, created_at=func.now(), expires_at=func.adddate(func.now(), text("INTERVAL 5 MINUTE")), seat_id=seat["id"], theatre_id=seat["theatre_id"]))
            session.commit()
            return ticket
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
            user_obj = session.get(User, user.id) 
            session.delete(user_obj)
            session.commit()
        except Exception as e:
            print("--Error--", e)
            session.rollback()

def add_user(user: validation.UserAuth):
    with Session(engine) as session:
        try:
            session.execute(insert(User).values(auth_id=user.sub))
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
            result = session.execute(select(Movie).options(selectinload(Movie.screenings))).scalars().all()
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

def delete_screening(screening):
    with Session(engine) as session:
        try:
            screening_obj = session.get(Screening, screening.id)
            session.delete(screening_obj)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

def add_screening(screening):
    with Session(engine) as session:
        try:
            screening_obj = Screening(**screening.dict())
            session.add(screening_obj)
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


def clean_unfinished_tickets():
    with Session(engine) as session:
        try:
            session.execute(delete(Ticket).where(Ticket.expires_at <= func.now(), Ticket.status=="registered"))
            session.commit()
        except SQLAlchemyError as e:
            raise DatabaseError from e


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
#        User.__table__.create(bind=engine, checkfirst=True)
        Movie.__table__.create(bind=engine, checkfirst=True)
        Theatre.__table__.create(bind=engine, checkfirst=True)
        Seat.__table__.create(bind=engine, checkfirst=True)
        Screening.__table__.create(bind=engine, checkfirst=True)
        create_theatre(1, "Salong A", 10, 3)
        Ticket.__table__.create(bind=engine, checkfirst=True)

        #some_user = session.get(User, 1)

        session.commit()
    
    
    
    Base.metadata.create_all(engine)


        

