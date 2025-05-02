import pandas as pd
import numpy as np
import os
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

df = pd.DataFrame(
    columns=[
        "price",
        "text",
        "area",
        "flat_toilets",
        "balcony",
        "current_floors",
        "total_floors",
        "ceiling",
        "dorm",
        "mortgage",
        "year",
        "type_of_house",
        "condition",
        "repair_status",
        "type_of_floor",
        "location",
    ]
)

count = 0

with open(
    "C:/Users/User/AILabEngineers/task3/links_krisha.txt", "r", encoding="utf-8"
) as f:
    links = [line.strip() for line in f if line.strip()]

# Настройки Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

for link in links:
    url = "https://krisha.kz/" + link
    soup = None

    for attempt in range(3):
        try:
            driver.get(url)
            time.sleep(4)  # имитация ожидания загрузки страницы
            soup = BeautifulSoup(driver.page_source, "html.parser")
            break
        except (TimeoutException, WebDriverException):
            print(f"[!] Retry {attempt + 1}/3 for {url}")
            time.sleep(3)

    if soup is None:
        print(f"[❌] Skipping {url} after 3 failed attempts")
        continue

    def extract(selector, attr=None, default=np.nan):
        try:
            element = soup.select_one(selector)
            if attr:
                return element[attr].strip()
            return element.text.strip()
        except:
            return default

    def extract_data_name(data_name):
        try:
            el = soup.find("div", {"data-name": data_name})
            return el.find("div", class_="offer__advert-short-info").text.strip()
        except:
            return np.nan

    try:
        price = extract("div.offer__price")
        clean_price = "".join(filter(str.isdigit, price))
    except:
        clean_price = np.nan

    text = extract("h1")
    area_text = extract_data_name("live.square")
    if isinstance(area_text, str) and "Площадь кухни" in area_text:
        area_text = area_text.split(",")[0].strip()

    flat_toilet_text = extract_data_name("flat.toilet")
    balcony_text = extract_data_name("flat.balcony")

    try:
        floor_text = extract_data_name("flat.floor")
        if " из " in floor_text:
            current_floor, total_floors = map(int, floor_text.split(" из ")[0:2])
        else:
            current_floor, total_floors = np.nan, np.nan
    except:
        current_floor, total_floors = np.nan, np.nan

    try:
        ceiling_el = soup.find("dt", {"data-name": "ceiling"})
        ceiling_val = ceiling_el.find_next_sibling("dd").text.strip()
        match = re.search(r"\d+(\.\d+)?", ceiling_val)
        clean_ceiling = float(match.group()) if match else np.nan
    except:
        clean_ceiling = np.nan

    try:
        mortgage_text = soup.find(
            "div", class_="offer__parameters-mortgaged"
        ).text.strip()
    except:
        mortgage_text = np.nan

    year_text = extract_data_name("house.year")

    try:
        type_home_el = soup.find("div", {"data-name": "flat.building"})
        type_home_text = (
            type_home_el.find("div", class_="offer__advert-short-info")
            .text.strip()
            .split("\n")[0]
        )
    except:
        type_home_text = np.nan

    try:
        dorm_el = soup.find("dt", {"data-name": "flat.priv_dorm"})
        dorm_text = dorm_el.find_next_sibling("dd").text.strip() if dorm_el else np.nan
    except:
        dorm_text = np.nan

    condition_text = extract_data_name("flat.renovation")

    try:
        repair_status_el = soup.find("dt", {"data-name": "live.furniture"})
        repair_status_text = (
            repair_status_el.find_next_sibling("dd").text.strip()
            if repair_status_el
            else np.nan
        )
    except:
        repair_status_text = np.nan

    try:
        floor_type_el = soup.find("dt", {"data-name": "flat.flooring"})
        type_of_floor_text = (
            floor_type_el.find_next_sibling("dd").text.strip()
            if floor_type_el
            else np.nan
        )
    except:
        type_of_floor_text = np.nan

    location = extract("div.offer__location")

    row = [
        clean_price,
        text,
        area_text,
        flat_toilet_text,
        balcony_text,
        current_floor,
        total_floors,
        clean_ceiling,
        dorm_text,
        mortgage_text,
        year_text,
        type_home_text,
        condition_text,
        repair_status_text,
        type_of_floor_text,
        location,
    ]

    print(row)
    df.loc[len(df)] = row

    df.tail(1).to_csv(
        "krisha_all_data.csv",
        mode="a",
        index=False,
        header=not os.path.exists("krisha_all_data.csv"),
        encoding="utf-8-sig",
    )
    count += 1
    print(f"[✓] Scraped {count}/{len(links)}")

driver.quit()
