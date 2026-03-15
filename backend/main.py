from fastapi import FastAPI, HTTPException, Request, Depends, status, WebSocket
from fastapi_plugin.fast_api_client import Auth0FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import httpx
from datetime import datetime, timezone
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
from fastapi.responses import HTMLResponse, FileResponse
from models import engine
from fastapi.staticfiles import StaticFiles

manager = websocket.ConnectionManager()

scheduler = BackgroundScheduler()
scheduler.add_job(crud_operations.clean_pending_bookings, 'interval', minutes=5)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
app = FastAPI()


roles_string = 'http://localhost:8000/roles'

yes = 999


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

async def verify_user(claims: dict = Depends(auth0.require_auth()), session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_user_by_sub(claims.sub, session)

def require_admin(claims: dict = Depends(auth0.require_auth()), session: Session = Depends(crud_operations.create_session)):
    user = crud_operations.get_user_by_sub(claims.sub, session)
    if 'admin' in claims[roles_string] and user.is_admin == True:
        return
    else:
        raise crud_operations.AuthorizationError(user.id)

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

@app.exception_handler(crud_operations.AuthorizationError)
def integrity_error(request: Request, exc: crud_operations.AuthorizationError):
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
    content={"detail": str(exc), "error_type": "authorization_error"}
    )

@app.exception_handler(crud_operations.BookingAlreadyPaidError)
def integrity_error(request: Request, exc: crud_operations.BookingAlreadyPaidError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
    content={"detail": str(exc), "error_type": "booking_already_paid_error"}
    )

async def getFromTMDB(path, parameters): 
    response = await tmdb_client.get(url=path, params=parameters)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


# GET REQUESTS


@app.get("/api/tmdb/movies/search/{query}", dependencies=[Depends(require_admin)])
async def search_movie(query):
    url = "/search/movie"
    params = { 
              "language": "en-US", 
              "page": 1, 
              "query": query,
              "sort_by":"popularity.desc",
              }
    return await getFromTMDB(url, params)

@app.get("/api/tmdb/movies/{id}", dependencies=[Depends(require_admin)])
async def getMovieDetails(id):
        url = f"/movie/{id}"
        params = {"append_to_response": "releases"}
        return await getFromTMDB(url, params)



