from bs4 import BeautifulSoup
from fastapi import FastAPI
import requests
import time

app = FastAPI()
cache_data=[]
last_fetch=0

@app.get('/news')
def get_news(page: int = 1, limit: int = 5):
    global cache_data, last_fetch
    start = time.time()

    if time.time() - last_fetch > 60:
        print("fetching fresh data")

        url = "https://news.ycombinator.com/"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        cache_data = [
            item.get_text(strip=True) for item in soup.find_all("span", class_="titleline")
        ]
        last_fetch = time.time()
    else:
        print("using cached data")

    end = time.time()
    time_taken = round(end - start, 4)
    print("time taken", time_taken)

    start_index = (page - 1) * limit
    end_index = start_index + limit

    return {
        "time taken": time_taken,
        "page": page,
        "limit": limit,
        "total": len(cache_data),
        "data": cache_data[start_index:end_index]
    }
    