import os
import pandas as pd
import datetime
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# load raw data and drop unused columns

def load_data(input_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    df = df.drop(columns=['url', 'parsed_at'], errors='ignore')

    if 'brand' in df.columns:
        split = df['brand'].str.split(' ', n=1, expand=True)
        df['brand'] = split[0]
        df['model'] = split[1] 

    df['model'] = df['model'].fillna('unknown_model')
    return df

# create age

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if 'year' in df.columns:
        df['age'] = datetime.datetime.now().year - df['year']
    return df

# null handling & flag features

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # mileage handling
    if 'mileage' in df.columns:
        df['mileage'] = pd.to_numeric(df['mileage'], errors='coerce')
        df['mileage'] = df['mileage'].fillna(df.groupby('year')['mileage'].transform('median'))
        df['mileage'] = df['mileage'].fillna(df['mileage'].median())
        low_thr = float(os.getenv('LOW_MILEAGE_THRESHOLD', 5000))
        df['low_mileage'] = (df['mileage'] < low_thr).astype(int)

    # engine volume / electric flag
    if 'engine_volume_liters' in df.columns:
        df['engine_volume_liters'] = pd.to_numeric(df['engine_volume_liters'], errors='coerce')
        drive = df.get('drive_type', pd.Series(dtype=str)).fillna('').str.lower()
        trans = df.get('transmission', pd.Series(dtype=str)).fillna('').str.lower()
        df['is_electric'] = ((df['engine_volume_liters'].isna()) | (drive == 'electric') | (trans == 'electric')).astype(int)
        df['engine_volume_liters'] = df['engine_volume_liters'].fillna(0)

    # body_style imputation
    if 'body_style' in df.columns:
        grp = df.groupby(['brand', 'model'])['body_style']
        df['body_style'] = df['body_style'].fillna(grp.transform(lambda x: x.mode().iloc[0] if len(x.mode())==1 else pd.NA))
        if not df['body_style'].mode().empty:
            df['body_style'] = df['body_style'].fillna(df['body_style'].mode().iloc[0])

    # color bucketing
    if 'color' in df.columns:
        top_n = int(os.getenv('TOP_COLOR_COUNT', 10))
        top_colors = df['color'].value_counts().nlargest(top_n).index
        df['color'] = df['color'].where(df['color'].isin(top_colors), 'other').fillna('other')

    return df

# prepare data & pipeline

def prepare_data(df: pd.DataFrame, target_col: str):
    X = df.drop(columns=[target_col])
    y = df[target_col]
    num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

    preprocessor = ColumnTransformer([
        ('num', Pipeline([('scaler', StandardScaler())]), num_cols),
        ('cat', Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), cat_cols)
    ])
    return X, y, preprocessor

# train/test split

def split_data(X, y):
    train_size = float(os.getenv('TRAIN_SIZE', 0.7))
    valid_size = float(os.getenv('VALID_SIZE', 0.1))
    if train_size + valid_size >= 1.0:
        raise ValueError('TRAIN_SIZE + VALID_SIZE must be < 1.0')

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, train_size=train_size, random_state=42)
    valid_relative_size = valid_size / (1.0 - train_size)
    X_valid, X_test, y_valid, y_test = train_test_split(X_temp, y_temp, train_size=valid_relative_size, random_state=42)
    return X_train, X_valid, X_test, y_train, y_valid, y_test

# Save artifacts

def save_artifacts(preproc, X_train, X_valid, X_test, y_train, y_valid, y_test, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    X_train.to_csv(os.path.join(out_dir, 'X_train.csv'), index=False)
    X_valid.to_csv(os.path.join(out_dir, 'X_valid.csv'), index=False)
    X_test.to_csv(os.path.join(out_dir, 'X_test.csv'), index=False)
    y_train.to_frame().to_csv(os.path.join(out_dir, 'y_train.csv'), index=False)
    y_valid.to_frame().to_csv(os.path.join(out_dir, 'y_valid.csv'), index=False)
    y_test.to_frame().to_csv(os.path.join(out_dir, 'y_test.csv'), index=False)
    joblib.dump(preproc, os.path.join(out_dir, 'preprocessor.joblib'))
 
if __name__ == '__main__':
    default_raw = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'kolesa_almaty_raw.csv')
    default_out = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

    RAW_DATA_PATH = os.getenv('RAW_DATA_PATH', default_raw)
    TARGET_COL = os.getenv('TARGET_COL', 'price')
    OUTPUT_DIR = os.getenv('OUTPUT_DIR', default_out)

    print(f"[Transform] Load {RAW_DATA_PATH}")
    df = preprocess_data(engineer_features(load_data(RAW_DATA_PATH)))
    X, y, preproc = prepare_data(df, TARGET_COL)
    X_train, X_valid, X_test, y_train, y_valid, y_test = split_data(X, y)
    save_artifacts(preproc, X_train, X_valid, X_test, y_train, y_valid, y_test, OUTPUT_DIR)
    print(f"[Transform] Done. Artifacts in {OUTPUT_DIR}")
