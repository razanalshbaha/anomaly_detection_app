from fastapi import FastAPI, UploadFile, File, APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from app.services.object import outlier_detection
from app.schema.schema import sessions_collection
from .auth import get_current_user
from typing import Annotated
from starlette import status
import pandas as pd
from io import BytesIO


router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]

def authenticate_session_name(Session_name: str, id: int):
    session = sessions_collection.find_one({"owner_id": id, "id": Session_name})
    if not session:
        return True
    return False

@router.get("/read_all")
async def read_all(user: user_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed.",
        )
    sessions_cursor = sessions_collection.find({"owner_id": user['id']}, {"_id": 0})
    sessions = [session for session in sessions_cursor]
    return sessions 




@router.post("/addSession/")
async def create_session(user: user_dependency, file : UploadFile = File(...)):
    if user is None: 
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    with open(file.filename, "wb") as f:
        f.write(file.file.read())

    df = pd.read_csv(file.filename)
    file_data = df.to_dict(orient='records')
    file_name= authenticate_session_name(file.filename, user['id'])
    if file_name:
        file_name= file.filename
        anomalies= outlier_detection(file.filename)  
        anomalies_df= pd.DataFrame(anomalies)
        session_data = {
            "owner_id": user['id'],
            "file_name": file_name,
            "file": file_data,
            "updated_file": anomalies
        }
        sessions_collection.insert_one(session_data)
        csv_bytes=anomalies_df.to_csv(index=False).encode('utf-8')
        return StreamingResponse(BytesIO(csv_bytes),media_type= "text/csv")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail= "Authentication Failed.",
    )    

