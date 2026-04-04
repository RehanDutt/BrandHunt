import os
import sys

# 1. Get the path to the 'event_apollo' folder
# This goes from app/main.py -> app -> event_apollo
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Add that path to Python's "search list" BEFORE importing your modules
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 3. Now Python can see 'routers', 'collecters', and 'engines'
from fastapi import FastAPI
from app.routers import companies # Use the full path if 'routers' is inside 'app'

app = FastAPI(title="Event Apollo")

@app.get("/")
def health_check():
    return {"status": "alive", "message": "Event Apollo backend running"}

app.include_router(companies.router)