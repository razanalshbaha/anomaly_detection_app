from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.database.database import users_collection
from config import ALGORITHM, SECRET_KEY
from typing import Annotated
from app.database.database import sessions_collection
import re
from pydantic import BaseModel

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Response(BaseModel):
    message: str

def authenticate_user(email: str, password: str):
    user = users_collection.find_one({"email": email})
    if not user:
        return None
    if not bcrypt_context.verify(password, user['hashed_password']):
        return None
    return user


def create_access_token(email: str, user_id: str, expires_delta: timedelta):
    encode = {"sub": email, "id": user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: str = payload.get("id")
        if email is None or user_id is None:
            print("")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        user = users_collection.find_one({"email": email})
        # print(user)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found.",
            )
        return {"email": email, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


def authenticate_session_name(Session_name: str, id: int):
    session = sessions_collection.find_one({"owner_id": id, "id": Session_name})
    if not session:
        return True
    return False

def get_all_sessions(id: int):
    # somne fields are of type base64, so we need to send them to the client as bytes
    # import base64
    # s = []
    sessions = sessions_collection.find({"owner_id": id})
    # for session in sessions:
    #     session["plot_LineId"] = base64.b64encode(session["plot_LineId"])
    #     session["plot_Logrecord"] = base64.b64encode(session["plot_Logrecord"])
    #     session["plot_Date"] = base64.b64encode(session["plot_Date"])
    #     session["plot_Pid"] = base64.b64encode(session["plot_Pid"])
    #     session["plot_Level"] = base64.b64encode(session["plot_Level"])
    #     session["plot_Component"] = base64.b64encode(session["plot_Component"])
    #     session["plot_EventId"] = base64.b64encode(session["plot_EventId"])
    #     session["plot_EventTemplate"] = base64.b64encode(session["plot_EventTemplate"])

        # s.append(session)
    sessions_list = list(sessions)
    return sessions_list


def authenticate_user_email(email: str):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(pattern, email):
        return True
    else:
        return False
    

user_dependency = Annotated[dict, Depends(get_current_user)]