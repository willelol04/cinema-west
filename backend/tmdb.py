import os
from dotenv import load_dotenv
from fastapi import HTTPException
import httpx

load_dotenv()
tmdb_key = os.getenv('TMDBKEY')

tmdb_headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_key}"
}

tmdb_client = httpx.AsyncClient(headers=tmdb_headers, base_url="https://api.themoviedb.org/3")

async def get_from_TMDB(path, parameters):
    response = await tmdb_client.get(url=path, params=parameters)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

async def get_genres():
    url = "/genre/movie/list"
    params = {}
    result = await get_from_TMDB(url, params)
    return result['genres']




