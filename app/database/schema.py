from pymongo import MongoClient
from pydantic import BaseModel
from config import CONNECTION_STRING


client = MongoClient(CONNECTION_STRING, tlsAllowInvalidCertificates=True, tlsAllowInvalidHostnames=True)


db = client["mydatabase"]

users_collection = db["users"]
sessions_collection = db["sessions"]


class User(BaseModel):
    id: str
    email: str
    hashed_password: str
    is_active: bool = True


class Session(BaseModel):
    owner_id: int
    file_name: str
    file: bytes
    updated_file: bytes