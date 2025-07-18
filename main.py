from fastapi import FastAPI
from typing import Dict
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# API-Keys aus Umgebungsvariablen holen
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
LENS_API_KEY = os.getenv("LENS_API_KEY")
OPENCORPORATES_API_KEY = os.getenv("OPENCORPORATES_API_KEY")

# ---- MODELL FÜR LENS PATENT-SUCHE ----
class PatentQuery(BaseModel):
    query: Dict[str, str]
    size: int = 10

# ---- GNEWS COMPETITORS ----
@app.get("/competitors")
def competitors(target: str) -> Dict:
    url = f"https://gnews.io/api/v4/search?q={target}&token={GNEWS_API_KEY}&lang=de&max=5"
    response = requests.get(url)
    return {"competitors_news": [a["title"] for a in response.json().get("articles", [])]}

# ---- OPENCORPORATES COMPANIES ----
@app.get("/companies")
def companies_search(q: str) -> Dict:
    url = f"https://api.opencorporates.com/v0.4/companies/search?q={q}&api_token={OPENCORPORATES_API_KEY}"
    response = requests.get(url)
    return {"companies": response.json().get("results", [])}

# ---- LENS PATENT SEARCH ----
@app.post("/search_patents")
def search_patents(payload: PatentQuery) -> Dict:
    headers = {"Authorization": f"Bearer {LENS_API_KEY}"}
    body = {
        "query": {"query_string": payload.query["query_string"]},
        "size": payload.size
    }

    response = requests.post("https://api.lens.org/api/v5/patent/search", json=body, headers=headers)

    try:
        data = response.json()
    except Exception:
        return {
            "error": "Lens API Error",
            "status_code": response.status_code,
            "details": response.text
        }

    return {"patent_results": data.get("data", [])}
