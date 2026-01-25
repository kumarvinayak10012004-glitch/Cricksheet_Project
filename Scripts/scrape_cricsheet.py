from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import requests
import os

# ChromeDriver path
driver_path = r"C:\Users\Lenovo\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

service = Service(driver_path)
driver = webdriver.Chrome(service=service)

url = "https://cricsheet.org/matches/"
driver.get(url)
time.sleep(5)

# Find all links on the page
links = driver.find_elements(By.TAG_NAME, "a")

json_links = {}

for link in links:
    href = link.get_attribute("href")
    text = link.text.lower()

    if href and href.endswith(".zip"):
        if "test" in text:
            json_links["test"] = href
        elif "odi" in text:
            json_links["odi"] = href
        elif "t20" in text:
            json_links["t20"] = href
        elif "ipl" in text:
            json_links["ipl"] = href

driver.quit()

print("Found ZIP links:")
for k, v in json_links.items():
    print(k, "->", v)
