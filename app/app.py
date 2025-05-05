from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pathlib import Path

app = FastAPI()

# Загрузка модели
base_path = Path(__file__).resolve().parent.parent
model = joblib.load(base_path / "model" / "random_forest_model.pkl")

# Загрузка колонок
columns = joblib.load(base_path / "model" / "columns.pkl")

@app.post("/predict")
def predict(data: PersonInput):
    df = pd.DataFrame([data.dict()])
    df = pd.get_dummies(df)

    # 👉 Добавим недостающие колонки и порядок:
    for col in columns:
        if col not in df.columns:
            df[col] = 0
    df = df[columns]  # порядок как при обучении

    prediction = model.predict(df)[0]
    return {"prediction": int(prediction)}


 