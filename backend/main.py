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


async def getFromTMDB(path, parameters): 
    response = await tmdb_client.get(url=path, params=parameters)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


# GET REQUESTS

@app.get("/tmdb/movies/upcoming")
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

@app.get("/tmdb/movies/search/{query}")
async def searchMovie(query):
    if query not in banned_keyword_list:
        url = "/search/movie"
        params = { 
                  "language": "en-US", 
                  "page": 1, 
                  "query": query,
                  "sort_by":"popularity.desc",
                  }
        return await getFromTMDB(url, params)

@app.get("/tmdb/movies/{id}")
async def getMovieDetails(id):
        url = "/movie/"+id
        params = {}
        return await getFromTMDB(url, params)


@app.get("/movie/isadded/{id}")
def movie_is_added(id):
    movie = get_movie(id)
    return {"message": True if movie else False}

@app.get("/movies/{id}") 
def get_movie(id):
    return db.get_movie(id)

@app.get("/movies", response_model=List[models.Movie])
def get_movies_all():
    return db.get_movies_all()

@app.get("/theatres")
def get_theatres_all():
    return db.get_theatres_all()

# POST-REQUESTS

@app.post("/movies") 
def add_movie(movie: models.Movie):
    db.add_movie(movie)
    return movie

@app.delete("/movies") 
def delete_movie(movie: models.Movie):
    db.delete_movie(movie)
    return movie

@app.post("/users", response_model=models.UserResponse) 
def add_user(user: models.UserCreate):
    db.add_user(user)
    return user

@app.post("/screenings")
def add_screening(screening: Screening):
    db.add_screening(screening)
    return screening

@app.get("/screenings/{id}")
def get_screening(id):
    return db.get_screening(id)

@app.get("/screenings")
def get_screenings_all():
    return db.get_screenings_all()

# Genre

async def get_genres():
        url = "/genre/movie/list"
        params = {}
        result = await getFromTMDB(url, params)
        return result['genres']

def post_genres(genres):
    db.post_genres(genres)
    return genres

def get_genres_all():
    print(db.get_genres_all())


#EVENT FUNCTIONS
@app.on_event("startup")
async def startup():
    for each in db.get_genres_all():
        print(each.name, end=": ")
        for e in each.movies:
            print(e.title, end=", ")
        print("\n")




@app.on_event("shutdown")
async def shutdown():
    print("\n\nclosing tmdb_client\n\n")
    await tmdb_client.aclose()
    print("closed tmdb")
