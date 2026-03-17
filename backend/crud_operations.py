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
from datetime import timedelta, datetime, timezone

from models import engine, Base, movie_genre, Movie, User, Genre, Theatre, Ticket, Screening, Seat, Booking
import validation

from contextlib import contextmanager


def create_session():
    with Session(engine) as session:
        with session.begin():
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
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

class AuthorizationError(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
    def __str__(self):
        return f"User with id: {self.user_id} not authorized for this task."

class BookingAlreadyPaidError(Exception):
    def __init__(self, booking_id):
        self.booking_id = booking_id

    def __str__(self):
        return f"Booking has already been paid for."


def add_booking(user, booking: validation.BookingAdd, session):
        try:
            created_tickets = []
            booking_id = session.execute(insert(Booking).values(user_id=user.id, screening_id=booking.screening_id, total_price=100*len(booking.seats)).returning(Booking.id)).scalar()
            for seat in booking.seats:
                t = Ticket(booking_id=booking_id, screening_id=booking.screening_id, seat_id=seat["id"], theatre_id=seat["theatre_id"])
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

def get_user_by_sub(sub, session):
    try:
        user = session.execute(select(User).where(User.sub==sub)).scalar()
        if user:
            return user
        else: 
            raise EntityNotFoundError(f"User with id {sub} not found.")
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
        results = session.execute(select(User).where(User.email.contains(query), User.is_admin != True).options(selectinload(User.bookings).selectinload(Booking.tickets), selectinload(User.bookings).selectinload(Booking.screening).selectinload(Screening.movie))).scalars().all()
        print(results)
        return results
    except Exception as e:
        raise

def delete_user(user, session):
    try:
        user = get_user_by_sub(user.sub, session)
        if not user:
            raise EntityNotFoundError(f"No user with id:{user.id}")

        if not user.is_admin:
            session.delete(user)
        else:
            raise SQLAlchemyError
        return {"id": user.sub}
    except IntegrityError as e:
        print(e)
        raise DatabaseConflictError("Conflict occured while deleting movie.") from e
    except SQLAlchemyError as e:
        print(e)
        raise DatabaseError("Database query Failed. Cannot delete admin from API endpoint.") from e
    except Exception as e:
        print(e)
        raise

def add_user(user, session):
    try:
        session.execute(insert(User).values(sub=user.sub, nickname=user.nickname, email=user.email, is_admin=user.is_admin))
        return user
    except Exception as e:
        print("--Error--", e)
        raise

def patch_current_user_role(sub, is_admin, session):
    try:
        return session.execute(update(User).where(User.sub==sub).values(is_admin=is_admin))
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



# -- Movies --
def get_movie(id, session):
    try:
        result = session.execute(select(Movie).where(Movie.id==id).options(selectinload(Movie.screenings), selectinload(Movie.genres))).scalars().first()
        if not result:
            raise EntityNotFoundError(f"No movie with id:{id}")
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
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        tomorrow_start = today_start + timedelta(hours=24)
        tomorrow_end = today_end + timedelta(hours=24)

        todays_movies = session.execute(select(Movie).join(Screening).where(Screening.start_time >= today_start).where(Screening.start_time <= today_end).distinct()).scalars().all()

        tomorrows_movies = session.execute(select(Movie).join(Screening).where(Screening.start_time >= tomorrow_start).where(Screening.start_time <= tomorrow_end).distinct()).scalars().all()

        upcoming_movies = session.execute(select(Movie).where(Movie.release_date > func.now())).scalars().all()

        return {"today": todays_movies, "tomorrow": tomorrows_movies, "upcoming": upcoming_movies}
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
                         backdrop_path=movie["backdrop_path"], 
                         rating=rating,
                         language=movie["original_language"], 
                         release_date=movie["release_date"])
        session.add(movie_obj)
        session.flush()

        for genre in movie["genres"]:
            print(genre)
            session.execute(insert(movie_genre).values(genre_id=genre["id"], movie_id=movie["id"]))
    except Exception as e:
        print(e)
        raise
    
    
    



# -- Screenings --
def get_screening(id, session):
    try:
        screening = session.execute(select(Screening).where(Screening.id==id).options(selectinload(Screening.movie), selectinload(Screening.theatre).selectinload(Theatre.seats))).scalars().first()
        screening.booked_seat_ids = session.execute(select(Ticket.seat_id).where(Ticket.screening_id==id)).scalars().all()
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

def get_booking(user, id, session):
    try:
        booking = session.get(Booking, id, options=[selectinload(Booking.tickets)])
        if booking:
                if booking.user_id == user.id or user.is_admin:
                    return booking
                else:
                    raise AuthorizationError(user.id)
        else:
            raise EntityNotFoundError(f"No booking with id:{id}")
    except SQLAlchemyError as e:
        raise DatabaseError from e
    except Exception as e:
        print(e)
        raise

def confirm_booking(user, booking_id, session):
    try:
        booking = session.get(Booking, booking_id)

        if not booking:
            raise EntityNotFoundError(f"No booking with id:{booking_id}")

        if user.id != booking.user_id:
            raise AuthorizationError(user.id)

        if booking.status == 'complete':
            raise BookingAlreadyPaidError(booking_id)
        
        booking.status='complete'
        booking.paid_at=datetime.now(timezone.utc)

        return {"status": "successful", "booking": booking}
        
    except SQLAlchemyError as e:
        raise DatabaseError from e

def delete_booking(booking, session, user):
    try:
        booking_obj = session.get(Booking, booking.id)
        if booking_obj.user_id == user.id or user.is_admin:
            if booking_obj:
                session.delete(booking_obj)
            else:
                raise EntityNotFoundError(f"No booking with id:{booking.id}")
        else:
            raise AuthorizationError(user.id)
    except IntegrityError as e:
        print("--Error--", e)
        raise DatabaseConflictError("Conflict occured while deleting booking.") from e
    except SQLAlchemyError as e:
        print(e)
        raise DatabaseError("Database query Failed") from e


# tickets
def get_user_bookings(user, session):
    try:
        result = session.execute(select(Booking)
                                 .where(Booking.user_id==user.id)
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
        #create_theatre(1, "Salong A", 20, 7, session)
        Booking.__table__.create(bind=engine, checkfirst=True)
        Ticket.__table__.create(bind=engine, checkfirst=True)

        #some_user = session.get(User, 1)

        session.commit()
    
    
    
    Base.metadata.create_all(engine)


        

