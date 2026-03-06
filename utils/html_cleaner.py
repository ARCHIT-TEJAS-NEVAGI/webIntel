from bs4 import BeautifulSoup

def clean_html(html):

    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    cleaned_text = " ".join(text.split())

    return cleaned_text