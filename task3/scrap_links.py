import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

MAX_LINKS = 25000

existing_links = set()
if os.path.exists("C:/Users/User/AILabEngineers/task3/links_krisha.txt"):
    with open(
        "C:/Users/User/AILabEngineers/task3/links_krisha.txt", "r", encoding="utf-8"
    ) as f:
        existing_links = set(line.strip() for line in f)

driver = webdriver.Chrome()
url = "https://krisha.kz/prodazha/kvartiry"
driver.get(url)

new_links = []

try:
    while True:
        if len(existing_links) >= MAX_LINKS:
            print(f"🚫 Достигнут лимит {MAX_LINKS} ссылок. Остановка.")
            break

        soup = BeautifulSoup(driver.page_source, "html.parser")
        a_elements = soup.find_all("a", class_="a-card__title")

        for a_element in a_elements:
            link = a_element.get("href")
            if link and link not in existing_links:
                new_links.append(link)
                existing_links.add(link)
                if len(existing_links) >= MAX_LINKS:
                    print(
                        f"🚫 Достигнут лимит {MAX_LINKS} ссылок во время сбора. Остановка."
                    )
                    break

        print(f"🟢 Новых ссылок: {len(new_links)} (всего: {len(existing_links)})")

        if len(existing_links) >= MAX_LINKS:
            break

        try:
            next_button = driver.find_element(By.LINK_TEXT, "Дальше")
            next_button.click()
            time.sleep(2)
        except:
            print("❌ Кнопка 'Дальше' не найдена — остановка.")
            break

except Exception as e:
    print(f"‼️ Ошибка: {e}")

finally:
    driver.quit()
    if new_links:
        with open("links.txt", "a", encoding="utf-8") as f:
            for link in new_links:
                f.write(link + "\n")
        print(f"✅ Сохранено новых ссылок: {len(new_links)}")
    else:
        print("⚠️ Новых ссылок нет, ничего не сохранено.")
