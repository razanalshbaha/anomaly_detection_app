from fastapi import UploadFile, File, APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from app.services.object import outlier_detection
from app.database.database import sessions_collection
from starlette import status
import pandas as pd
from io import BytesIO
from app.services.router_utils import user_dependency, authenticate_session_name


router = APIRouter()


@router.post("/add_session/")
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
        anomalies, plots= await outlier_detection(file.filename)  
        anomalies_df= pd.DataFrame(anomalies)
        session_data = {
            "owner_id": user['id'],
            "file_name": file_name,
            "file": file_data,
            "updated_file": anomalies
        }

        session_data.update(plots)

        sessions_collection.insert_one(session_data)
        csv_bytes=anomalies_df.to_csv(index=False).encode('utf-8')
        return StreamingResponse(BytesIO(csv_bytes),media_type= "text/csv")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail= "Authentication Failed.",
    )    
