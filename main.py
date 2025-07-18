from fastapi import FastAPI
from typing import Dict
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# API-Keys
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
LENS_API_KEY = os.getenv("LENS_API_KEY")
OPENCORPORATES_API_KEY = os.getenv("OPENCORPORATES_API_KEY")

# ---- MODELL FÜR PATENT-SUCHE ----
class PatentQuery(BaseModel):
    query: Dict[str, str]
    size: int = 10

# ---- COMPETITORS ----
@app.get("/competitors")
def competitors(target: str) -> Dict:
    url = f"https://gnews.io/api/v4/search?q={target}&token={GNEWS_API_KEY}&lang=de&max=5"
    response = requests.get(url)
    return {"competitors_news": [a["title"] for a in response.json().get("articles", [])]}

# ---- USPTO PATENTS ----
@app.post("/uspto_patents")
def uspto_patents(search: Dict) -> Dict:
    search_term = search["search_term"]

    url = "https://api.patentsview.org/graphql"
    graphql_query = {
        "query": f"""
        query {{
            patents(input: {{perPage: 5, keyword: "{search_term}"}}) {{
                patentNumber
                patentTitle
                patentDate
            }}
        }}
        """
    }

    response = requests.post(url, json=graphql_query)

    if response.status_code != 200:
        return {
            "error": "GraphQL PatentsView API Error",
            "status_code": response.status_code,
            "details": response.text
        }

    return response.json()


# ---- LENS PATENTS ----
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
            "details": response.text  # <<< gibt auch Plaintext oder HTML bei Fehlern aus
        }

    return {"patent_results": data.get("data", [])}

# ---- COMPANY SEARCH ----
@app.get("/companies")
def companies_search(q: str) -> Dict:
    url = f"https://api.opencorporates.com/v0.4/companies/search?q={q}&api_token={OPENCORPORATES_API_KEY}"
    response = requests.get(url)
    return {"companies": response.json().get("results", [])}
