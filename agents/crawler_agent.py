import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def crawl_website(base_url, max_pages=10):

    visited = set()
    queue = [base_url]
    pages = []

    while queue and len(visited) < max_pages:

        url = queue.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            text = soup.get_text()
            pages.append(text)

            visited.add(url)

            for link in soup.find_all("a", href=True):

                full_url = urljoin(base_url, link["href"])

                if base_url in full_url:
                    queue.append(full_url)

        except:
            pass

    return pages