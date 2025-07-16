
from fastapi import FastAPI
from typing import Dict

app = FastAPI()

@app.get("/competitors")
def competitors(target: str) -> Dict:
    return {"competitors": [f"{target} Konkurrent A", f"{target} Konkurrent B"]}

@app.get("/substitutes")
def substitutes(product: str) -> Dict:
    return {"substitutes": [f"Alternative zu {product} 1", f"Alternative zu {product} 2"]}

@app.get("/suppliers")
def suppliers(industry: str) -> Dict:
    return {"suppliers": [f"{industry} Lieferant 1", f"{industry} Lieferant 2"]}

@app.get("/newentrants")
def newentrants(industry: str) -> Dict:
    return {"entrants": [f"Neues Unternehmen in {industry} 1", f"Neuer Marktteilnehmer in {industry} 2"]}

@app.get("/customerpower")
def customerpower(market: str) -> Dict:
    return {"customer_power": "Hoch"}
