from fastapi import FastAPI
from typing import Dict
import requests
import os

app = FastAPI()

# API-Keys aus Umgebungsvariablen holen
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
LENS_API_KEY = os.getenv("LENS_API_KEY")
OPENCORPORATES_API_KEY = os.getenv("OPENCORPORATES_API_KEY")

@app.get("/competitors")
def competitors(target: str) -> Dict:
    url = f"https://gnews.io/api/v4/search?q={target}&token={GNEWS_API_KEY}&lang=de&max=5"
    response = requests.get(url)
    data = response.json()
    articles = [article["title"] for article in data.get("articles", [])]
    return {"competitors_news": articles}

@app.post("/search_patents")
def search_patents(query: str) -> Dict:
    headers = {"Authorization": f"Bearer {LENS_API_KEY}"}
    body = {
        "query": {"query_string": query},
        "size": 10
    }
    response = requests.post("https://api.lens.org/api/v5/patent/search", json=body, headers=headers)
    data = response.json()
    return {"patent_results": data.get("data", [])}

@app.get("/companies")
def companies_search(q: str) -> Dict:
    url = f"https://api.opencorporates.com/v0.4/companies/search?q={q}&api_token={OPENCORPORATES_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return {"companies": data.get("results", [])}
