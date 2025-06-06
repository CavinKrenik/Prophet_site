# live_api.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

class MarketData(BaseModel):
    price: float
    volume: float
    sentiment: float
    score: float

# Load trained model
model = joblib.load("model.pkl")

@app.get("/")
def root():
    return {"status": "Live Model API is running"}

@app.post("/predict")
def predict(data: MarketData):
    features = [[
        data.price,
        data.volume,
        data.sentiment,
        data.score
    ]]
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0].max()
    return {
        "prediction": prediction,
        "confidence": round(probability * 100, 2)
    }
