import pandas as pd
import re
import numpy as np

df = pd.read_csv("C:/Users/User/AILabEngineers/task3/data/raw/krisha1.csv")


def check_csv(df: pd.DataFrame) -> pd.DataFrame:
    error_values = ["Не удается получить доступ к сайту", "Страница не найдена"]
    df = df[~df["text"].isin(error_values)].reset_index(drop=True)
    return df

def extract_street(text):
    if pd.isna(text):
        return np.nan
    parts = str(text).split(',')
    return parts[-1].strip() if len(parts) > 1 else np.nan

def extract_rooms(text):
    match = re.search(r"(\d+)-комнатная", str(text))
    return int(match.group(1)) if match else np.nan


def extract_total_area(text):
    match = re.search(r"[\d.]+", str(text))
    return float(match.group()) if match else np.nan


def clean_location(text):
    """Удаляет '\nпоказать на карте' и делит на город + район"""
    if pd.isna(text):
        return pd.Series([None, None])

    # Удаляем \n и всё после него
    cleaned = str(text).split("\n")[0]

    # Делим по запятой
    parts = cleaned.split(",")

    city = parts[0].strip() if len(parts) > 0 else np.nan
    district = parts[1].strip() if len(parts) > 1 else np.nan

    return pd.Series([city, district])


def clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:

    # Проверяем на ошибки со скрапа
    df = check_csv(df)

    # Делим location на city и district
    df[["city", "district"]] = df["location"].apply(clean_location)
    df["city"] = df["city"].str.replace(r"показать.*", "", regex=True).str.strip()
    df["district"] = (
        df["district"].str.replace(r"показать.*", "", regex=True).str.strip()
    )
    df.drop(columns="location", inplace=True)

    # Чистим area от дерьма
    df["area"] = df["area"].apply(extract_total_area)

    # Чистим price от дерьма
    df["rooms"] = df["text"].apply(extract_rooms)
    df.drop(columns="text", inplace=True)
    return df


if __name__ == "__main__":
    df = pd.read_csv("C:/Users/User/AILabEngineers/task3/data/raw/krisha1.csv")
    df_cleaned = clean_pipeline(df)
    df_cleaned.to_csv(
        "C:/Users/User/AILabEngineers/task3/data/processed/krisha_cleaned.csv",
        index=False,
    )
