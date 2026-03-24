import sqlalchemy
import asyncio
import aiomysql
import pymysql
from typing import List, Any
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

from tmdb import get_genres

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
            finally:
                session.close()



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


def add_booking(user, booking, session):
        try:
            created_tickets = []
            booking_id = session.execute(insert(Booking).values(user_id=user.id, screening_id=booking.screening_id, total_price=100*len(booking.seats)).returning(Booking.id)).scalar()
            for seat in booking.seats:
                t = Ticket(booking_id=booking_id, screening_id=booking.screening_id, seat_id=seat["id"], theatre_id=seat["theatre_id"])
                created_tickets.append(t)
            session.add_all(created_tickets)
            session.flush()
            return get_booking(user, booking_id, session)
        except IntegrityError as e:
            raise DatabaseConflictError("Seat already booked") from e
        except SQLAlchemyError as e:
            raise DatabaseError("Database Insertion Failed") from e


# -- Users --
def get_user_by_id(id, session):
    user = session.execute(select(User).where(User.id==id)).scalar()
    if user:
        return user
    else:
        raise EntityNotFoundError(f"User with id {id} not found.")

def get_user_by_sub(sub, session):
        user = session.execute(select(User).where(User.sub==sub)).scalar()
        if user:
            return user
        else: 
            raise EntityNotFoundError(f"User with sub {sub} not found.")

def search_user(query, session):
    return session.execute(select(User).where(User.email.contains(query), User.is_admin != True).options(selectinload(User.bookings).selectinload(Booking.tickets), selectinload(User.bookings).selectinload(Booking.screening).selectinload(Screening.movie))).scalars().all()

def delete_user(user, session):
    try:
        user = get_user_by_sub(user.sub, session)
        if not user:
            raise EntityNotFoundError(f"No user with id:{user.id}")

        if not user.is_admin:
            session.delete(user)
        else:
            raise SQLAlchemyError
    except IntegrityError as e:
        raise DatabaseConflictError("Conflict occured while deleting user") from e
    except SQLAlchemyError as e:
        raise DatabaseError("Database query Failed. Cannot delete admin from API endpoint.") from e

def add_user(user, session):
    try:
        added_user = User(sub=user.sub, nickname=user.nickname, email=user.email, is_admin=user.is_admin)
        session.add(added_user)
        session.flush()
        #session.execute(insert(User).values(sub=user.sub, nickname=user.nickname, email=user.email, is_admin=user.is_admin))
        return added_user
    except SQLAlchemyError as e:
        raise DatabaseError("Database query Failed. Cannot add user.") from e

def patch_current_user_role(sub, is_admin, session):
        user = get_user_by_sub(sub, session)
        user.is_admin = is_admin
        session.flush()

        return user
        return session.execute(update(User).where(User.sub==sub).values(is_admin=is_admin))

# -- Theatres --
def get_theatre(id, session):
    theatre = session.get(Theatre, id)
    if theatre:
        return theatre
    else:
        raise EntityNotFoundError(f"No theatre with id: {id}")

def get_theatres_all(session):
    theatres = session.execute(select(Theatre)).scalars().all()
    return theatres

# -- Movies --
def get_movie(id, session):
    movie = session.execute(select(Movie).where(Movie.id==id).options(selectinload(Movie.screenings), selectinload(Movie.genres))).scalars().first()
    if not movie:
        raise EntityNotFoundError(f"No movie with id:{id}")
    return movie

def get_movies_all(title, genre, rating, session):
    stmt = select(Movie)
    if title:
        stmt = stmt.where(Movie.title.contains(title))
    if rating:
        stmt = stmt.where(Movie.rating!=None).where(Movie.rating==rating)
    if genre:
        stmt = stmt.join(Movie.genres).where(Genre.id == genre)

    result = session.execute(stmt.options(selectinload(Movie.screenings).selectinload(Screening.theatre)).order_by(Movie.created_at.desc())).scalars().all()

    return result

