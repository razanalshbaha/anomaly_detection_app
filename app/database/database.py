from pymongo import MongoClient
from pydantic import BaseModel
from config import CONNECTION_STRING


client = MongoClient(CONNECTION_STRING, tlsAllowInvalidCertificates=True, tlsAllowInvalidHostnames=True)

db = client["mydatabase"]

users_collection = db["users"]
sessions_collection = db["sessions"]
