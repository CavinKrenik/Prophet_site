from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import pandas as pd
from datetime import datetime

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

@app.get("/logs")
def read_latest_logs():
    today = datetime.now().strftime("%Y-%m-%d")
    file_path = os.path.join(LOG_FOLDER, f"signals_{today}.csv")
    if not os.path.exists(file_path):
        return JSONResponse(content={"error": "Log file not found."}, status_code=404)
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

@app.post("/upload")
def upload_log(file: UploadFile = File(...)):
    contents = file.file.read()
    file_path = os.path.join(LOG_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    return {"filename": file.filename, "message": "File uploaded successfully."}