def get_movies_schedule(session):
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    tomorrow_start = today_start + timedelta(hours=24)
    tomorrow_end = today_end + timedelta(hours=24)

    todays_movies = session.execute(select(Movie).join(Screening).where(Screening.start_time >= today_start).where(Screening.start_time <= today_end).distinct()).scalars().all()

    tomorrows_movies = session.execute(select(Movie).join(Screening).where(Screening.start_time >= tomorrow_start).where(Screening.start_time <= tomorrow_end).distinct()).scalars().all()

    upcoming_movies = session.execute(select(Movie).where(Movie.release_date > datetime.now(timezone.utc))).scalars().all()

    return {"today": todays_movies, "tomorrow": tomorrows_movies, "upcoming": upcoming_movies}

def delete_movie(movie, session):
    try:
        movie_to_delete = get_movie(movie.id, session)
        session.delete(movie_to_delete)
        session.flush()
    except IntegrityError as e:
        raise DatabaseConflictError("Conflict occured while deleting movie.") from e
    except SQLAlchemyError as e:
        raise DatabaseError("Database query Failed") from e

def add_movie(movie, session):
    try:
        rating = None
        for country in movie['releases']['countries']:
            if country["iso_3166_1"] == "US" and country["certification"] != '':
                rating = country["certification"]
                
        movie_to_add = Movie(id=movie["id"],
                         title=movie["title"], 
                         overview=movie["overview"], 
                         runtime=movie["runtime"],
                         poster_path=movie["poster_path"], 
                         backdrop_path=movie["backdrop_path"], 
                         rating=rating,
                         language=movie["original_language"], 
                         release_date=movie["release_date"])


        session.add(movie_to_add)
        session.flush()

        for genre in movie["genres"]:
            session.execute(insert(movie_genre).values(genre_id=genre["id"], movie_id=movie["id"]))


        return movie_to_add

    except IntegrityError as e:
        print(e)
        raise DatabaseConflictError("Conflict occured while adding movie.") from e
    except SQLAlchemyError as e:
        print(e)
        raise DatabaseError("Database query Failed. Cannot add movie to database.") from e

    
    



# -- Screenings --
def get_screening(id, session):
    screening = session.execute(select(Screening).where(Screening.id==id).options(selectinload(Screening.movie), selectinload(Screening.theatre).selectinload(Theatre.seats))).scalars().first()
    if not screening:
        raise EntityNotFoundError(f"No screening with id: {id}")
    screening.booked_seat_ids = session.execute(select(Ticket.seat_id).where(Ticket.screening_id==id)).scalars().all()
    return screening

def get_screenings_all(title, session):
        stmt = select(Screening)

        if title:
            stmt = stmt.join(Movie).where(Movie.title.contains(title))

        result = session.execute(stmt.options(selectinload(Screening.movie), selectinload(Screening.theatre)).order_by(Screening.start_time)).scalars().all()
        return result

"""
def patch_screening(screening, session):
    try:
        screening_to_patch = session.get(Screening, screening.id)

        if not screening_to_patch:
            raise EntityNotFoundError(f"No screening_id with id: {screening.id}")
        screening_to_patch.start_time = screening.start_time
        return "Successful update"

    except SQLAlchemyError as e:
        raise DatabaseError("Database query Failed") from e

"""

def delete_screening(screening, session):
    screening_to_delete = session.get(Screening, screening.id)

    if not screening_to_delete:
        raise EntityNotFoundError(f"No screening with id:{screening.id}")
    session.delete(screening_to_delete)


def add_screening(screening, session):
    try:
        added_screenings = []
        for time in screening.start_times:
            screening_to_add = Screening(movie_id=screening.movie_id, start_time=time, theatre_id=screening.theatre_id)
            session.add(screening_to_add)
            added_screenings.append(screening_to_add)

        session.flush()

        return added_screenings

    except IntegrityError as e:
        raise DatabaseConflictError("Conflict occured while adding screening(s).") from e

# -- genres --

async def add_genres():
    genres = await get_genres()
    with Session(engine) as session:
        session.execute(insert(Genre), genres)
        session.commit()

