import requests


def fetch_research_insights(traits):
    research_db = {
        "deep root system": "Improves water uptake from deeper soil layers",
        "heat shock protein expression": "Stabilizes proteins under heat stress",
        "waxy leaf coating": "Reduces transpiration and water loss",
        "salt tolerance": "Maintains ion balance under saline conditions",
        "cold tolerance proteins": "Prevents cellular damage during freezing temperatures"
    }

    insights = []

    for t in traits:
        if t in research_db:
            insights.append(research_db[t])
        else:
            insights.append("General stress adaptation mechanism")

    return insights