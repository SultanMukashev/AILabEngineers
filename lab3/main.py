from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import pandas as pd

import inference
from models import CarFeatures, PredictResponse, RetrainItem, RetrainResponse

app = FastAPI(title="Car Price Predictor", version="1.0")

# set up templates directory
templates = Jinja2Templates(directory="templates")


@app.post("/predict", response_model=PredictResponse)
async def predict_price(item: CarFeatures):
    try:
        payload = item.model_dump(exclude_none=True)
        df = pd.DataFrame([payload])
        price = inference.predict(df)
        return PredictResponse(price=price)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/retrain", response_model=RetrainResponse)
async def retrain_model(items: List[RetrainItem]):
    if not items:
        raise HTTPException(status_code=400, detail="No data provided")
    try:
        payloads = [i.model_dump(exclude_none=True) for i in items]
        df = pd.DataFrame(payloads)
        new_size = inference.retrain(df, y_col="price")
        return RetrainResponse(message="Model retrained", new_train_size=new_size)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # render index.html template
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict_form", response_class=HTMLResponse)
async def predict_form(
    request: Request,
    brand: str = Form(...),
    car_model: str = Form(...),
    year: int = Form(...),
    mileage: float = Form(...),
    city: str = Form(...),
    engine_volume_liters: float = Form(...),
    body_style: str = Form(...),
    color: str = Form(...),
    transmission: str = Form(...),
    drive_type: str = Form(...),
):
    try:
        # map alias car_model to model for inference
        payload = {
            "brand": brand,
            "model": car_model,
            "year": year,
            "mileage": mileage,
            "city": city,
            "engine_volume_liters": engine_volume_liters,
            "body_style": body_style,
            "color": color,
            "transmission": transmission,
            "drive_type": drive_type,
        }
        df = pd.DataFrame([payload])
        price = inference.predict(df)
        # render result.html template with price
        return templates.TemplateResponse(
            "result.html",
            {"request": request, "price": f"{price:,.0f} ₸"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
