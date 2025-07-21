from fastapi import FastAPI
from typing import Dict
import requests
import os

app = FastAPI()

OPENCORPORATES_API_KEY = os.getenv("OPENCORPORATES_API_KEY")

@app.get("/companies")
def companies_search(q: str) -> Dict:
    url = f"https://api.opencorporates.com/v0.4/companies/search?q={q}&api_token={OPENCORPORATES_API_KEY}"
    response = requests.get(url)
    return {"companies": response.json().get("results", [])}
