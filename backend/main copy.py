from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import httpx
import datetime
from pydantic import BaseModel
from typing import Optional
import asyncio
import aiomysql
import json
from sqlmodel import Field, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine





class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    f_name: str
    l_name: str
    email: str
    password: str
    is_admin: bool
    
db_url= f"mysql+aiomysql://cinema:6P3AZdYtUaWb7tBxHQa%@localhost:3306/cinema?charset=utf8mb4"

engine = create_async_engine(db_url, echo=True)

SQLModel.metadata.create_all(engine)





app = FastAPI()
load_dotenv()
tmdb_key = os.getenv('TMDBKEY')
banned_keywords = os.getenv('BANNED_KEYWORDS')
banned_keyword_list = banned_keywords.split(':')

tmdb_headers = {
    "accept": "application/json",
    "Authorization": "Bearer"+tmdb_key
}

tmdb_client = httpx.AsyncClient(headers=tmdb_headers, base_url="https://api.themoviedb.org/3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# VALIDATIONS BASEMODELS

class Movie(BaseModel):
    adult: Optional[bool] = None
    backdrop_path: Optional[str] = None
    genre_ids: Optional[list] = None
    id: Optional[int] = None
    original_language: Optional[str] = None
    original_title: Optional[str] = None
    overview: Optional[str] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    release_date: Optional[str] = None
    title: Optional[str] = None
    video: Optional[bool] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None

class User(BaseModel):
    f_name: str
    l_name: str
    email: str
    password: str
    
class Screening(BaseModel):
    movie_id: int
    theatre_id: int
    start_time: str


# HELPER FUNCTIONS
async def post_to_db(item: BaseModel, query, values):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            print("movie added")
            try:
                await cur.execute(query, values)
                await conn.commit()
                return "Successfully added item."
            except:
                return "Failed adding item."

async def delete_from_db(item: BaseModel, query, values):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(query, values)
                await conn.commit()
                return "Successfully deleted item."
            except:
                return "Falied deleting item."

async def get_from_db(query, values):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, values)
            result = await cur.fetchall()
            print(result)
            return {"result": result, "description": cur.description}


async def getFromTMDB(path, parameters): 
    response = await tmdb_client.get(url=path, params=parameters)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


# GET REQUESTS

@app.get("/movies/upcoming")
async def getUpcoming():
    url = "/discover/movie"
    today = datetime.date.today()
    print(today)
    params = {
              "include_video": 'false', 
              "language": "en-US", 
              "page": 1, 
              "primary_release_date.gte": today, 
              "primary_release_date.lte": "2026-10-12", 
              "with_origin_country": "US", 
              "sort_by":"popularity.desc",
              }
    return await getFromTMDB(url, params)

@app.get("/movies/search/{movie}")
async def searchMovie(movie):
    if movie not in banned_keyword_list:
        url = "https://api.themoviedb.org/3/search/movie"
        params = { 
                  "language": "en-US", 
                  "page": 1, 
                  "query": movie,
                  "sort_by":"popularity.desc",
                  }
        return await getFromTMDB(url, params)


@app.get("/movie/isadded/{id}")
async def movie_is_added(id):
    query = "select id from movie where id=%s;"
    values = id
    result = await get_from_db(query, values)
    print(result)
    return {"message": True if len(result['result']) != 0 else False}

@app.get("/movie/{id}")
async def get_movie(id):
    query = "select * from movie where id=%s;"
    values = id
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, values)
            result = await cur.fetchone()
            print(result)
            movie = {}
            for n in range(len(result)):
                movie[cur.description[n][0]] = result[n]
            return movie

@app.get("/movies/all")
async def get_movies_all():
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute('select * from movie;')
            r = await cur.fetchall()
            returnList = []
            for row in r:
                currObj = {}
                for n in range(len(cur.description)):
                    currObj[str(cur.description[n][0])]=str(row[n])
                print(currObj)
                returnList.append(currObj)
            print(returnList)
    
            return returnList

@app.get("/theatres/all")
async def get_theatres_all():
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute('select * from theatre;')
            r = await cur.fetchall()
            returnList = []
            for row in r:
                currObj = {}
                for n in range(len(cur.description)):
                    currObj[str(cur.description[n][0])]=str(row[n])
                print(currObj)
                returnList.append(currObj)
            print(returnList)
    
            return returnList


# POST-REQUESTS

@app.post("/addmovie") 
async def add_movie(movie: Movie):
    query = 'insert into movie(id, title, overview, poster_path, release_date, language) values(%s, %s, %s, %s, %s, %s);'
    values = (movie.id, movie.original_title, movie.overview, movie.poster_path, movie.release_date, movie.original_language)
    return await post_to_db(movie, query, values) 

@app.post("/delete_movie") 
async def delete_movie(movie: Movie):
        query = 'delete from cinema.screening where movie_id=%s; delete from cinema.movie where id=%s;'
        values = (movie.id, movie.id)
        return await delete_from_db(movie, query, values)

@app.post("/adduser") 
async def add_user(user: User):
    query = 'insert into user(f_name, l_name, email, password) values(%s, %s, %s, %s);'
    values = (user.f_name, user.l_name, user.email, user.password)
    return await post_to_db(user, query, values)

@app.post("/addscreening")
async def add_screening(screening: Screening):
    query = 'insert into screening(movie_id, theatre_id, start_time) values(%s, %s, %s);'
    values = (screening.movie_id, screening.theatre_id, screening.start_time)
    return await post_to_db(screening, query, values)






#EVENT FUNCTIONS

@app.on_event("startup")
async def startup_create_pool():
    global pool
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306, 
                                  user='cinema', password='6P3AZdYtUaWb7tBxHQa%', db='cinema')


@app.on_event("shutdown")
async def shutdown():
    print("\n\nclosing tmdb_client\n\n")
    await tmdb_client.aclose()
    print("closed tmdb")
    print("\n\nclosing pool\n\n")
    pool.close()
    await pool.wait_closed()
    print("closed pool")
