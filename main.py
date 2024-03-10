from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from app.router.api import router
from app.router import sessions
from app.router import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(router)
app.include_router(auth.router)
app.include_router(sessions.router) 


@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/health")
async def health_check():
    return True