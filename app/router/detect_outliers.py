from fastapi import FastAPI, UploadFile, File, APIRouter
from services.outlier_detection import outlier_detection


router = APIRouter()


@router.post("/outlier_detection")
async def get_outliers(file : UploadFile = File(...)):
    # if not file.filename.endswith('.csv'):
    #     return {"error": "Only CSV files are allowed"}
    with open(file.filename, "wb") as f:
        f.write(file.file.read())
    outlier_detection(file.filename)
    return {"message": "Outliers detected successfully"}