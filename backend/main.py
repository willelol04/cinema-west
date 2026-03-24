from __future__ import annotations

import os
import httpx
from dotenv import load_dotenv
from typing import List
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from . import crud_operations
from . import validation
from . import websocket
from .models import engine
from .tmdb import tmdb_client, get_from_TMDB

from fastapi import Request, status
from fastapi_plugin.fast_api_client import Auth0FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles



manager = websocket.ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clean_pending_bookings, 'interval', minutes=5)
    scheduler.start()
    yield
    print("\n\nclosing tmdb_client\n\n")
    await tmdb_client.aclose()
    print("closed tmdb")


async def clean_pending_bookings():
    screenings_to_update = crud_operations.clean_pending_bookings()
    print("\n\n\n")
    print(screenings_to_update)
    print("\n\n\n")
    with Session(engine) as session:
        for screening_id in screenings_to_update:
            booked_seat_ids = crud_operations.get_screening(screening_id, session).booked_seat_ids
            await manager.broadcast_screening_json(screening_id, booked_seat_ids)

app = FastAPI(lifespan=lifespan)


roles_string = 'http://localhost:8000/roles'



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


def verify_user(claims: dict = Depends(auth0.require_auth()), session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_user_by_sub(claims.sub, session)

def require_admin(claims: dict = Depends(auth0.require_auth()), session: Session = Depends(crud_operations.create_session)):
    user = crud_operations.get_user_by_sub(claims.sub, session)
    if 'admin' in claims[roles_string] and user.is_admin == True:
        return
    else:
        raise crud_operations.AuthorizationError(user.id)



@app.get("/api/tmdb/movies/search/{query}", dependencies=[Depends(require_admin)])
async def search_movies_on_TMDB(query):
    url = "/search/movie"
    params = {
        "language": "en-US",
        "page": 1,
        "query": query,
        "sort_by":"popularity.desc",
    }
    return await get_from_TMDB(url, params)

@app.get("/api/tmdb/movies/{id}", dependencies=[Depends(require_admin)])
async def get_movie_details(id):
    url = f"/movie/{id}"
    params = {"append_to_response": "releases"}
    return await get_from_TMDB(url, params)



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
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
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

@app.get("/api/movies/id/{id}", response_model=validation.MovieDetails | None)
def get_movie(id: int, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_movie(id, session)

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

@app.post("/api/movies" , dependencies=[Depends(require_admin), ], status_code=status.HTTP_201_CREATED)
async def add_movie(movie: validation.MovieBase, session: Session = Depends(crud_operations.create_session)):
    url = f"/movie/{movie.id}?append_to_response=release_dates"
    params = {"append_to_response": "releases"}
    movie_res = await get_from_TMDB(url, params)
    return crud_operations.add_movie(movie_res, session)

@app.delete("/api/movies", dependencies=[Depends(require_admin)], status_code=204)
def delete_movie(
                movie: validation.MovieBase,
                session: Session = Depends(crud_operations.create_session)
                ):
    crud_operations.delete_movie(movie, session)

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

@app.post("/api/screenings", response_model=List[validation.ScreeningBase], dependencies=[Depends(require_admin)], status_code=status.HTTP_201_CREATED)
def add_screening(screening: validation.ScreeningAdd, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.add_screening(screening, session)

@app.delete("/api/screenings", status_code=204, dependencies=[Depends(require_admin)])
def delete_screening(screening: validation.ScreeningBase, session: Session = Depends(crud_operations.create_session)):
    crud_operations.delete_screening(screening, session)

@app.get("/api/screenings/{id}")
def get_screening(id, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_screening(id, session)

@app.get("/api/screenings")
def get_screenings_all(title : str | None = None, session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_screenings_all(title, session)


@app.post("/api/bookings", response_model=validation.BookingResponse, status_code=status.HTTP_201_CREATED)
async def add_booking(booking: validation.BookingAdd, session: Session = Depends(crud_operations.create_session), user = Depends(verify_user)):
    added_booking = crud_operations.add_booking(user, booking, session)
    booked_seat_ids = crud_operations.get_screening(booking.screening_id, session).booked_seat_ids
    await manager.broadcast_screening_json(booking.screening_id,  booked_seat_ids)
    return added_booking

@app.delete("/api/bookings", status_code=204)
async def delete_booking(booking: validation.BookingRemove, session: Session = Depends(crud_operations.create_session), user = Depends(verify_user)):
    crud_operations.delete_booking(booking, session, user)
    booked_seat_ids = crud_operations.get_screening(booking.screening_id, session).booked_seat_ids
    await manager.broadcast_screening_json(booking.screening_id, booked_seat_ids)

@app.get("/api/bookings/{id}", response_model=validation.BookingResponse)
def get_booking(id, session: Session = Depends(crud_operations.create_session), user = Depends(verify_user)):
    return crud_operations.get_booking(user, id, session)

@app.post("/api/pay-booking", status_code=204)
async def pay_booking(data: validation.PaymentRequest, session: Session = Depends(crud_operations.create_session), user = Depends(verify_user)):
    crud_operations.confirm_booking(user, data.booking_id, session)


@app.websocket("/api/ws/{screening_id}")
async def websocket(websocket: WebSocket, screening_id: int):
    try:
        await manager.connect(websocket, screening_id)
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
            await manager.broadcast_screening_json(screening_id, booked_seat_ids)
    except WebSocketDisconnect:
        manager.disconnect(websocket, screening_id)
        await manager.broadcast_json({"type": "ping", "msg": "left", "screening_id": screening_id})

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

@app.delete("/api/auth0/users", status_code=204)
async def delete_user(user: validation.UserRemove, session: Session = Depends(crud_operations.create_session), db_user = Depends(verify_user)):

    delete_user_obj = crud_operations.get_user_by_sub(user.sub, session)

    if not delete_user_obj:
        raise crud_operations.EntityNotFoundError(f"User with sub {user.sub} not found.")

    if delete_user_obj.is_admin == True:
        raise crud_operations.DatabaseError("Database query Failed. Cannot delete admin from API endpoint.")

    if not(user.sub == db_user.sub or db_user.is_admin):
        raise crud_operations.AuthorizationError(db_user.id)

    async with httpx.AsyncClient() as client:
        token = await get_management_token()
        await client.delete(
            f"https://{auth0_domain}/api/v2/users/{user.sub}",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

    crud_operations.delete_user(user, session)

@app.get("/api/filters", response_model=validation.Filters)
def get_filters(session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_filters(session)

@app.get("/api/me")
def get_current_user(claims: dict = Depends(auth0.require_auth()), session: Session = Depends(crud_operations.create_session)):
    return crud_operations.get_user_by_sub(claims.sub, session)

@app.patch("/api/me/role", status_code=status.HTTP_200_OK)
def patch_current_user_role(user: validation.CurrentUserPatchRole, current_user = Depends(verify_user), session: Session = Depends(crud_operations.create_session)):
    crud_operations.patch_current_user_role(current_user.sub, user.is_admin, session)
    return user

@app.get("/api/me/bookings", response_model=List[validation.BookingResponse])
def get_user_bookings(user = Depends(verify_user), session: Session = Depends(crud_operations.create_session), claims: dict = Depends(auth0.require_auth())):
    return crud_operations.get_user_bookings(user, session)


app.mount("/static", StaticFiles(directory="dist"), name="static")
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    file_path = f"dist/{full_path}"
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return FileResponse("dist/index.html")



