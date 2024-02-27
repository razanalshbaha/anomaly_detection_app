from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.router.detect_outliers import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/health")
async def health_check():
    return True
    #return {"status": "ok"}