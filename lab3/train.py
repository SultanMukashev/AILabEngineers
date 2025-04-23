import os
import io
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error, r2_score
from dotenv import load_dotenv
import boto3

# load environment
load_dotenv()
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
ACCESS_KEY = os.getenv("MINIO_ROOT_USER")
SECRET_KEY = os.getenv("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.getenv("MINIO_BUCKET")
PREFIX = "ML"
MODEL_PATH = os.getenv("MODEL_PATH", "lab3/model/model.joblib")

# S3 Helper
s3 = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

def read_csv_from_minio(key: str) -> pd.DataFrame:
    """Download CSV object from MinIO and load into DataFrame."""
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=f"{PREFIX}/{key}")
    return pd.read_csv(io.BytesIO(obj["Body"].read()))

# load datasets 
X_train = read_csv_from_minio("X_train.csv")
X_valid = read_csv_from_minio("X_valid.csv")
X_test = read_csv_from_minio("X_test.csv")

y_train = read_csv_from_minio("y_train.csv")
y_valid = read_csv_from_minio("y_valid.csv")
y_test = read_csv_from_minio("y_test.csv")

# load & fit preprocessor
preproc_obj = s3.get_object(Bucket=BUCKET_NAME, Key=f"{PREFIX}/preprocessor.joblib")
preprocessor = joblib.load(io.BytesIO(preproc_obj["Body"].read()))

# fit on train only, then transform all splits
preprocessor.fit(X_train)
X_train = preprocessor.transform(X_train)
X_valid = preprocessor.transform(X_valid)
X_test = preprocessor.transform(X_test)

# train model 
model = RandomForestRegressor(n_estimators=200, max_depth=None, random_state=42, n_jobs=-1)
model.fit(X_train, y_train.values.ravel())

# validation metrics
val_preds = model.predict(X_valid)
val_mae = mean_absolute_error(y_valid, val_preds)
val_mse = mean_squared_error(y_valid, val_preds)
val_r2 = r2_score(y_valid, val_preds)
print(f"[Validation] MAE: {val_mae:,.2f}, MSE: {val_mse:,.2f}, R²: {val_r2:.3f}")

test_preds = model.predict(X_test)
mae = mean_absolute_error(y_test, test_preds)
mse = mean_squared_error(y_test, test_preds)
r2 = r2_score(y_test, test_preds)
print(f"[Test] MAE: {mae:,.2f}, MSE: {mse:,.2f}, R²: {r2:.3f}")

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump({"model": model, "preprocessor": preprocessor}, MODEL_PATH)
print(f"Model and preprocessor saved to {MODEL_PATH}")
