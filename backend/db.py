import sqlalchemy
import asyncio
import aiomysql
import pymysql
from typing import List
from typing import Optional
from sqlalchemy import Column, insert, Integer, String, Date, DateTime, Boolean, create_engine, text, ForeignKey, UniqueConstraint, Engine, select, Table
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload


import models



class Base (DeclarativeBase):
    pass

movie_genre = Table("movie_genre", Base.metadata, Column("movie_id", Integer, ForeignKey("movie.id"), primary_key=True), Column("genre_id", Integer, ForeignKey("genre.id"), primary_key=True))


    

class Movie(Base):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    overview: Mapped[str] = mapped_column(String(1000))
    poster_path: Mapped[str] = mapped_column(String(1000))
    release_date: Mapped[str] = mapped_column(Date, default="2024-01-01")
    language: Mapped[str] = mapped_column(String(10))

    screenings: Mapped[List["Screening"]] = relationship()
    genres: Mapped[List["Genre"]] = relationship(secondary=movie_genre)

class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    movies: Mapped[List["Movie"]] = relationship(secondary=movie_genre)
    

    
    

    


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    f_name: Mapped[str] = mapped_column(String(50))
    l_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(30))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)


class Theatre(Base):
    __tablename__ = "theatre"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    
class Seat(Base):
    __tablename__ = "seat"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    number: Mapped[int]
    theatre_id: Mapped[int] = mapped_column(ForeignKey("theatre.id"))

    __table_args__ = (UniqueConstraint("theatre_id", "number", name="yes"), )
    

class Screening(Base):
    __tablename__ = "screening"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movie.id"))
    theatre_id: Mapped[int] = mapped_column(ForeignKey("theatre.id"))
    start_time: Mapped[str] = mapped_column(DateTime)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (UniqueConstraint("theatre_id", "start_time", name="yes"), )
    

class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    screening_id: Mapped[int] = mapped_column(ForeignKey("screening.id"))
    seat_id: Mapped[int] = mapped_column(ForeignKey("seat.id"))
    created_at: Mapped[str] = mapped_column(DateTime, default="2024-01-01T13:45:30")
    is_cancelled: Mapped[bool] = mapped_column(default=False)
    
    __table_args__ = (UniqueConstraint("screening_id", "seat_id", name="yes"), )









engine = create_engine(
"mysql+pymysql://cinema:6P3AZdYtUaWb7tBxHQa%@127.0.0.1/cinema?charset=utf8mb4",
echo = True)



# -- Users --
def get_user(id):
    with Session(engine) as session:
        try:
            result = session.get(User, id)
            return result
        except Exception as e:
            print("--Error--", e)
            session.rollback()

def get_users_all():
    with Session(engine) as session:
        try:
            result = session.execute(select(User)).scalars().all()
            return result
        except Exception as e:
            print("--Error--", e)
            session.rollback()

def delete_user(user: models.UserResponse):
    with Session(engine) as session:
        try:
            user_obj = session.get(User, user.id) 
            session.delete(user_obj)
            session.commit()
        except Exception as e:
            print("--Error--", e)
            session.rollback()

def add_user(user: models.UserCreate):
    with Session(engine) as session:
        try:
            user_obj = User(**user.dict()) 
            session.add(user_obj)
            session.commit()
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

def delete_theatre(screening: models.Theatre):
    with Session(engine) as session:
        try:
            theatre_obj = session.get(Theatre, screening.id)
            session.delete(theatre_obj)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

def add_screening(theatre: models.Theatre):
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
            result = session.execute(select(Movie)).scalars().all()
            return result
        except Exception as e:
            print(e)

def delete_movie(movie: models.Movie):
    with Session(engine) as session:
        try:
            db_movie = session.get(Movie, movie.id)
            for screening in db_movie.screenings:
                session.delete(screening)
            session.delete(db_movie)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

def add_movie(movie: models.Movie):
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
            result = session.get(Screening, id)
            return result
        except Exception as e:
            print(e)

def get_screenings_all():
    with Session(engine) as session:
        try:
            result = session.execute(select(Screening)).scalars().all()
            return result
        except Exception as e:
            print(e)

def delete_screening(screening: models.Screening):
    with Session(engine) as session:
        try:
            screening_obj = session.get(Screening, screening.id)
            session.delete(screening_obj)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()

def add_screening(screening: models.Screening):
    with Session(engine) as session:
        try:
            screening_obj = Screening(**screening.dict())
            session.add(screening_obj)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
    
# -- genres --

def post_genres(genres: List[models.Genre]):
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



if __name__ == "__main__":

    first_user = User(f_name="yes", l_name="no", email="email", password="password") 
    add_user(user=first_user)


    with Session(engine) as session:

#        Ticket.__table__.drop(bind=engine, checkfirst=True)
#        Screening.__table__.drop(bind=engine, checkfirst=True)
#        Seat.__table__.drop(bind=engine, checkfirst=True)
#        Theatre.__table__.drop(bind=engine, checkfirst=True)
#        User.__table__.drop(bind=engine, checkfirst=True)
#        Movie.__table__.drop(bind=engine, checkfirst=True)
#        MovieGenre.__table__.drop(bind=engine, checkfirst=True)
##    
##
#        User.__table__.create(bind=engine, checkfirst=True)
#        Theatre.__table__.create(bind=engine, checkfirst=True)
#        Seat.__table__.create(bind=engine, checkfirst=True)
#        Screening.__table__.create(bind=engine, checkfirst=True)
#        Ticket.__table__.create(bind=engine, checkfirst=True)
        
        #some_user = session.get(User, 1)
        Movie.__table__.create(bind=engine, checkfirst=True)
        session.commit()
    
    Base.metadata.create_all(engine)


        

