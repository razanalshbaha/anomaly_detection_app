from fastapi import UploadFile, File, APIRouter, HTTPException
from app.services.object import outlier_detection
from app.database.database import sessions_collection
from starlette import status
import pandas as pd
from io import BytesIO
from app.services.router_utils import user_dependency, authenticate_session_name
from app.blob_storage.blob_storage import blob_service_client, container_name
import uuid
import os


router = APIRouter()
 


@router.post("/add_session")
async def create_session(user: user_dependency, file : UploadFile = File(...)):

    if user is None: 
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED
        )
    with open(file.filename, "wb") as f:
       f.write(file.file.read())

    df = pd.read_csv(file.filename)
    #file_data = df.to_dict(orient='records')
    file_name= authenticate_session_name(file.filename, user['id'])
    if file_name:
        file_name= file.filename
        anomalies, plots= await outlier_detection(file.filename)  
        anomalies_df= pd.DataFrame(anomalies)

        plots_list=[]

        csv_buffer = BytesIO()
        anomalies_df.to_csv(csv_buffer, index=False, encoding='utf-8')
        csv_buffer.seek(0) 
        blob_name = str(uuid.uuid4()) + ".csv"


        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        file_id= str(blob_client.blob_name)
        blob_client.upload_blob(csv_buffer.read(), overwrite=True)
        csv_buffer.close()
        
        for plot in plots:
            blob_obj= blob_service_client.get_blob_client(container=container_name, blob=str(uuid.uuid4()))
            plots_list.append(blob_obj.blob_name)
            blob_obj.upload_blob(plots[plot])
        
        session_data = {
            "owner_id": user['id'],
            "file_name": file_name,
            "file_id": file_id,
            "plots_list": plots_list
        }

        sessions_collection.insert_one(session_data)
        csv_bytes=anomalies_df.to_csv(index=False).encode('utf-8')
        os.remove(file.filename)
        return {"file_id": file_id, "plots": plots_list}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail= "Authentication Failed.",
    )    
