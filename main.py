import os

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
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


@app.get("/")
def read_root():
    return {"message": "use other route to query"}


@app.get("/user/{username}")
def get_user_data():
    return {"message": "use other route to query"}


# create new user
@app.post("/sign-up")
def sign_up(user: UserCreate):
    # TODO: encrypt the password, then save in database
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

    except (psycopg2.Error, Exception):
        # the raised exception will be caught
        if user_exists:
            raise HTTPException(status_code=400, detail="Username already exists.")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the request.",
        )


@app.on_event("startup")
async def startup_event():
    db.connect()