def get_genres_all(session):
    return session.execute(select(Genre).options(selectinload(Genre.movies)),).scalars().all()

def add_theatre(name, per_row, rows, session):
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    try: 
        theatre_to_add = Theatre(name=name, seats_per_row=per_row, number_of_rows=rows)
        session.add(theatre_to_add)
        session.flush()
        seats = [{"id": alphabet[a] + str(n), "theatre_id": theatre_to_add.id} for a in range(rows) for n in range(1, per_row + 1)]
        session.execute(insert(Seat), seats)

    except IntegrityError as e:
        raise DatabaseConflictError("Conflict occured while adding theatre.") from e
    except SQLAlchemyError as e:
        raise DatabaseError("Database query Failed. Cannot add theatre to database.") from e


# seats
def get_selected_seats(id: object, session: object) -> Any:
    return get_screening(id, session).booked_seat_ids

def clean_pending_bookings():
    with Session(engine) as session:
        try:
            screenings_to_update = session.execute(select(Screening.id).join(Booking).where(Booking.expires_at <= datetime.now(timezone.utc), Booking.status=="pending").distinct()).scalars().all()
            session.execute(delete(Booking).where(Booking.expires_at <= datetime.now(timezone.utc), Booking.status=="pending"))
            session.commit()
            return screenings_to_update
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseError("Database query failed. Could not clean pending tickets.") from e

# booking
def get_booking(user, id, session):
    try:
        booking = session.get(Booking, id, options=[selectinload(Booking.tickets), selectinload(Booking.screening)])

        if not booking:
            raise EntityNotFoundError(f"No booking with id:{id}")

        if booking.user_id == user.id or user.is_admin:
            return booking
        else:
            raise AuthorizationError(user.id)

    except SQLAlchemyError as e:
        raise DatabaseError from e

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

    except SQLAlchemyError as e:
        raise DatabaseError("Database query failed. Could not confirm booking.") from e

def delete_booking(booking, session, user):
    try:
        booking_to_delete = session.get(Booking, booking.id)
        if not (booking_to_delete.user_id == user.id or user.is_admin):
            raise AuthorizationError(user.id)

        if not booking_to_delete:
            raise EntityNotFoundError(f"No booking with id:{booking.id}")

        session.delete(booking_to_delete)

    except IntegrityError as e:
        raise DatabaseConflictError("Conflict occured while deleting booking.") from e
    except SQLAlchemyError as e:
        raise DatabaseError("Database query Failed. Could not delete booking.") from e


# tickets
def get_user_bookings(user, session):
    result = session.execute(select(Booking)
                             .where(Booking.user_id==user.id)
                             .options(
                                 selectinload(Booking.tickets).selectinload(Ticket.seat).selectinload(Seat.theatre),
                                 selectinload(Booking.tickets).selectinload(Ticket.screening).selectinload(Screening.movie),
                                 selectinload(Booking.screening).selectinload(Screening.theatre)
                                )).scalars().all()
    return result


def get_filters(session):
    genres = session.execute(select(Genre).where(Genre.movies.any()).order_by(Genre.name)).scalars().all()
    ratings = session.execute(select(Movie.rating).where(Movie.rating != None).distinct()).scalars().all()
    return {"genres": genres, "ratings": ratings}


async def main():
        #Base.metadata.drop_all(engine)
        with Session(engine) as session:

            Genre.__table__.create(bind=engine, checkfirst=True)
            User.__table__.create(bind=engine, checkfirst=True)
            Movie.__table__.create(bind=engine, checkfirst=True)
            Theatre.__table__.create(bind=engine, checkfirst=True)
            Seat.__table__.create(bind=engine, checkfirst=True)
            Screening.__table__.create(bind=engine, checkfirst=True)
            Booking.__table__.create(bind=engine, checkfirst=True)
            Ticket.__table__.create(bind=engine, checkfirst=True)
            add_theatre("Onyx", 24, 5, session)

            session.commit()

        Base.metadata.create_all(engine)
        await add_genres()

if __name__ == "__main__":
    asyncio.run(main())
