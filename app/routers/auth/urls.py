'''
FstAPI Security - First Steps
https://fastapi.tiangolo.com/tutorial/security/first-steps/
'''
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

router = APIRouter()
'''
Using a relative URL is important to make sure your application
keeps working even in an advanced use case like Behind a Proxy
The oauth2_scheme variable is an instance of OAuth2PasswordBearer,
but it is also a "callable"
It could be called as:
    oauth2_scheme(some, parameters)
So, it can be used with Depends.
FastAPI will know that it can use this dependency to define a 
"security scheme" in the OpenAPI schema (and the automatic API docs)
'''
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

'''
First install python-multipart.
E.g. pip install python-multipart.
This is because OAuth2 uses "form data" for sending the username and password.
'''


@router.post("/token")
async def token(form_data:  OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username")

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)

    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    return {"access_token": user.username, "token_type": "bearer"}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


'''
https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
'''


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


def fake_hash_password(password: str):
    return "fakehashed" + password
