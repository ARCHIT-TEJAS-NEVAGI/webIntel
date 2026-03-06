from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_links(html, base_url):

    soup = BeautifulSoup(html, "html.parser")

    links = set()

    for a in soup.find_all("a", href=True):

        url = urljoin(base_url, a["href"])

        if urlparse(url).netloc == urlparse(base_url).netloc:
            links.add(url)

    return list(links)