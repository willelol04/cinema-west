from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import httpx
import datetime
from pydantic import BaseModel
import asyncio
import aiomysql
import json

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
@app.get("/")
async def root():
    return {'message': 'hello world'}


async def getFromTMDB(path, parameters): 
    response = await tmdb_client.get(url=path, params=parameters)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()



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





@app.on_event("startup")
async def startup_create_pool():
    global pool
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306, 
                                  user='cinema', password='6P3AZdYtUaWb7tBxHQa%', db='cinema')







@app.get("/movies/all")
async def get_movies_all():
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute('select * from movie;')
            r = await cur.fetchall()
            #print(r)
            #print(cur.description)
            
            returnList = {}
            for row in r:
                currObj = {}
                for n in range(len(cur.description)):
                    currObj[str(cur.description[n][0])]=str(row[n])
                print(currObj)
                returnList.append(currObj)
            #print(returnList)
    
            return returnList

class Movie(BaseModel):
    id: str
    title: str
    overview: str
    poster_path: str
    release_date: str
    language: str

@app.post("/addmovie") 
async def add_movie(movie: Movie):
    print(movie)
    return {movie}
    """
    Docstring for add_movie
    
    :param movie: Description
    :type movie: Movie
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute('use cinema;')
            await cur.execute(f'insert into movie(id, title, overview, release_date, language) values(1352, "movie {inc}", "Lorem ipsum dolor sit amet, ipsum dolor sit amet, ipsum dolor sit amet.", "2024-01-01", "en");')
            
            await conn.commit()
            print("movie added -", inc)
            inc = inc +1
    """






        
@app.on_event("shutdown")
async def shutdown():
    print("\n\nclosing tmdb_client\n\n")
    await tmdb_client.aclose()
    print("closed tmdb")
    print("\n\nclosing pool\n\n")
    pool.close()
    await pool.wait_closed()
    print("closed pool")