import os
import threading
import joblib
import pandas as pd
import datetime as _dt
from sklearn.ensemble import RandomForestRegressor

DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "model.joblib")
MODEL_PATH = os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH)
_lock = threading.Lock()

_bundle = joblib.load(MODEL_PATH)
_model: RandomForestRegressor = _bundle["model"]
_preprocessor = _bundle["preprocessor"]

def _derive_features(df: pd.DataFrame) -> pd.DataFrame:
    """Enrich incoming dataframe with engineered features expected by the model.
    Ensures all columns used during training exist with correct dtypes.
    """
    df = df.copy()

    # numeric conversions
    for col in ["year", "mileage", "engine_volume_liters"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # age
    if "year" in df.columns:
        df["age"] = _dt.datetime.now().year - df["year"]

    # low_mileage flag (threshold 5 000)
    if "mileage" in df.columns:
        df["low_mileage"] = (df["mileage"] < 5_000).astype(int)
    else:
        df["low_mileage"] = 0

    # electric flag (engine volume missing or 0)
    elec_cond = (
        df.get("engine_volume_liters").isna()
        if "engine_volume_liters" in df.columns
        else pd.Series([True] * len(df))
    ) | (df.get("engine_volume_liters", 0) == 0)
    df["is_electric"] = elec_cond.astype(int)

    # ensure numeric engine_volume_liters exists and filled
    if "engine_volume_liters" not in df.columns:
        df["engine_volume_liters"] = 0
    df["engine_volume_liters"] = df["engine_volume_liters"].fillna(0)

    # make sure optional categorical columns exist
    optional_cats = [
        "drive_type",
        "transmission",
        "body_style",
        "color",
        "city",
    ]
    for col in optional_cats:
        if col not in df.columns:
            df[col] = pd.NA

    return df

_X_train_cache: pd.DataFrame | None = None
_y_train_cache: pd.Series | None = None

def _ensure_cache(df: pd.DataFrame, y):
    """Append new data to in‑memory train cache."""
    global _X_train_cache, _y_train_cache
    if _X_train_cache is None:
        _X_train_cache = df.copy()
        _y_train_cache = y.copy()
    else:
        _X_train_cache = pd.concat([_X_train_cache, df], ignore_index=True)
        _y_train_cache = pd.concat([_y_train_cache, y], ignore_index=True)


def predict(df: pd.DataFrame) -> float:
    with _lock:
        df = _derive_features(df)
        X = _preprocessor.transform(df)
        return float(_model.predict(X)[0])


def retrain(df: pd.DataFrame, y_col: str = "price") -> int:
    with _lock:
        y = df.pop(y_col)
        df = _derive_features(df)
        _ensure_cache(df, y)

        _preprocessor.fit(_X_train_cache)
        X_proc = _preprocessor.transform(_X_train_cache)

        global _model
        _model = RandomForestRegressor(n_estimators=300, random_state=42, n_jobs=-1)
        _model.fit(X_proc, _y_train_cache.values.ravel())

        joblib.dump({"model": _model, "preprocessor": _preprocessor}, MODEL_PATH)
        return len(_y_train_cache)
