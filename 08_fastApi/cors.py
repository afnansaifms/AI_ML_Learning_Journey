from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os 
from dotenv import load_dotenv
from config import settings

app = FastAPI()

load_dotenv()
origins=settings.origins
# origins = [
#     "http://localhost:5173"
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def home():
    return {
        "message": "cors enable API"
    }