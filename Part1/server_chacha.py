from datetime import datetime, timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

import os
from MT19937.RandomClass import Random
import json
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "user1": {
        "username": "USER",
        "full_name": "First_name Second_name",
        "email": "example@example.com",
        "password": "secret",
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
class AccessCode:
    randomElement: Random
    key2: bytes

    def __init__(self):
        key: int = int.from_bytes(os.urandom(32), byteorder="little")
        self.key2 = get_random_bytes(32)
        self.randomElement = Random(key)

    def get_next_num(self):
        return self.randomElement.randint(0, 2**32)

    def get_encoding(self):
        access_key_info = self.get_next_num()
        plainkey = str(access_key_info).encode("utf-8")
        cipher = ChaCha20.new(key=self.key2)
        ciphertext = cipher.encrypt(plainkey)

        nonce = b64encode(cipher.nonce).decode("utf-8")
        ct = b64encode(ciphertext).decode("utf-8")
        return nonce, ct, access_key_info

    def get_decode(self, nonce, ct):
        try:
            nn = b64decode(nonce)
            ciphertext = b64decode(ct)
            cipher = ChaCha20.new(key=self.key2, nonce=nn)
            plaintext = cipher.decrypt(ciphertext)
            return plaintext
        except:
            return None


class Token(BaseModel):
    Token: str


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    password: str


class AccessKeyInfo:
    access_key: int
    user: str
    expiration_date: timedelta


AccesscodeGen = AccessCode()

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
    nonce, ct, access_key_info = AccesscodeGen.get_encoding()

    fake_access_key_db.append(tuple((nonce, access_key_info)))
    return ct


def confirm_password(access_token):
    found = False
    for nonce, access_code in fake_access_key_db:
        ret = None
        ret = AccesscodeGen.get_decode(nonce, access_token)
        if not ret == None:
            try:
                ret_int = int(ret.decode("utf-8"))
                if ret_int == access_code:
                    found = True
                    break
            except:
                found = False
    return found


@app.get("/login", response_model=Token)
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
    return {"Token": access_token}


@app.get("/drone/setup")
async def start_drones(access_token: str):
    found = confirm_password(access_token)

    if not found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have access to this command",
            headers={"WWW-Authenticate": "Bearer"},
        )

    for x in fake_drone_db:
        fake_drone_db[x] = AccesscodeGen.get_next_num()
    return {"Response": "successful"}


@app.get("/drone/getpos")
async def get_drone_position(drone_name: str):
    dronePos = get_drone_pos(fake_drone_db, drone_name)
    if dronePos is None:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Drone doesnt exist",
        )
    return {"Drone_position": dronePos}


@app.get("/drone/getalldronenames")
async def get_drones():
    return {"Drone_names": list(fake_drone_db.keys())}


@app.get("/drone/getalldronepositions")
async def get_drones():
    return {"Drone_positions": list(fake_drone_db.values())}


@app.get("/logout")
async def logout(access_token: str):
    for nonce, access_code in fake_access_key_db:
        ret = None
        ret = AccesscodeGen.get_decode(nonce, access_token)
        if not ret == None:
            try:
                ret_int = int(ret.decode("utf-8"))
                if ret_int == access_code:
                    fake_access_key_db.remove(tuple((nonce, access_code)))
                    return {"Response": "successful"}
            except:
                ret = None

    raise HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail="This is not an access token that is avaiable",
        headers={"WWW-Authenticate": "Bearer"},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
