import os
from datetime import date, datetime

import jwt
import psycopg2
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel

from db import Database

load_dotenv()

app = FastAPI()

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
    last_login: date


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
    login_is_invalid = False
    # TODO: update user's last_login
    try:
        # Check if the username and password match
        result = db.execute_query_one(
            "SELECT COUNT(*) FROM public.user WHERE username = %s AND password = %s;",
            user.username,
            user.password,
        )
        # not exist
        if result[0] == 0:
            login_is_invalid = True
            raise HTTPException(status_code=401, detail="Invalid username or password.")

        encoded_jwt = jwt.encode(
            {"username": user.username}, os.environ.get("JWT_SECRET"), algorithm="HS256"
        )
        return {"jwt": encoded_jwt}

    except (psycopg2.Error, Exception) as e:
        if login_is_invalid:
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        raise HTTPException(
            status_code=500, detail="An error occurred while processing the request."
        )


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
    except (psycopg2.Error, Exception) as error:
        if error.status_code == 401:
            raise HTTPException(status_code=401, detail="Invalid JWT.")
        elif error.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found.")
        else:
            raise HTTPException(
                status_code=500,
                detail="An error occurred while processing the request.",
            )


@app.on_event("startup")
async def startup_event():
    db.connect()
