import os
from datetime import date, datetime
from typing import Union

import jwt
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import Database

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# establishing the connection
db_config = {
    "host": "127.0.0.1",
    "port": "5432",
    "database": "test",
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
}

db = Database(**db_config)


# User model for request body validation
class UserCreate(BaseModel):
    username: str
    password: str


# User model for request body validation
class UserLogin(BaseModel):
    username: str
    password: str


# User model
class User(BaseModel):
    username: str
    password: str
    birthday: date
    created_time: datetime
    last_login: datetime


class UserUpdate(BaseModel):
    password: Union[str, None] = None
    birthday: Union[str, None] = None


@app.get("/")
def read_root():
    return {"message": "use other route to query"}


# create new user
@app.post("/sign-up")
def sign_up(user: UserCreate):
    user_exists = False
    try:
        # Check if the username already exists
        result = db.execute_query_one(
            "SELECT COUNT(*) FROM public.user WHERE username = %s;", user.username
        )
        if result[0] > 0:
            user_exists = True
            raise HTTPException(status_code=400, detail="Username already exists.")

        # Insert the user into the database
        db.execute_query_insert(
            "INSERT INTO public.user (username, password) VALUES (%s, %s);",
            user.username,
            user.password,
        )

        return {"message": "User created successfully."}

    except (psycopg2.Error, Exception) as e:
        # the raised exception will be caught
        print(e)
        if user_exists:
            raise HTTPException(status_code=400, detail="Username already exists.")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the request.",
        )


# Login endpoint
@app.post("/login")
def login(user: UserLogin):
    # Check if the username and password match
    result = db.execute_query_one(
        "SELECT COUNT(*) FROM public.user WHERE username = %s AND password = %s;",
        user.username,
        user.password,
    )
    # not exist
    if result[0] == 0:
        raise HTTPException(status_code=401, detail="Invalid username or password.")

    # update last_login
    query = "UPDATE public.user SET last_login=%s WHERE username=%s"
    db.execute_query_insert(query, datetime.utcnow(), user.username)

    encoded_jwt = jwt.encode(
        {"username": user.username}, os.environ.get("JWT_SECRET"), algorithm="HS256"
    )
    return {"jwt": encoded_jwt}


# Route to get user data
@app.get("/user/{username}")
def get_user(username: str, token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided.")

    try:
        # Verify and decode the JWT
        decoded_token = jwt.decode(
            token, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
        jwt_username = decoded_token.get("username")
        if not jwt_username or jwt_username != username:
            raise HTTPException(status_code=401, detail="Invalid JWT.")

        # Retrieve user data from the database
        query = "SELECT username,password,birthday,created_time,last_login FROM public.user WHERE username = %s;"
        result = db.execute_query_one(query, username)
        if not result:
            raise HTTPException(status_code=404, detail="User not found.")

        fields = ["username", "password", "birthday", "created_time", "last_login"]

        user_data = {}
        for index, field in enumerate(fields):
            user_data[field] = result[index]

        return user_data
    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired JWT.")
    except Exception as exc:
        raise exc  # raise again


@app.put("/user/{username}")
def update_user(username: str, user: UserUpdate, token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=401, detail="Token not provided.")

    try:
        # Verify and decode the JWT
        decoded_token = jwt.decode(
            token, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
        jwt_username = decoded_token.get("username")

        if not jwt_username or jwt_username != username:
            raise HTTPException(status_code=401, detail="Invalid JWT.")

            # Retrieve user data from the database
        query = "SELECT password,birthday FROM public.user WHERE username = %s;"
        user_data = db.execute_query_one(query, username)

        if user_data is None:
            raise HTTPException(status_code=404, detail="User not found.")

        # Update user data based on the fields that are passed in
        password = user.password if user.password is not None else user_data[0]
        birthday = user.birthday if user.birthday is not None else user_data[1]

        # Update user data in the database
        update_query = (
            "UPDATE public.user SET password=%s, birthday=%s WHERE username=%s;"
        )
        # NOTE: use execute then commit to UPDATE
        db.execute_query_insert(update_query, password, birthday, username)

        # Return success message
        return {"message": "User data updated successfully."}

    except jwt.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid JWT.")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired JWT.")
    except Exception as exc:
        # Reraise any exception that is not related to JWT
        raise exc


@app.on_event("startup")
async def startup_event():
    db.connect()
