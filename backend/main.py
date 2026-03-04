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
from sqlalchemy.orm import Session
import atexit
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from models import engine


manager = websocket.ConnectionManager()

scheduler = BackgroundScheduler()
scheduler.add_job(crud_operations.clean_pending_bookings, 'interval', seconds=10)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
app = FastAPI()
load_dotenv()
tmdb_key = os.getenv('TMDBKEY')
auth0_domain = os.getenv('AUTH0_DOMAIN')
auth0_audience = os.getenv('AUTH0_AUDIENCE')
auth0_client_id = os.getenv('AUTH0_CLIENT_ID')
auth0_client_secret = os.getenv('AUTH0_CLIENT_SECRET')

auth0 = Auth0FastAPI(
    domain=auth0_domain,
    audience=auth0_audience,
)

tmdb_headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_key}"
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
async def search_movie(query):
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
        url = f"/movie/{id}"
        params = {"append_to_response": "releases"}
        return await getFromTMDB(url, params)



@app.get("/movies/id/{id}") 
def get_movie(id: int, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_movie(id, session)

@app.get("/movie/isadded/{id}")
def movie_is_added(id, session: Session = Depends(crud_operations.create_session)):
    movie = get_movie(id, session)
    return {"message": True if movie else False}

@app.get("/movies/upcoming") 
def get_movies_upcoming(session: Session = Depends(crud_operations.create_session)):
    movies = crud_operations.get_movies_upcoming(session)
    print(movies)
    return movies

@app.get("/movies/", response_model=List[validation.MovieAdmin])
def get_movies_all(title: str | None = None, genre: int | None = None, rating: str | None = None, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_movies_all(title, genre, rating, session)

@app.get("/movies/schedule", response_model=validation.MovieSchedule)
def get_movies_schedule(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_movies_schedule(session)

@app.get("/theatres")
def get_theatres_all(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_theatres_all(session)

# POST-REQUESTS

@app.post("/movies/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth0.require_auth())])
async def add_movie(movie: validation.MovieBase, session: Session = Depends(crud_operations.create_session)):
    url = f"/movie/{movie.id}?append_to_response=release_dates"
    params = {"append_to_response": "releases"}
    movie_res = await getFromTMDB(url, params)
    print(movie_res)
    return crud_operations.add_movie(movie_res, session)

@app.delete("/movies/", dependencies=[Depends(auth0.require_auth())])
def delete_movie(movie: validation.Movie,session: Session = Depends(crud_operations.create_session)):
    return crud_operations.delete_movie(movie, session)

@app.post("/users", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth0.require_auth())])
def add_user(user: validation.UserAuth,session: Session = Depends(crud_operations.create_session) ):
    print("------")
    print(user)
    print("------")
    crud_operations.add_user(user, session)
    return user

@app.get("/users/{id}")
def get_user(id,session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_user_by_id(id, session)

@app.get("/users/search/{query}", dependencies=[Depends(auth0.require_auth())], response_model=List[validation.UserAdmin])
def search_user(query, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.search_user(query, session)

@app.get("/auth0/users/{auth_id}")
def get_auth_user(auth_id, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_user_by_auth_id(auth_id, session)

@app.post("/screenings", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth0.require_auth())])
def add_screening(screening: validation.ScreeningAdd, session: Session = Depends(crud_operations.create_session)):
    crud_operations.add_screening(screening, session)
    return screening

@app.delete("/screenings", status_code=status.HTTP_200_OK, dependencies=[Depends(auth0.require_auth())])
def delete_screening(screening: validation.ScreeningBase, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.delete_screening(screening, session)

@app.get("/screenings/{id}")
def get_screening(id, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_screening(id, session)

@app.get("/screenings")
def get_screenings_all(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_screenings_all(session)

# Genre

async def get_genres():
        url = "/genre/movie/list"
        params = {}
        result = await getFromTMDB(url, params)
        return result['genres']

def post_genres(genres, session: Session = Depends(crud_operations.create_session)):
    crud_operations.post_genres(genres, session)
    return genres

def get_genres_all(session: Session = Depends(crud_operations.create_session)):
    print(crud_operations.get_genres_all(session))
    
# Booking

@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def add_booking(booking: validation.BookingAdd, session: Session = Depends(crud_operations.create_session), claims: dict = Depends(auth0.require_auth())):
    return crud_operations.add_booking(booking, session, claims.sub)

@app.delete("/bookings", dependencies=[Depends(auth0.require_auth())])
async def delete_booking(booking: validation.BookingRemove, session: Session = Depends(crud_operations.create_session)):
    ret = crud_operations.delete_booking(booking, session)
    booked_seats = crud_operations.get_selected_seats(booking.screening_id, session)
    await manager.broadcast_seats_json(booking.screening_id, {"msg": "Thank you", "booked_seat_ids": booked_seats})
    return ret
    

@app.get("/bookings/{id}", response_model=validation.BookingBase)
def get_booking(id, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_booking(id, session)

@app.post("/pay-booking")
async def pay_booking(data: validation.PaymentRequest, session: Session = Depends(crud_operations.create_session)):
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
    
    
    return crud_operations.confirm_booking(data.booking_id, session)
        



    return transaction_res.json()

# Tickets

@app.get("/my-bookings/", response_model=List[validation.BookingResponse])
def get_user_bookings(session: Session = Depends(crud_operations.create_session), claims: dict = Depends(auth0.require_auth())):
    return crud_operations.get_user_bookings(claims.sub, session)

#EVENT FUNCTIONS
@app.on_event("startup")
async def startup():
    return
    genres = await get_genres()
    post_genres(genres)



# screenings

@app.patch("/screenings", dependencies=[Depends(auth0.require_auth())])
def patch_screening(screening: validation.ScreeningPatchRequest, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.patch_screening(screening, session)

@app.on_event("shutdown")
async def shutdown():
    print("\n\nclosing tmdb_client\n\n")
    await tmdb_client.aclose()
    print("closed tmdb")
    

@app.websocket("/ws/{screening_id}")
async def websocket(websocket: WebSocket, screening_id: int, session: Session = Depends(crud_operations.create_session)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            print("\n\n\n\n", "Thank you", data, "\n\n\n\n")
            booked_seats = crud_operations.get_selected_seats(screening_id, session)
            await manager.broadcast_seats_json(screening_id, {"msg": "Thank you", "booked_seat_ids": booked_seats})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        

    




DARWIN_BASE = "https://darwinbank.duckdns.org/api"



# auth0

async def get_management_token():
    url = f"https://{auth0_domain}/oauth/token"

    payload = {
        "client_id": auth0_client_id,
        "client_secret": auth0_client_secret,
        "audience": f"https://{auth0_domain}/api/v2/",
        "grant_type": "client_credentials",
    }
    headers = {
        'content-type': 'application/x-www-form-urlencoded'
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]


@app.delete("/auth0/users", dependencies=[Depends(auth0.require_auth())])
async def delete_user(user: validation.AuthUserRemove, session: Session = Depends(crud_operations.create_session)):
    async with httpx.AsyncClient() as client:
        token = await get_management_token()
        print("\n\n\n\n\n\n\n")
        print(token)
        print("\n\n\n\n\n\n\n")
        delete_res = await client.delete(
            f"https://{auth0_domain}/api/v2/users/{user.sub}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
    
    return crud_operations.delete_user(user, session)



@app.get("/filters", response_model=validation.Filters)
def get_filters(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_filters(session)
