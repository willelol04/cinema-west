from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import httpx
import datetime
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import aiomysql
import json


import db
import models
from fastapi import Depends



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
def movie_is_added(id):
    movie = get_movie(id)
    return {"message": True if movie else False}

@app.get("/movie/{id}", response_model=models.Movie) 
def get_movie(id):
    return db.get_movie(id)


@app.get("/movies/all", response_model=List[models.Movie])
def get_movies_all():
    return db.get_movies_all()

@app.get("/theatres/all")
def get_theatres_all():
    return db.get_theatres_all()

# POST-REQUESTS

@app.post("/addmovie") 
def add_movie(movie: models.Movie):
    db.add_movie(movie)
    return movie

@app.post("/delete_movie") 
def delete_movie(movie: models.Movie):
    db.delete_movie(movie)
    return movie

@app.post("/adduser", response_model=models.UserResponse) 
def add_user(user: models.UserCreate):
    db.add_user(user)
    return user

@app.post("/addscreening")
def add_screening(screening: Screening):
    db.add_screening(screening)
    return screening






#EVENT FUNCTIONS


@app.on_event("shutdown")
async def shutdown():
    print("\n\nclosing tmdb_client\n\n")
    await tmdb_client.aclose()
    print("closed tmdb")
