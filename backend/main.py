from fastapi import FastAPI, HTTPException, Request, Depends, status, WebSocket
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
import websocket

from fastapi import Depends

from fastapi.responses import JSONResponse

from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


manager = websocket.ConnectionManager()

scheduler = BackgroundScheduler()
scheduler.add_job(crud_operations.clean_pending_bookings, 'interval', seconds=10)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
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

@app.exception_handler(crud_operations.EntityNotFoundError)
def integrity_error(request: Request, exc: crud_operations.EntityNotFoundError):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    content={"detail": str(exc), "error_type": "entity_not_found_error"}
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
    movies = crud_operations.get_movies_upcoming()
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
    return crud_operations.delete_movie(movie)

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
    return
    print(crud_operations.get_genres_all())
    
# Booking

@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def add_booking(booking: validation.BookingAdd, claims: dict = Depends(auth0.require_auth())):
    return crud_operations.add_booking(booking, claims.sub)

@app.get("/bookings/{id}", response_model=validation.BookingBase)
def get_booking(id):
    return crud_operations.get_booking(id)

@app.post("/pay-booking")
async def pay_booking(data: validation.PaymentRequest):
    """
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            f"{DARWIN_BASE}/token",
            data={"username": data.username, "password": data.password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        print("Token status:", token_res.status_code)
        print("Token response:", token_res.text)
        print("Cookies after token:", client.cookies)
        
        if token_res.status_code != 200:
            raise HTTPException(status_code=401, detail="Authentication failed")

        transaction_res = await client.post(
            f"{DARWIN_BASE}/transaction/new",
            json={
                "from_account": data.from_account,
                "to_account": 63,
                "amount": data.amount * 100,
                "transaction_type": "cinema",
                "message": "Stonks goin up for cinema west frfr",
                "currency": "SEK",
            },
        )
        
        print("Transaction status:", transaction_res.status_code)
        print("Transaction response:", transaction_res.text)

        if transaction_res.status_code != 200:
            raise HTTPException(status_code=400, detail=transaction_res.json())
    
    """
    
    return crud_operations.confirm_booking(data.booking_id)
        



    return transaction_res.json()

# Tickets

@app.get("/tickets/me", response_model=List[validation.TicketResponse])
def get_user_tickets(claims: dict = Depends(auth0.require_auth())):
    return crud_operations.get_user_tickets(claims.sub)

#EVENT FUNCTIONS
@app.on_event("startup")
async def startup():
    return
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
    

@app.websocket("/ws/{screening_id}")
async def websocket(websocket: WebSocket, screening_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print("\n\n\n\n", "Thank you", data, "\n\n\n\n")
            booked_seats = crud_operations.get_selected_seats(screening_id)
            await manager.broadcast_seats_json(screening_id, {"msg": "Thank you", "booked_seat_ids": booked_seats})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        #await manager.broadcast(f"Client {screening_id} has left")
        

    




DARWIN_BASE = "https://darwinbank.duckdns.org/api"
