from bs4 import BeautifulSoup
import requests


def crawl_website(url):

    pages = []

    try:
        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        text_elements = soup.find_all([
            "p", "li", "h1", "h2", "h3", "span"
        ])

        text = " ".join([el.get_text(strip=True) for el in text_elements])

        pages.append(text)

    except Exception as e:
        print("Crawler error:", e)

    return pages