@app.get("/api/movies/id/{id}", response_model=validation.MovieDetails | None)
def get_movie(id: int, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_movie(id, session)

"""

@app.get("/api/movie/isadded/{id}")
def movie_is_added(id, session: Session = Depends(crud_operations.create_session)):
    movie = get_movie(id, session)
    return {"message": True if movie else False}

@app.get("/api/movies/upcoming") 
def get_movies_upcoming(session: Session = Depends(crud_operations.create_session)):
    movies = crud_operations.get_movies_upcoming(session)
    print(movies)
    return movies

"""



@app.get("/api/movies", response_model=List[validation.MovieDisplay])
@app.get("/api/admin/movies", response_model=List[validation.MovieDetails])
def get_movies_all(title: str | None = None, genre: int | None = None, rating: str | None = None, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_movies_all(title, genre, rating, session)


@app.get("/api/movies/schedule", response_model=validation.MovieSchedule)
def get_movies_schedule(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_movies_schedule(session)

@app.get("/api/theatres", dependencies=[Depends(require_admin)])
def get_theatres_all(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_theatres_all(session)

# POST-REQUESTS

@app.post("/api/movies", dependencies=[Depends(require_admin), ], status_code=status.HTTP_201_CREATED)
async def add_movie(movie: validation.MovieBase, session: Session = Depends(crud_operations.create_session)):
    url = f"/movie/{movie.id}?append_to_response=release_dates"
    params = {"append_to_response": "releases"}
    movie_res = await getFromTMDB(url, params)
    print(movie_res)
    return crud_operations.add_movie(movie_res, session)

@app.delete("/api/movies", dependencies=[Depends(require_admin)])
def delete_movie(movie: validation.MovieBase,session: Session = Depends(crud_operations.create_session)):
    return crud_operations.delete_movie(movie, session)

@app.post("/api/users", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth0.require_auth())])
def add_user(user: validation.UserAdd, session: Session = Depends(crud_operations.create_session)):
    crud_operations.add_user(user, session)
    return user

@app.get("/api/users/{id}", dependencies=[Depends(auth0.require_auth())])
def get_user(id,session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_user_by_id(id, session)

@app.get("/api/users/search/{query}", dependencies=[Depends(require_admin)], response_model=List[validation.UserAdmin])
def search_user(query, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.search_user(query, session)

@app.get("/api/auth0/users/{sub}", dependencies=[Depends(auth0.require_auth())])
def get_auth_user(sub, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_user_by_sub(sub, session)

@app.post("/api/screenings", dependencies=[Depends(require_admin)], status_code=status.HTTP_201_CREATED)
def add_screening(screening: validation.ScreeningAdd, session: Session = Depends(crud_operations.create_session)):
    crud_operations.add_screening(screening, session)
    return screening

@app.delete("/api/screenings", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def delete_screening(screening: validation.ScreeningBase, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.delete_screening(screening, session)

@app.get("/api/screenings/{id}")
def get_screening(id, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_screening(id, session)

@app.get("/api/screenings")
def get_screenings_all(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_screenings_all(session)

# Genre

async def get_genres():
        url = "/genre/movie/list"
        params = {}
        result = await getFromTMDB(url, params)
        return result['genres']


def get_genres_all(session: Session = Depends(crud_operations.create_session)):
    print(crud_operations.get_genres_all(session))
    
# Booking

@app.post("/api/bookings", status_code=status.HTTP_201_CREATED)
def add_booking(booking: validation.BookingAdd, session: Session = Depends(crud_operations.create_session), user = Depends(verify_user)):
    return crud_operations.add_booking(user, booking, session)

@app.delete("/api/bookings")
async def delete_booking(booking: validation.BookingRemove, session: Session = Depends(crud_operations.create_session), user = Depends(verify_user)):
    ret = crud_operations.delete_booking(booking, session, user)
    booked_seat_ids = crud_operations.get_screening(booking.screening_id, session).booked_seat_ids
    await manager.broadcast_screening_json(booking.screening_id, {"type": "update", "screening_id": booking.screening_id, "booked_seat_ids": booked_seat_ids})
    return ret
    

@app.get("/api/bookings/{id}", response_model=validation.BookingBase)
def get_booking(id, session: Session = Depends(crud_operations.create_session), user = Depends(verify_user)):
    return crud_operations.get_booking(user, id, session)

@app.post("/api/pay-booking")
async def pay_booking(data: validation.PaymentRequest, session: Session = Depends(crud_operations.create_session), user = Depends(verify_user)):
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

    
    
    return crud_operations.confirm_booking(user, data.booking_id, session)
        



    return transaction_res.json()

# Tickets

@app.get("/api/my-bookings", response_model=List[validation.BookingResponse])
def get_user_bookings(user = Depends(verify_user), session: Session = Depends(crud_operations.create_session), claims: dict = Depends(auth0.require_auth())):
    return crud_operations.get_user_bookings(user, session)

#EVENT FUNCTIONS
@app.on_event("startup")
async def startup():
    genres = await get_genres()
    #crud_operations.post_genres(genres)



# screenings

@app.patch("/api/screenings", dependencies=[Depends(require_admin)])
def patch_screening(screening: validation.ScreeningPatchRequest, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.patch_screening(screening, session)

@app.on_event("shutdown")
async def shutdown():
    print("\n\nclosing tmdb_client\n\n")
    await tmdb_client.aclose()
    print("closed tmdb")



@app.websocket("/api/ws/{screening_id}")
async def websocket(websocket: WebSocket, screening_id: int):
    print("\n\n\n\n\n", websocket.path_params, "\n\n\n\n\n")
    try:
        await manager.connect(websocket)
        await manager.broadcast_json({"type": "ping", "msg": "joined", "screening_id": screening_id})
        with Session(engine) as session:
            booked_seat_ids = crud_operations.get_screening(int(websocket.path_params['screening_id']), session).booked_seat_ids
        await manager.send_personal_json({"type": "update", "screening_id": screening_id, "booked_seat_ids": booked_seat_ids}, websocket)

    except Exception as e:
        raise e


    try:
        while True:
            data = await websocket.receive_json()
            print("\n\n\n\n", "Thank you", data, "\n\n\n\n")
            with Session(engine) as session:
                booked_seat_ids = crud_operations.get_screening(int(websocket.path_params['screening_id']), session).booked_seat_ids
            await manager.broadcast_screening_json(screening_id, {"type":"update", "screening_id": screening_id, "booked_seat_ids": booked_seat_ids})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast_json({"type": "ping", "msg": "left", "screening_id": screening_id})


    




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




@app.delete("/api/auth0/users")
async def delete_user(user: validation.UserRemove, session: Session = Depends(crud_operations.create_session), db_user = Depends(verify_user)):

    delete_user_obj = crud_operations.get_user_by_sub(user.sub, session)

    if not delete_user_obj:
        raise crud_operations.EntityNotFoundError(f"User with sub {user.sub} not found.")

    print(delete_user_obj.email)

    if delete_user_obj.is_admin == True:
        raise crud_operations.DatabaseError("Database query Failed. Cannot delete admin from API endpoint.")

    if not(user.sub == db_user.sub or db_user.is_admin):
        raise crud_operations.AuthorizationError(db_user.id)

    async with httpx.AsyncClient() as client:
        try:
            token = await get_management_token()
            await client.delete(
                f"https://{auth0_domain}/api/v2/users/{user.sub}",
                headers={
                    "Authorization": f"Bearer {token}"
                }
            )
        except Exception as e:
            print(e)

    
    return crud_operations.delete_user(user, session)


@app.get("/api/filters", response_model=validation.Filters)
def get_filters(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_filters(session)





app.mount("/static", StaticFiles(directory="dist"), name="static")
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_path = f"dist/{full_path}"
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse("dist/index.html")




