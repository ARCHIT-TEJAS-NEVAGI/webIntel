import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils.html_cleaner import clean_html


def scrape_with_requests(url):

    try:
        response = requests.get(url, timeout=10)

        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text()

        return html, text

    except Exception:
        return None, None


def scrape_with_selenium(url):

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get(url)

    html = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()

    return html, text


def scrape_page(url):

    # Try fast method first
    html, text = scrape_with_requests(url)

    # If page has little content → fallback
    if text is None or len(text.strip()) < 1000:

        print("Using Selenium fallback...")

        html, text = scrape_with_selenium(url)

    cleaned_text = clean_html(html)

    return html, cleaned_text