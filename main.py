# FastAPI backend for PepeProphet

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import os
from datetime import datetime

app = FastAPI()

# CORS Middleware for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth Dependency
API_KEY = "pepe-secret-token"
def verify_token(token: str = Form(...)):
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Upload training data
data_dir = "./uploaded_logs"
os.makedirs(data_dir, exist_ok=True)

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...), token: str = Depends(verify_token)):
    contents = await file.read()
    filepath = os.path.join(data_dir, file.filename)
    with open(filepath, "wb") as f:
        f.write(contents)
    return {"message": "File uploaded successfully", "filename": file.filename}

# Get signal log (latest or by date)
@app.get("/logs")
def get_logs(date: str = None):
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    file_path = f"logs/signals_{date}.csv"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Log not found")
    df = pd.read_csv(file_path)
    return df.tail(50).to_dict(orient="records")

# Trigger notification (placeholder)
@app.post("/notify")
def notify(event: str = Form(...), token: str = Depends(verify_token)):
    print(f"[Notification] Triggered: {event}")
    return {"message": f"Notification '{event}' triggered"}

# Example analytics summary
@app.get("/analytics")
def analytics_summary():
    return {
        "accuracy": [72, 78, 83, 79, 85],
        "confidence": {"MIND": 87, "WEPE": 81, "BTC": 74, "SOL": 68, "XRP": 65}
    }
