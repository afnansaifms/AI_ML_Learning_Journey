from bs4 import BeautifulSoup
from fastapi import FastAPI
import requests

app = FastAPI()


@app.get('/news')
def get_news(page: int = 1, limit: int = 5):
    url = "https://news.ycombinator.com/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    titles = []
    for item in soup.find_all("span", class_="titleline"):
        titles.append(item.get_text(strip=True))

    start = (page - 1) * limit
    end = start + limit
    return {
        "page": page,
        "limit": limit,
        "total": len(titles),
        "data": titles[start:end]
    }