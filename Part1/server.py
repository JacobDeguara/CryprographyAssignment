from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

import os
from MT19937.RandomClass import Random

ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "password": "secret",
        "disabled": False,
    }
}

fake_drone_db = {
    "drone1": 0,
    "drone2": 0,
    "drone3": 0,
    "drone4": 0,
    "drone5": 0,
    "drone6": 0,
}

fake_access_key_db = list()


# This class handles the Randomiser
class MersenneTwisterRandomiser:
    randomElement: Random

    def __init__(self):
        key: int = int.from_bytes(os.urandom(32), byteorder="little")
        self.randomElement = Random(key)

    def get_next_num(self):
        return self.randomElement.randint(0, 10000)


class Token(BaseModel):
    token: str


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    password: str


class AccessKeyInfo:
    access_key: int
    user: str
    expiration_date: timedelta


MersenneTwisterRandomiserClass = MersenneTwisterRandomiser()

app = FastAPI()


def verify_password(plain_password: str, password: str):
    return plain_password == password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def get_drone_pos(db, drone_name: str):
    if drone_name in db:
        drone_pos: int = db[drone_name]
        return drone_pos


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(expires_delta: timedelta, username: str | None = None):
    # --- Use the PRNG to get session token ---
    access_key_info = MersenneTwisterRandomiserClass.get_next_num()
    fake_access_key_db.append(access_key_info)
    return access_key_info


@app.post("/login", response_model=Token)
async def login_for_access_token(username: str, password: str):
    user = authenticate_user(fake_users_db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        expires_delta=access_token_expires, username=user.username
    )
    return {"token": access_token}


@app.get("/drone/setup", response_model=Token)
async def start_drones(access_token: str):
    for x in fake_drone_db:
        fake_drone_db[x] = MersenneTwisterRandomiserClass.get_next_num()
    return {"token": ":thumbs_up:"}


@app.get("/drone/getpos", response_model=Token)
async def get_drone_position(access_token: str, drone_number: str):
    dronePos = get_drone_pos(fake_drone_db, drone_number)
    if dronePos is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Drone doesnt exist",
        )
    return {"token": dronePos}


@app.get("/logout")
async def logout(access_token: str):
    if access_token in fake_access_key_db:
        fake_access_key_db.remove(access_token)
    return {"token": ":thumbs_up:"}
