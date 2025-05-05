# etl/train.py

def train_model():
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    import joblib
    from pathlib import Path

    base_path = Path(__file__).resolve().parent.parent
    model_path = base_path / "model" / "random_forest_model.pkl"
    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Загрузка и обработка данных
    df = pd.read_csv(base_path / "raw" / "clean_.csv")
    y = df["income"].apply(lambda x: 1 if x == ">50K" else 0)
    X = pd.get_dummies(df.drop(columns=["income"]))

    # Сохраняем список колонок
    feature_columns = X.columns
    joblib.dump(feature_columns, model_path.parent / "columns.pkl")

    # Тренировка модели
    X_train_full, X_temp, y_train_full, y_temp = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_full, y_train_full)

    # Сохранение модели
    joblib.dump(model, model_path)
