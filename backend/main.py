from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi_plugin.fast_api_client import Auth0FastAPI
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


import crud_operations
import validation
from fastapi import Depends

from fastapi.responses import JSONResponse




app = FastAPI()
load_dotenv()
tmdb_key = os.getenv('TMDBKEY')
banned_keywords = os.getenv('BANNED_KEYWORDS')
auth0_domain = os.getenv('AUTH0_DOMAIN')
auth0_audience = os.getenv('AUTH0_AUDIENCE')
banned_keyword_list = banned_keywords.split(':')

auth0 = Auth0FastAPI(
    domain=auth0_domain,
    audience=auth0_audience,
)

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
    expose_headers=["*"],
)

@app.exception_handler(crud_operations.DatabaseConflictError)
def integrity_error(request: Request, exc: crud_operations.DatabaseConflictError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
    content={"detail": str(exc), "error_type": "conflict"}
    )

@app.exception_handler(crud_operations.DatabaseError)
def integrity_error(request: Request, exc: crud_operations.DatabaseError):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content={"detail": str(exc), "error_type": "database_error"}
    )


async def getFromTMDB(path, parameters): 
    response = await tmdb_client.get(url=path, params=parameters)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/api/private")
def private(claims: dict = Depends(auth0.require_auth())):
   # A valid access token is required to access this route
       return {"message": "private API call successful.", "claims": claims}


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

@app.get("/movies/id/{id}") 
def get_movie(id: int):
    return crud_operations.get_movie(id)

@app.get("/movies/upcoming") 
def get_movies_upcoming():
    movies = crud_operations.get_movies_upcoming(datetime.datetime.now())
    print(movies)
    return movies

@app.get("/movies", response_model=List[validation.Movie])
def get_movies_all():
    return crud_operations.get_movies_all()

@app.get("/theatres")
def get_theatres_all():
    return crud_operations.get_theatres_all()

# POST-REQUESTS

@app.post("/movies", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth0.require_auth())])
def add_movie(movie: validation.Movie):
    crud_operations.add_movie(movie)
    return movie

@app.delete("/movies", dependencies=[Depends(auth0.require_auth())])
def delete_movie(movie: validation.Movie):
    crud_operations.delete_movie(movie)
    return movie

@app.post("/users", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth0.require_auth())])
def add_user(user: validation.UserAuth):
    print("------")
    print(user)
    print("------")
    crud_operations.add_user(user)
    return user

@app.get("/users/{id}")
def get_user(id):
    return crud_operations.get_user_by_id(id)

@app.get("/auth0/users/{auth_id}")
def get_user(auth_id):
    return crud_operations.get_user_by_auth_id(auth_id)

@app.post("/screenings", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth0.require_auth())])
def add_screening(screening: validation.ScreeningAdd):
    crud_operations.add_screening(screening)
    return screening

@app.get("/screenings/{id}")
def get_screening(id):
    return crud_operations.get_screening(id)

@app.get("/screenings")
def get_screenings_all():
    return crud_operations.get_screenings_all()

# Genre

async def get_genres():
        url = "/genre/movie/list"
        params = {}
        result = await getFromTMDB(url, params)
        return result['genres']

def post_genres(genres):
    crud_operations.post_genres(genres)
    return genres

def get_genres_all():
    print(crud_operations.get_genres_all())
    
# Ticket

@app.post("/tickets", status_code=status.HTTP_201_CREATED)
def add_tickets(ticket: validation.TicketAdd, claims: dict = Depends(auth0.require_auth())):
    return crud_operations.add_tickets(ticket, claims.sub)



#EVENT FUNCTIONS
@app.on_event("startup")
async def startup():
    for each in crud_operations.get_genres_all():
        print(each.name, end=": ")
        for e in each.movies:
            print(e.title, end=", ")
        print("\n")



@app.on_event("shutdown")
async def shutdown():
    print("\n\nclosing tmdb_client\n\n")
    await tmdb_client.aclose()
    print("closed tmdb")
