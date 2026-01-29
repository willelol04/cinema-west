from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import httpx

app = FastAPI()
load_dotenv()
tmdb_key = os.getenv('TMDBKEY')
tmdb_headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwMDFkNjE4ZGY1MjIyZWYzZmQ0OGI4MmI4ZDhlOWMyMiIsIm5iZiI6MTc2ODA3NTg2My43MzQwMDAyLCJzdWIiOiI2OTYyYjI1NzMwOTMzNWQ5NzFiZDNkZGIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.x0SqioH1dam9lnA-SUKBH2bH4zq4crkVB1owOPHWJ8k"
}

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

@app.get("/getupcoming")
async def getUpcoming():
            
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer"+tmdb_key
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="weather service error")

    return response.json()